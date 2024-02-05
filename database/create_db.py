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
            id SERIAL PRIMARY KEY,
            user_fio VARCHAR(100),
            manager_id INT NULL,
            FOREIGN KEY(manager_id) REFERENCES managers(id) ON DELETE SET NULL)''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id SERIAL PRIMARY KEY,
            client_id INT,
            descr TEXT,
            weight NUMERIC(10,3),
            size TEXT, 
            addr_from TEXT,
            addr_to TEXT, 
            way_to_py VARCHAR(50),                    
            FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE)''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS pretences (
            id SERIAL PRIMARY KEY,
            client_id INT NULL,
            id_invoice INT NULL,
            email VARCHAR(100), 
            desc_pret TEXT,
            summa NUMERIC(10,2),
            photo TEXT,                
            FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE,
            FOREIGN KEY(id_invoice) REFERENCES invoices(id) ON DELETE CASCADE)''')
    conn.commit()
   

def register_user(user):
    cur.execute('''INSERT INTO users (user_id, user_name, group_name) VALUES (%s, %s, %s)''', user)
    conn.commit()

def check_user(user_id):
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,)) 
    user = cur.fetchone()
    return user 

def select_groups(group_name):
    cur.execute("SELECT user_id FROM users WHERE group_name = %s", (group_name,)) 
    users = cur.fetchone()
    return users 

async def insert_data(data):
    cur.execute('''INSERT INTO dialog (person_name, person, assistant) VALUES (%s, %s, %s)''', data)
    conn.commit()