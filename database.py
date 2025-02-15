import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT NOT NULL,
    chat_id INTEGER NOT NULL
)
''')



def getUser(link):
    con = None
    cur = None
    try:
        con = sqlite3.connect('database.db')
        cur = con.cursor()

        cur.execute('''
            SELECT chat_id
            FROM links
            WHERE link = ?
            ORDER BY chat_id
        ''', (link,))

        data = cur.fetchall()

        return data[0][0]

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        if cur:
            cur.close()
        if con:
            con.close()

def create_link(link, chat_id):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    cur.execute('''
               SELECT link
               FROM links
               WHERE chat_id = ?
           ''', (chat_id,))

    data = cur.fetchone()

    if data:

        cur.execute('''
                   UPDATE links
                   SET link = ?
                   WHERE chat_id = ?
               ''', (chat_id, link))
    else:

        cur.execute('''
                   INSERT INTO links (link, chat_id)
                   VALUES (?, ?)
               ''', (link, chat_id))

    con.commit()


    cur.close()
    con.close()
