from Assets.db import *
import eel

USERNAME = ""
PASSMAIN = ""
BASIC_FAIL_MSG = "Something went wrong. Try again later"


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
    eel.retrievePassword(read_user_website(USERNAME))


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
    eel.retrieveNotes(read_notes_db(USERNAME))


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
eel.start("index.html", cmdline_args=["-incognito"])
