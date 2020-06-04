import sqlite3


def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, patient text, address text, prescription text, date text)")
    conn.commit()
    conn.close()


def insert(patient, address, prescription, date):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book VALUES (NULL,?,?,?,?)",
                (patient, address, prescription, date))
    conn.commit()
    conn.close()
    view()


def view():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows


def search(patient="", address="", prescription="", date=""):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE patient=? OR address=? OR prescription=? OR date=?",
                (patient, address, prescription, date))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete(id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()


def update(id, patient, address, prescription, date):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("UPDATE book SET patient=?, address=?, prescription=?, date=? WHERE id=?",
                (patient, address, prescription, date, id))
    conn.commit()
    conn.close()


connect()
