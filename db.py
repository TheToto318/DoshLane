import sqlite3
from cryptography.fernet import Fernet
import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d


def garycrypt(data):
    data2 = str.encode(data)
    out = b64e(zlib.compress(data2, 9))
    return out.decode("utf-8")


def garydecrypt(data):
    data2 = str.encode(data)
    out = zlib.decompress(b64d(data))
    return out.decode("utf-8")


def create_user(Usermain, PassMain):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute(
            "CREATE TABLE User" + Usermain + " (User TEXT, PassMain TEXT, Pass TEXT, Website TEXT, Notes TEXT, Notetitle TEXT, Key TEXT)")
        keyaes = Fernet.generate_key()
        ckeyaes = garycrypt(keyaes.decode())
        c.execute("INSERT INTO User" + Usermain + "(Key) VALUES (?)", (ckeyaes,))
    except sqlite3.OperationalError:
        return False
    else:
        keyaesdecrypt = garydecrypt(ckeyaes)
        PassMainE = PassMain.encode()
        f = Fernet(keyaesdecrypt)
        PassMainEncrypted = f.encrypt(PassMainE)
        c.execute("INSERT INTO User" + Usermain + "(PassMain) VALUES (?)", (PassMainEncrypted,))
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
        c.execute("SELECT Key FROM User" + User + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    try:
        c.execute("SELECT PassMain FROM User" + User + "")
    except sqlite3.OperationalError:
        print('Not exist')
        return False
    else:
        dbpass = c.fetchall()
        dbpass = dbpass[1][0]
        f = Fernet(keydecrypt)
        dbpass = f.decrypt(dbpass)
        dbpass = dbpass.decode("utf-8")
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
    c.execute("SELECT Key FROM User" + Usermain + "")
    keydecrypt = c.fetchall()
    keydecrypt = garydecrypt(keydecrypt[0][0])
    c.execute("SELECT Pass FROM User" + Usermain + " WHERE Website=(?) AND User=(?)", (Website, User))
    userdata = c.fetchall()
    userdata = userdata[0][0]
    f = Fernet(keydecrypt)
    userdata = f.decrypt(userdata)
    userdata = userdata.decode("utf-8")
    return userdata


def data_entry(Usermain, User, Pass, Website):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT Key FROM User" + Usermain + "")
    keydecrypt = c.fetchall()
    keydecrypt = garydecrypt(keydecrypt[0][0])
    Pass = Pass.encode()
    f = Fernet(keydecrypt)
    Pass = f.encrypt(Pass)
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
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = dbpass[1][0]
    f = Fernet(keydecrypt)
    dbpass = f.decrypt(dbpass)
    dbpass = dbpass.decode("utf-8")
    if Passmain == dbpass:
        c.execute("SELECT Pass FROM User" + Usermain + " WHERE Website=(?) AND User=(?)", (Website, User))
        webpass = c.fetchall()
        webpass = webpass[0][0]
        f = Fernet(keydecrypt)
        webpass = f.decrypt(webpass)
        webpass = webpass.decode("utf-8")
        if Pass == webpass:
            c.execute("DELETE from User" + Usermain + " WHERE Website=(?) AND User=(?)", (Website, User))
            conn.commit()
            c.close()
            return True
        else:
            print("website password invalid")
            return False
    else:
        print('Master password invalid')
        return False


def update_password_website(Usermain, Passmain, New, Website):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = dbpass[1][0]
    f = Fernet(keydecrypt)
    dbpass = f.decrypt(dbpass)
    dbpass = dbpass.decode("utf-8")
    print(dbpass)
    if dbpass == Passmain:
        New = New.encode()
        f = Fernet(keydecrypt)
        Newencrypt = f.encrypt(New)
        c.execute("UPDATE User" + Usermain + " SET Pass=(?) WHERE Website=(?)", (Newencrypt, Website,))
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
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = dbpass[1][0]
    f = Fernet(keydecrypt)
    dbpass = f.decrypt(dbpass)
    dbpass = dbpass.decode("utf-8")
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
    try:
        c.execute("SELECT Key FROM User" + Olduser + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Olduser + "")
    dbpass = c.fetchall()
    dbpass = dbpass[1][0]
    f = Fernet(keydecrypt)
    dbpass = f.decrypt(dbpass)
    dbpass = dbpass.decode("utf-8")
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
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    c.execute("SELECT PassMain FROM User" + Usermain + "")
    dbpass = c.fetchall()
    dbpass = dbpass[1][0]
    f = Fernet(keydecrypt)
    dbpass = f.decrypt(dbpass)
    dbpass = dbpass.decode("utf-8")
    if dbpass == Passmain:
        Newpassmain = Newpassmain.encode()
        f = Fernet(keydecrypt)
        Newpassmain = f.encrypt(Newpassmain)
        dbpasscrypt = dbpass[1][0]
        c.execute("SELECT PassMain FROM User" + Usermain + "")
        dbpass = c.fetchall()
        dbpass = dbpass[1][0]
        c.execute("UPDATE User" + Usermain + " SET PassMain=(?) WHERE PassMain=(?)", (Newpassmain, dbpass,))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def read_notes(Usermain, Notetitle):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    c.execute("SELECT Notes FROM User" + Usermain + " WHERE Notetitle=(?)", (Notetitle, ))
    Note = c.fetchall()
    Note = Note[0][0]
    f = Fernet(keydecrypt)
    Note = f.decrypt(Note)
    Note = Note.decode("utf-8")
    print(Note)
    return Note


def insert_notes(Usermain, Note, Notetitle):
    try:
        conn = sqlite3.connect("dashlane.db")
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    Note = Note.encode()
    f = Fernet(keydecrypt)
    Note = f.encrypt(Note)
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
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    Editnote = Editnote.encode()
    f = Fernet(keydecrypt)
    Editnote = f.encrypt(Editnote)
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
