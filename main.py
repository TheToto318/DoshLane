import eel

@eel.expose
def login(data):
    username, password = data["Username"], data["Password"]
    eel.validLogin() if username != password else eel.failed("Wrong username or password")
    
@eel.expose
def signup(data):
    username, password = data["Username"], data["Password"]
    if username == password:
        eel.failed("Hold on, You can't have the same password and username")
    elif len(["True" for x in password if x.isupper()]) == 0:
        eel.failed("You must have at least 1 Caps and 1 number in your password")
    elif len(["True" for x in password if x in [str(x) for x in "1234567890"]]) == 0:
        eel.failed("You must have at least 1 Caps and 1 number in your password")
    elif len(password) < 6:
        eel.failed("This password is secure but too short. It must be at least 6 characters long")
    else:
        eel.validSignUp()

eel.init("Web")
eel.start("index.html", cmdline_args=["-incognito"])