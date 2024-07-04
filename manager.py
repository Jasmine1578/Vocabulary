import sqlite3
import sqlite3 as sql

def connect_bd(path):
    conn = sql.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(path):
    conn_bd = connect_bd(path)
    conn_bd.execute("""
    CREATE TABLE IF NOT EXISTS vocab (
    id integer primary key,
    word_val varchar(255) not null,
    word_trans  varchar(255) not null
    );
    """)
    conn_bd.commit()
    conn_bd.close()

def insert_values(path):
    conn_bd = connect_bd(path)
    conn_bd.execute("""delete from vocab;""")
    conn_bd.execute("""insert into vocab values (1, 'eat', 'есть')""")
    conn_bd.execute("""insert into vocab values (2, 'build', 'сборка')""")
    conn_bd.execute("""insert into vocab values (3, 'engine', 'движок')""")
    conn_bd.execute("""insert into vocab values (4, 'hardware', 'аппаратное обеспечение')""")
    conn_bd.execute("""insert into vocab values (5, 'software', 'программное обеспечение')""")
    conn_bd.execute("""insert into vocab values (6, 'scrolling', 'прокрутка')""")
    conn_bd.commit()
    conn_bd.close()

def all_vocab(path):
    conn_bd = connect_bd(path)
    cur = conn_bd.cursor()
    req_sql = """
    SELECT 
    *
    FROM vocab;
    """
    try:
        cur.execute(req_sql)
        result = cur.fetchall()
        conn_bd.close()
        if result:
            return result
    except:
        print('Ошибка чтения.')
        conn_bd.close()
    return []