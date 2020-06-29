import eel

###############################################################################DB#######################################################################

import sqlite3
from cryptography.fernet import Fernet
import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import os, sys, inspect

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


DB_PATH = os.getenv('APPDATA')
if not os.path.exists(DB_PATH + '\\Doshlane'):
    os.mkdir(DB_PATH + '\\Doshlane')
DB_PATH = DB_PATH + '\\Doshlane\\doshlane.db'


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
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute(
            "CREATE TABLE User" + Usermain + " (User TEXT, PassMain TEXT, Pass TEXT, Website TEXT, Notes TEXT, Notetitle TEXT, Key TEXT)")
        keyaes = Fernet.generate_key()
        ckeyaes = garycrypt(keyaes.decode())
        c.execute("INSERT INTO User" + Usermain +
                  "(Key) VALUES (?)", (ckeyaes,))
    except sqlite3.OperationalError:
        return False
    else:
        keyaesdecrypt = garydecrypt(ckeyaes)
        PassMainE = PassMain.encode()
        f = Fernet(keyaesdecrypt)
        PassMainEncrypted = f.encrypt(PassMainE)
        c.execute("INSERT INTO User" + Usermain +
                  "(PassMain) VALUES (?)", (PassMainEncrypted,))
        conn.commit()
        c.close()
        conn.close()
        return True


def credential_check(User, Pass):
    try:
        conn = sqlite3.connect(DB_PATH)
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
        conn = sqlite3.connect(DB_PATH)
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
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("SELECT Key FROM User" + Usermain + "")
    keydecrypt = c.fetchall()
    keydecrypt = garydecrypt(keydecrypt[0][0])
    c.execute("SELECT Pass FROM User" + Usermain +
              " WHERE Website=(?) AND User=(?)", (Website, User))
    userdata = c.fetchall()
    userdata = userdata[0][0]
    f = Fernet(keydecrypt)
    userdata = f.decrypt(userdata)
    userdata = userdata.decode("utf-8")
    return userdata


def data_entry(Usermain, User, Pass, Website):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
        return False
    c.execute("SELECT Key FROM User" + Usermain + "")
    keydecrypt = c.fetchall()
    keydecrypt = garydecrypt(keydecrypt[0][0])
    Pass = Pass.encode()
    f = Fernet(keydecrypt)
    Pass = f.encrypt(Pass)
    c.execute("INSERT INTO User" + Usermain +
              "(User, Pass, Website) VALUES (?, ?, ?)", (User, Pass, Website))
    conn.commit()
    c.close()
    return True


def delete_all_user_info(User):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("DELETE from Manager WHERE User=(?)", (User,))
    conn.commit()
    c.close()


def delete_website(Usermain, Passmain, User, Pass, Website):
    try:
        conn = sqlite3.connect(DB_PATH)
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
        c.execute("SELECT Pass FROM User" + Usermain +
                  " WHERE Website=(?) AND User=(?)", (Website, User))
        webpass = c.fetchall()
        webpass = webpass[0][0]
        f = Fernet(keydecrypt)
        webpass = f.decrypt(webpass)
        webpass = webpass.decode("utf-8")
        if Pass == webpass:
            c.execute("DELETE from User" + Usermain +
                      " WHERE Website=(?) AND User=(?)", (Website, User))
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
        conn = sqlite3.connect(DB_PATH)
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
        c.execute("UPDATE User" + Usermain +
                  " SET Pass=(?) WHERE Website=(?)", (Newencrypt, Website,))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def update_user(Usermain, Passmain, New, Website):
    try:
        conn = sqlite3.connect(DB_PATH)
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
        c.execute("UPDATE User" + Usermain +
                  " SET User=(?) WHERE Website=(?)", (New, Website,))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def update_usermain(Olduser, Passmain, Newuser):
    try:
        conn = sqlite3.connect(DB_PATH)
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
        c.execute("ALTER TABLE User" + Olduser +
                  " RENAME TO User" + Newuser + "")
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def update_password_main(Usermain, Passmain, Newpassmain):
    try:
        conn = sqlite3.connect(DB_PATH)
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
        c.execute("UPDATE User" + Usermain +
                  " SET PassMain=(?) WHERE PassMain=(?)", (Newpassmain, dbpass,))
        conn.commit()
        c.close()
        return True
    else:
        print('Error invalid password')
        return False


def read_notes_db(Usermain):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
    c.execute("SELECT Notes, Notetitle FROM User" + Usermain + "")
    Note = c.fetchall()
    Notee = Note[2:]
    final = []
    for i in range(len(Notee)):
        out = []
        Note2 = Notee[i][0]
        Notetitle = Notee[i][1]
        if Note2 is not None:
            f = Fernet(keydecrypt)
            decrypted = f.decrypt(Note2)
            decrypted = decrypted.decode("utf-8")
            out.append(Notetitle)
            out.append(decrypted)
            final.append(out)
    return final


def insert_note_db(Usermain, Note, Notetitle):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
    try:
        c.execute("SELECT Key FROM User" + Usermain + "")
        keydecrypt = c.fetchall()
        keydecrypt = garydecrypt(keydecrypt[0][0])
    except Exception as error:
        print(error)
        return False
    Note = Note.encode()
    f = Fernet(keydecrypt)
    Note = f.encrypt(Note)
    c.execute("INSERT INTO User" + Usermain +
              "(Notes, Notetitle) VALUES (?, ?)", (Note, Notetitle))
    conn.commit()
    c.close()
    return True


def delete_note_db(Usermain, Notetitle):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("DELETE from User" + Usermain +
              " WHERE Notetitle=(?)", (Notetitle,))
    conn.commit()
    c.close()
    return True


