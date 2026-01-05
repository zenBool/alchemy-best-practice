from .db import Dialog, Message, session


def query_example():
    d = Dialog('user_id_333')
    c_m = Message(d, 'hello')
    b_m = Message(d, 'again')
    last_msg_obj = Message(d, 'last')

    data = d, c_m, b_m, last_msg_obj

    with session() as s:
        s.add_all(list(data))
        s.commit()

        s.refresh(d)

        # Проверяем, что связь last_message работает правильно
        print(f"Ожидаемое последнее сообщение: {last_msg_obj}")
        print(f"Найденное через relationship: {d.last_message}")
        assert d.last_message is last_msg_obj


if __name__ == '__main__':
    query_example()
