import sqlite3

conn = sqlite3.connect("dashlane.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS Manager(User TEXT, Pass TEXT, Website TEXT)")


def data_entry(User, Pass, Website):
    "Algo Hashage et generation mdp"
    c.execute("INSERT INTO Manager (User, Pass, Website) VALUES (?, ?, ?)", (User, Pass, Website))
    conn.commit()
    c.close()
    conn.close()


def read_user_info(User):
    "Algo dehasahge"
    c.execute("SELECT * FROM Manager WHERE User=(?)", (User,))
    userdata = c.fetchall()
    print(userdata)


def delete_all_user_info(User):
    c.execute("DELETE from Manager WHERE User=(?)", (User,))
    conn.commit()
    c.close()


def delete_website(User, Pass, Website):
    c.execute("SELECT Pass FROM Manager WHERE User=(?) AND Website=(?)", (User, Website))
    dbpass = c.fetchall()
    for row in dbpass:
        dbpass = (row[0])
    "Algo hashage Pass"
    if Pass == dbpass:
        c.execute("DELETE from Manager WHERE User=(?) AND Website=(?)", (User, Website))
        conn.commit()
        c.close()
        succes = 1
    else:
        print('Error invalid password')
        succes = 0


def update_password(User, Old, New, Website):
    c.execute("SELECT Pass FROM Manager WHERE User=(?) AND Website=(?)", (User, Website))
    dbold = c.fetchall()
    for row in dbold:
        dbold = (row[0])
    "Algo hashage pour old et new"
    if Old == dbold:
        c.execute("UPDATE Manager SET Pass=(?) WHERE Pass=(?) AND Website=(?)", (New, Old, Website))
        conn.commit()
        c.close()
        succes = 1
    else:
        print('Error invalid password')
        succes = 0


def update_user(Pass, newuser, Website):
    c.execute("SELECT Pass FROM Manager WHERE Website=(?)", (Website,))
    dbpass = c.fetchall()
    for row in dbpass:
        dbpass = (row[0])
    "Algo hashage pour Pass"
    if Pass == dbpass:
        c.execute("UPDATE Manager SET User=(?) WHERE Pass=(?) AND Website=(?)", (newuser, Pass, Website))
        conn.commit()
        c.close()
        succes = 1
    else:
        print('Error invalid password')
        succes = 0


