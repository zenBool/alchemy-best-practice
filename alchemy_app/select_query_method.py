import sqlalchemy as sa
from .db import Dialog, Message, current_session, session

Dialog.query = current_session.query_property()


def some_handler1():
    dialogs = Dialog.query.all()

def some_handler2():
    dialogs = current_session.query(Dialog).all()

def some_handler3():
    with session() as s:
        dialogs = s.query(Dialog).all()

def some_handler3a():
    with session() as s:
        dialog = Dialog(325)
        s.add(dialog)

        first = s.query(Dialog).first()
        last = s.query(Dialog).filter(Dialog.id == sa.func.max(Dialog.id)).first()

        print('Fist dialog id:', first)
        print('Last dialog id:', last)

def some_handler4():
    dialog = Dialog('test')
    message = Message(dialog, 'hello')

    with session() as s:
        s.add(message)
        for (d, m) in s.query(Dialog, Message).all():
            print(dir(m))
            exit(0)


if __name__ == '__main__':
    some_handler3a()
