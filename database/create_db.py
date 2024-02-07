import psycopg2 
import os 
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('DB_HOST')
name = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

def connect_to_database():
    global conn, cur
    conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=name)
    cur = conn.cursor()
    if conn:
        print('DataBase connected')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INT PRIMARY KEY,
            user_fio VARCHAR(100),
            manager_id INT NULL,
            FOREIGN KEY(manager_id) REFERENCES managers(id) ON DELETE SET NULL)''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id SERIAL PRIMARY KEY,
            client_id INT,
            descr TEXT,
            weight VARCHAR(20),
            size TEXT, 
            addr_from TEXT,
            addr_to TEXT, 
            way_to_py VARCHAR(50),                    
            FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE)''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS pretences (
            id SERIAL PRIMARY KEY,
            client_id INT,
            id_invoice INT,
            email VARCHAR(100), 
            desc_pret TEXT,
            summa text,
            photo TEXT,                
            FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE,
            FOREIGN KEY(id_invoice) REFERENCES invoices(id) ON DELETE CASCADE)''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS client_manager (
            manager_id INT,
            client_id INT,     
            PRIMARY KEY(manager_id, client_id), 
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(manager_id) REFERENCES managers(id))''')
    conn.commit()



async def add_invoices(data):
    cur.execute('''INSERT INTO invoices (client_id, descr, weight, size, addr_from, addr_to, way_to_py) VALUES (%s, %s, %s, %s, %s, %s, %s )''', tuple(data.values()))
    conn.commit()
    cur.execute("SELECT currval(pg_get_serial_sequence('invoices','id'))") 
    last = cur.fetchone()
    return last

async def add_pretences(data):
    cur.execute('''INSERT INTO pretences (client_id, id_invoice, email, desc_pret, summa, photo) VALUES (%s, %s, %s, %s, %s, %s)''', tuple(data.values()))
    conn.commit()


async def reg_client(client):
    cur.execute('''INSERT INTO clients (id, user_fio,manager_id) VALUES (%s, %s,  %s)''', client)
    conn.commit()


async def find_manager():
    cur.execute("select manager_id from client_manager group by manager_id order by count(client_id) asc limit 1;") 
    manager = cur.fetchone()
    return manager

async def select_manager(client_id):
    cur.execute("SELECT manager_id FROM clients WHERE id = %s", (client_id,)) 
    man_id = cur.fetchone()
    return man_id


async def select_client(client_id):
    cur.execute("SELECT count(*) FROM clients WHERE id = %s", (client_id,)) 
    count = cur.fetchone()
    return count