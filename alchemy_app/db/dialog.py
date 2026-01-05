import sqlalchemy as sa
from sqlalchemy import orm as so
from sqlalchemy.ext.declarative import declared_attr

from .base import Base


class Dialog(Base):
    __tablename__ = "dialog"

    id = sa.Column('dialog_id', sa.Integer, primary_key=True)

    created_at = sa.Column(
        sa.DateTime(), nullable=False, server_default=sa.func.now(),
    )
    user_id = sa.Column(sa.String, nullable=False, index=True,)

    def __init__(self, user_id):
        self.user_id = user_id

    @declared_attr
    def last_message(cls):
        def condition():
            from sqlalchemy.orm import foreign, remote
            from .message import Message

            message = sa.alias(Message, 'msg')

            subquery = sa.select(
                sa.func.max(remote(message.c.message_id))
            ).where(
                remote(message.c.dialog_id) == foreign(Dialog.id)
            ).scalar_subquery()

            dialog_condition = remote(Message.dialog_id) == foreign(Dialog.id)
            message_condition = remote(Message.id) == subquery
            return dialog_condition & message_condition

        return so.relationship('Message', primaryjoin=condition, uselist=False, viewonly=True)

    # @declared_attr
    # def last_message(cls):
    #     """Отношение, указывающее на последнее сообщение в диалоге.
    #     Работает через коррелированный подзапрос. Только для чтения.
    #     """
    #     # from .message import Message
    #     # Получаем класс Message из реестра, чтобы избежать прямого импорта
    #     Message = cls.registry.mappers['Message'].class_
    #
    #     # 1. Создаем подзапрос для нахождения ID последнего сообщения
    #     #    для каждого диалога.
    #     subq = (
    #         sa.select(sa.func.max(Message.id))
    #         .where(Message.dialog_id == cls.id)
    #         .correlate_except(Message)  # Указываем, что подзапрос коррелирован с Dialog
    #         .scalar_subquery()
    #     )
    #
    #     # 2. Определяем условие для связи:
    #     #    - ID диалога должен совпадать
    #     #    - ID сообщения должен быть равен ID, найденному в подзапросе
    #     primaryjoin_condition = sa.and_(
    #         cls.id == Message.dialog_id,
    #         Message.id == subq
    #     )
    #
    #     return so.relationship(
    #         Message,
    #         primaryjoin=primaryjoin_condition,
    #         uselist=False,
    #         viewonly=True,
    #     )
