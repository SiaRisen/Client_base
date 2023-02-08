import psycopg2


def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Clients (
        id SERIAL  PRIMARY KEY, 
        first_name VARCHAR(60) NOT NULL,
        last_name  VARCHAR(60) NOT NULL,
        email      VARCHAR(60) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Phones (
        id SERIAL    PRIMARY KEY,
        phone_number BIGINT NOT NULL,
        client_id    INTEGER NOT NULL REFERENCES Clients(id)
    );
    """)
    print("Таблицы созданы")


def add_client(cur, first_name: str, last_name: str, email, phone_number=None):
    # first_name = input("Введите имя:")
    # last_name = input("Введите фамилию:")
    # email = input("Введите email:")
    cur.execute("""
    INSERT INTO Clients (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
    """, (first_name, last_name, email))
    client_id = cur.fetchone()[0]

    # phone_number = int(input("Введите номер телефона:"))
    cur.execute("""
    INSERT INTO Phones (phone_number, client_id) VALUES (%s, %s) RETURNING id; 
    """, (phone_number, client_id))

    cur.execute("""
    SELECT * FROM Clients;
    """)
    print(cur.fetchall())

    cur.execute("""
    SELECT * FROM Phones;
    """)
    print(cur.fetchall())


def add_phone(cur, phone_number, client_id):
    # phone_number = int(input("Введите номер телефона:"))
    # client_id = input("Введите id клиента:")
    cur.execute("""
    INSERT INTO Phones (phone_number, client_id) VALUES (%s, %s) RETURNING id; 
    """, (phone_number, client_id))
    cur.execute("""
    SELECT * FROM Phones;
    """)
    print(cur.fetchall())


def change_data(cur, client_id, first_name=None, last_name=None, email=None, phone_number=None):
    # client_id = input("Введите id клиента:")
    # first_name = input("Введите имя:")
    # last_name = input("Введите фамилию:")
    # email = input("Введите email:")
    # phone_number = int(input("Введите номер телефона:"))
    if first_name:
        cur.execute("""
        UPDATE Clients SET first_name=%s WHERE id=%s;
        """, (first_name, client_id))
        cur.execute("""
        SELECT first_name FROM Clients WHERE id=%s;
        """, (client_id,))
        print("Изменено:", cur.fetchone())
    elif last_name:
        cur.execute("""
        UPDATE Clients SET last_name=%s WHERE id=%s;
        """, (last_name, client_id))
        cur.execute("""
        SELECT last_name FROM Clients WHERE id=%s;
        """, (client_id,))
        print("Изменено:", cur.fetchone())
    elif email:
        cur.execute("""
        UPDATE Clients SET e_mail=%s WHERE id=%s;
        """, (email, client_id))
        cur.execute("""
        SELECT email FROM Clients WHERE id=%s;
        """, (client_id,))
        print("Изменено:", cur.fetchone())
    elif phone_number:
        cur.execute("""
        UPDATE Phones SET phone_number=%s WHERE id=%s;
        """, (phone_number, client_id))
        cur.execute("""
        SELECT phone_number FROM Phones WHERE id=%s;
        """, (client_id,))
        print("Изменено:", cur.fetchone())


def delete_phone(cur, client_id, phone_number):
    # phone_number = int(input("Введите номер телефона:"))
    # client_id = input("Введите id клиента:")
    cur.execute("""
    DELETE FROM Phones WHERE id=%s AND phone_number=%s;
    """, (client_id, phone_number))
    cur.execute("""
    SELECT * FROM Phones;
    """)
    print(cur.fetchall())


def delete_client(cur, client_id):
    # client_id = input("Введите id клиента:")
    cur.execute(""" 
    DELETE FROM Phones WHERE id=%s;
    """, (client_id,))

    cur.execute(""" 
    DELETE FROM Clients WHERE id=%s;
    """, (client_id,))

    cur.execute("""
    SELECT * FROM Clients;
    """)
    print(cur.fetchall())

    cur.execute("""
        SELECT * FROM Phones;
        """)
    print(cur.fetchall())


def search_client(cur, first_name=None, last_name=None, email=None, phone_number=None):
    # first_name = input("Введите имя:")
    # last_name = input("Введите фамилию:")
    # email = input("Введите email:")
    # phone_number = int(input("Введите номер телефона:"))
    cur.execute("""
    SELECT * FROM Clients c
    JOIN Phones p ON c.id = p.client_id
    WHERE first_name=%s OR last_name=%s OR email=%s OR phone_number=%s
    """, (first_name, last_name, email, phone_number))
    print(cur.fetchall())


def delete_db(cur):
    cur.execute("""
    DROP TABLE Phones;
    DROP TABLE Clients;
    """)
    print("Таблицы успешно удалены")


def main():
    print("Используйте команды: "
    "1-создать БД, 2-добавить нового клиента, 3-добавить телефон для существующего клиента,\
    4-изменить данные о клиенте, 5-удалить телефон для существующего клиента, 6-удалить существующего клиента,\
    7-найти клиента по его данным(имени, фамилии, email-у или телефону), 8-удалить таблицы, 9-завершить ввод")
    with psycopg2.connect(database="clients", user="postgres", password=" ") as conn:
        with conn.cursor() as cur:
            while True:
                command = input("Введите команду: ")
                if command == "1":
                    create_db(cur)
                    conn.commit()
                if command == "2":
                    add_client(cur, first_name='Anne', last_name='Dou', email='AnnD@gmail.com', phone_number='89847654789')
                if command == "3":
                    add_phone(cur, '89269123764', 1)
                if command == "4":
                    change_data(cur, 1, first_name='Jane', last_name='Parker', email='PrestiJ@mail.ru', phone_number='84536789012')
                if command == "5":
                    delete_phone(cur, 1, '89847654789')
                if command == "6":
                    delete_client(cur, 1)
                if command == "7":
                    search_client(cur, first_name=None, last_name='Parker', email=None, phone_number=None)
                if command == "8":
                    delete_db(cur)
                if command == "9":
                    break

    conn.close()


if __name__ == '__main__':
    main()
