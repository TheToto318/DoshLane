import sqlite3


def create_user(Usermain, PassMain):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute(
            "CREATE TABLE User" + Usermain + " (User TEXT, PassMain TEXT, Pass TEXT, Website TEXT, Notes TEXT, Notetitle TEXT)")
    except sqlite3.OperationalError:
        return False
    else:
        c.execute("INSERT INTO User" + Usermain + "(PassMain) VALUES (?)", (PassMain,))
        conn.commit()
        c.close()
        conn.close()
        return True


def credential_check(User, Pass):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute("SELECT PassMain FROM User" + User + "")
    except sqlite3.OperationalError:
        print('Not exist')
        return False
    else:
        dbpass = c.fetchall()
        dbpass = (dbpass[0][0])
        "Algo dehashage Pass"
        if Pass == dbpass:
            return True
        else:
            print('Error invalid password')
            return False


def read_user_website(User):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    "Algo dehasahge"
    c.execute("SELECT User, Website FROM User" + User + "")
    userdata = c.fetchall()
    temp = []
    for x in userdata[1:]:
        if x != (None, None):
            temp.append(x)
    return temp


def read_user_password(Usermain, User, Website):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT Pass FROM User" + Usermain + " WHERE Website=(?)", (Website,))
    "algo dehashage"
    userdata = c.fetchall()
    return userdata


def data_entry(Usermain, User, Pass, Website):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    "Algo Hashage et generation mdp"
    c.execute("INSERT INTO User" + Usermain + "(User, Pass, Website) VALUES (?, ?, ?)", (User, Pass, Website))
    conn.commit()
    c.close()


def delete_all_user_info(User):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("DELETE from Manager WHERE User=(?)", (User,))
    conn.commit()
    c.close()


def delete_website(Usermain, Passmain, User, Pass, Website):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    if Pass == dbpass:
        c.execute("DELETE from User" + Usermain + " WHERE Website=(?) AND User=(?) AND Pass=(?)", (Website, User, Pass))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def update_password_website(Usermain, Passmain, New, Website):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    "Algo hashage pour old et new"
    print(dbpass)
    if dbpass == Passmain:
        c.execute("UPDATE User" + Usermain + " SET Pass=(?) WHERE Website=(?)", (New, Website,))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def update_user(Usermain, Passmain, New, Website):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    "Algo hashage pour Pass"
    if dbpass == Passmain:
        c.execute("UPDATE User" + Usermain + " SET User=(?) WHERE Website=(?)", (New, Website,))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def update_usermain(Olduser, Passmain, Newuser):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Olduser + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    "Algo hashage pour Pass"
    if dbpass == Passmain:
        c.execute("ALTER TABLE User" + Olduser + " RENAME TO User" + Newuser + "")
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def update_password_main(Usermain, Passmain, Newpassmain):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = (dbpass[0][0])
    "Algo hashage pour Pass"
    if dbpass == Passmain:
        c.execute(f"UPDATE User" + Usermain + " SET PassMain=(?) WHERE PassMain=(?)", (Newpassmain, Passmain,))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def insert_notes(Usermain, Note, Notetitle):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("INSERT INTO User" + Usermain + "(Notes, Notetitle) VALUES (?, ?)", (Note, Notetitle))
    conn.commit()
    c.close()


def delete_notes(Usermain, Notetitle):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("DELETE from User" + Usermain + " WHERE Notetitle=(?)", (Notetitle,))
    conn.commit()
    c.close()
    return True


def update_notes(Usermain, Notetitle, Editnote):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("UPDATE User" + Usermain + " SET Notes=(?) WHERE Notetitle=(?)", (Editnote, Notetitle,))
    conn.commit()
    c.close()
    return True


def update_notes_title(Usermain, Notetitle, Newnotetitle):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("UPDATE User" + Usermain + " SET Notetitle=(?) WHERE Notetitle=(?)", (Newnotetitle, Notetitle,))
    conn.commit()
    c.close()
    return True

# TODO Update usermain and password OK
# TODO Update note and note title, delete notes OK
# TODO Initiate db (try execpt)
# TODO f string

