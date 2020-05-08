import sqlite3

conn = sqlite3.connect("dashlane.db")
c = conn.cursor()


def create_user(Usermain, PassMain):
    c.execute("CREATE TABLE User" + Usermain + "(User TEXT, PassMain TEXT, Pass TEXT, Website TEXT)")
    c.execute("INSERT INTO User" + Usermain + "(PassMain) VALUES (?)", (PassMain,))
    conn.commit()
    c.close()
    conn.close()
    succes = True


def credential_check(User, Pass):
    try:
        c.execute("SELECT PassMain FROM User" + User + "")
    except sqlite3.OperationalError:
        print('Not exist')
        succes = False
    else:
        dbpass = c.fetchall()
        dbpass = (dbpass[0][0])
        "Algo dehashage Pass"
        if Pass == dbpass:
            succes = True
        else:
                print('Error invalid password')
                succes = False


def read_user_info(User):
    "Algo dehasahge"
    c.execute("SELECT User, Pass, Website FROM User" + User + "")
    userdata = c.fetchall()
    print(userdata)


def data_entry(Usermain, User, Pass, Website):
    "Algo Hashage et generation mdp"
    c.execute("INSERT INTO User" + Usermain + "(User, Pass, Website) VALUES (?, ?, ?)", (User, Pass, Website))
    conn.commit()
    c.close()


def delete_all_user_info(User):
    c.execute("DELETE from Manager WHERE User=(?)", (User,))
    conn.commit()
    c.close()


def delete_website(Usermain, Pass, Website):
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    if Pass == dbpass:
        c.execute("DELETE from User" + Usermain + " WHERE Website=(?)", (Website,))
        conn.commit()
        c.close()
        succes = True
    else:
        print('Error invalid password')
        succes = False


def update_password_website(Usermain, Passmain, New, Website):
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    "Algo hashage pour old et new"
    print(dbpass)
    if dbpass == Passmain:
        c.execute("UPDATE User" + Usermain + " SET Pass=(?) WHERE Website=(?)", (New, Website,))
        conn.commit()
        c.close()
        succes = True
    else:
        print('Error invalid password')
        succes = False


def update_user(Usermain, Passmain, New, Website):
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    "Algo hashage pour Pass"
    if dbpass == Passmain:
        c.execute("UPDATE User" + Usermain + " SET User=(?) WHERE Website=(?)", (New, Website,))
        conn.commit()
        c.close()
        succes = True
    else:
        print('Error invalid password')
        succes = False
