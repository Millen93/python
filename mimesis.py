import psycopg2
from mimesis import Generic
from mimesis.locales import Locale
from mimesis.enums import TimestampFormat

###Setting localisation of fake data
generic = Generic(locale=Locale.EN)

###Amount of fake data 
fake_data = 10

###Creating connection to db
conn = psycopg2.connect(
    host="uwu",
    database="db",
    password="password",
    user="postgres"
)

###Creating script for test tables in db
def create_tables(conn):
    commands = (
    """
    CREATE TABLE client (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(50) NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE transaction (
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES client(id),
        card_num VARCHAR(21) NOT NULL,
        price VARCHAR(15) NOT NULL)
    """,
    """
     CREATE TABLE shop(
        id SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES client(id),
        transaction_id INTEGER NOT NULL REFERENCES transaction(id),
        address VARCHAR(50) NOT NULL,
        consultant VARCHAR(50) NOT NULL,
        timestamp TIMESTAMP NOT NULL
    )
    """
    )
    cur=conn.cursor()
    for _ in commands:
        cur.execute(_)
        conn.commit
print('Create tables yes or no in db')
answ = input()
if answ == 'yes':
    create_tables(conn)

### Creating fake data for client
def client_table():
    client = generic.person.full_name()
    return client

def inserting_client(cur, client):
    cur.execute("INSERT INTO client (full_name) VALUES (%s) RETURNING id", (client,))
    id = cur.fetchone()[0]
    conn.commit()
    return id

### Creating fake data for transaction
def transaction_table(client_id):
    card_num = generic.payment.credit_card_number()
    value = generic.finance.price()
    symbol = generic.finance.currency_symbol()
    price =  str(value)+" "+symbol
    return client_id, price, card_num

def inserting_transaction(cur, client_id, price, card_num):
    cur.execute("INSERT INTO transaction (client_id, card_num, price) VALUES (%s, %s, %s) RETURNING id",
                   (client_id, card_num, price))
    transaction_id = cur.fetchone()[0]
    conn.commit()
    return client_id, transaction_id

### Creating fake data for shop
def shop_table(client_id, transaction_id):
    street = generic.address.street_name()
    num = generic.address.street_number()
    cons = generic.person.full_name()
    time = generic.datetime.timestamp(fmt=TimestampFormat.RFC_3339)
    address = str(street) + " " + num
    return client_id, transaction_id, address, cons, time

def inserting_shop(cur, client_id, transaction_id, address, cons, time):
    cur.execute("INSERT INTO shop (client_id, transaction_id, address, consultant, timestamp) VALUES (%s, %s, %s, %s, %s)",
                   (client_id, transaction_id, address, cons, time))
    conn.commit()

cursor = conn.cursor()
###Start generating
for _ in range(fake_data):
    client = client_table()
    client_id = inserting_client(cursor, client)
    transaction = transaction_table(client_id)
    ids = inserting_transaction(cursor, *transaction)
    shop = shop_table(*ids)
    inserting_shop(cursor, *shop)