def update_note_db(Usermain, Notetitle, Editnote):
    try:
        conn = sqlite3.connect(DB_PATH)
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
    c.execute("UPDATE User" + Usermain +
              " SET Notes=(?) WHERE Notetitle=(?)", (Editnote, Notetitle,))
    conn.commit()
    c.close()
    return True


def update_note_title_db(Usermain, Notetitle, Newnotetitle):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    except Exception as error:
        print(error)
    c.execute("UPDATE User" + Usermain +
              " SET Notetitle=(?) WHERE Notetitle=(?)", (Newnotetitle, Notetitle,))
    conn.commit()
    c.close()
    return True



##################################################################################################################################################################


chrome_dir = os.path.join(os.path.dirname(__file__), "Chrome-bin")
chrome_dir = resource_path("Chrome-bin")
chrome_dir = chrome_dir + '\chrome.exe'

eel.browsers.set_path('chrome', chrome_dir)

USERNAME = ""
PASSMAIN = ""
BASIC_FAIL_MSG = "Something went wrong. Try again later"

# Redirect & log out


@eel.expose
def logout():
    global USERNAME, PASSMAIN
    USERNAME, PASSMAIN = "", ""
    eel.goBackLogin()


@eel.expose
def check_if_logged_in():
    global USERNAME, PASSMAIN
    if (USERNAME == "" or PASSMAIN == ""):
        eel.goBackLogin()


@eel.expose
def login(data):
    global USERNAME, PASSMAIN
    username, password = data["Username"], data["Password"]
    res = credential_check(username, password)
    if res is True:
        USERNAME, PASSMAIN = username, password
        eel.validLogin()
    else:
        eel.failed("Wrong username or password")


@eel.expose
def signup(data):
    global USERNAME, PASSMAIN
    username, password = data["Username"], data["Password"]
    if username == password:
        eel.failed("Hold on, You can't have the same password and username")
    elif len(["True" for x in password if x.isupper()]) == 0:
        eel.failed("You must have at least 1 Caps and 1 number in your password")
    elif len(["True" for x in password if x in [str(x) for x in "1234567890"]]) == 0:
        eel.failed("You must have at least 1 Caps and 1 number in your password")
    elif len(password) < 6:
        eel.failed(
            "This password is secure but too short. It must be at least 6 characters long")
    else:
        res = create_user(username, password)
        if res is True:
            USERNAME, PASSMAIN = username, password
            eel.validSignUp()
        else:
            eel.failed(BASIC_FAIL_MSG)

# Passwords


@eel.expose
def get_pswds_list():
    global USERNAME
    if USERNAME != "":
        eel.retrievePassword(read_user_website(USERNAME))
    else:
        pass


@eel.expose
def get_pswd(user, website):
    res = read_user_password(USERNAME, user, website)
    eel.copyPassword(res)


@eel.expose
def save_password(username, pswd, website):
    res = data_entry(USERNAME, username, pswd, website)
    if res is True:
        eel.addPasswordField(username, website)
    else:
        eel.failed(BASIC_FAIL_MSG)


@eel.expose
def update_password(i, username, website, password):
    res1 = update_password_website(USERNAME, PASSMAIN, password, website)
    res2 = update_user(USERNAME, PASSMAIN, username, website)
    if res1 is True and res2 is True:
        eel.editSuccess()
    else:
        eel.failed(BASIC_FAIL_MSG)


@eel.expose
def delete_password(i, username, website):
    pswd = read_user_password(USERNAME, username, website)
    res = delete_website(USERNAME, PASSMAIN, username, pswd, website)
    if res is True:
        eel.deleteDropdown(i, "pswd")
    else:
        eel.failed(BASIC_FAIL_MSG)

# Notes


@eel.expose
def get_notes_list():
    global USERNAME
    if USERNAME != "":
        eel.retrieveNotes(read_notes_db(USERNAME))
    else:
        pass


@eel.expose
def save_note(note_title, note):
    res = insert_note_db(USERNAME, note, note_title)
    if res is True:
        eel.addNoteField(note_title, note)
    else:
        eel.failed(BASIC_FAIL_MSG)


@eel.expose
def update_note(i, note_title, new_title, new_content):
    res = update_note_title_db(USERNAME, note_title, new_title)
    if res is True:
        res = update_note_db(USERNAME, new_title, new_content)
        if res is True:
            eel.editSuccess()
        else:
            eel.failed(BASIC_FAIL_MSG)
    else:
        eel.failed(BASIC_FAIL_MSG)


@eel.expose
def delete_note(i, note_title):
    res = delete_note_db(USERNAME, note_title)
    if res is True:
        eel.deleteDropdown(i, "note")
    else:
        eel.failed(BASIC_FAIL_MSG)

# Setting


@eel.expose
def update_username_main(data):
    global USERNAME
    username, new_username, password = data
    res = credential_check(username, password)
    print(res)
    if res is True:
        x = update_usermain(username, password, new_username)
        if x == True:
            USERNAME = username
            eel.successUsername()
        else:
            eel.failed(BASIC_FAIL_MSG)
    else:
        eel.failed("Wrong username or password")


@eel.expose
def update_pswd_main(data):
    global PASSMAIN
    password, new_password = data
    res = credential_check(USERNAME, password)
    if res is True:
        x = update_password_main(USERNAME, password, new_password)
        if x == True:
            PASSMAIN = new_password
            eel.successPassword()
        else:
            eel.failed(BASIC_FAIL_MSG)
    else:
        eel.failed("Wrong username or password")


eel.init("Web")
eel.start("index.html", mode='chrome', cmdline_args=["-incognito"])
