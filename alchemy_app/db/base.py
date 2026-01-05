import os
import typing
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase, Session as SessionType

from dotenv import load_dotenv

# Загружаем .env из корня проекта.
load_dotenv()


# 1. Современная декларативная база
class Base(DeclarativeBase):
    pass

metadata = Base.metadata

# 2. Создаем синхронный движок.
# SQLAlchemy 2.0 требует синхронный драйвер для create_engine.
db_url = os.environ.get("DB_URL")
if not db_url:
    raise ValueError("Переменная окружения DB_URL не установлена.")

engine = create_engine(db_url, echo=False)


# 3. Создаем сконфигурированный класс "Session"
# Движок привязывается здесь.
Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4. Создаем ScopedSession для управления сессиями в потоках
# Это обеспечивает сессию, локальную для текущего потока (thread-local).
current_session = scoped_session(Session)

# Привязываем метаданные из Base к движку.
Base.metadata.bind = engine

# Привязываем метаданные из Base к движку.
Base.metadata.create_all(engine)

# 5. Переписываем контекстный менеджер для работы со scoped_session
@contextmanager
def session(**kwargs) -> typing.ContextManager[SessionType]:
    """
    Контекстный менеджер, который управляет транзакциями в рамках current_session.
    Он начинает транзакцию и выполняет commit, если не было исключений.
    В случае ошибки выполняется rollback.
    """
    s = current_session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        # Реестр scoped_session сам управляет закрытием сессии.
        current_session.remove()
