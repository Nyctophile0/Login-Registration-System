import sqlite3
import os
import time
import pyfiglet
from termcolor import cprint
import pwinput
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import check_password_hash, generate_password_hash

# Connection
con = sqlite3.connect('test.db')

# Cursor
cur = con.cursor()

# Validating email address
def emailvalidate(email):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        #print(str(e))
        return str(e)

# Ensuring proper input
def configureinput():
    '''while True:
        try:
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            confirmpassword = input("Confirm Password: ")
        except ValueError:
            print("Field cannot be blank.")
            continue

        if not name or email or password or confirmpassword:
            print("Field cannot be blank.")
        else:
            break'''

    name = False
    email = False
    password = False
    confirmpassword = False

    while not name:
        name = input("Name: ")

        if not name:
            cprint("Field cannot be blank!", 'red')

    while True:
        email = input("Email: ")
        check = emailvalidate(email)

        if not email:
            cprint("Field cannot be blank!", 'red')

        elif check:
            print(check)
        else:
            break

    while not password:
        password = pwinput.pwinput("Password: ")

        if not password:
            cprint("Field cannot be blank!", 'red')

        # checking for strong password
        if any(x.isupper() for x in password) and any(x.islower() for x in password) and any(x.isdigit() for x in password) and len(password) >= 7:
            cprint("Strong Password!", 'green')
        else:
            cprint("Weak Password!. Password should contain atleast one lowercase letter, one uppercase letter, one digit and its length should be more than 7.", 'red')
            password = False

    while not confirmpassword:
        confirmpassword = pwinput.pwinput("Confirm Password: ")

        if not confirmpassword:
            cprint("Field cannot be blank!", 'red')

    if password != confirmpassword:
        cprint("Sorry, Passwords don't match. Try again!", 'red')
        while True:
            password = pwinput.pwinput("Password: ")
            confirmpassword = pwinput.pwinput("Confirm Password: ")

            if password == confirmpassword:
                break
            else:
                cprint("Sorry, Passwords don't match. Try again!", 'red')

    return name, email, password, confirmpassword

def header():
    os.system('clear')
    cprint(pyfiglet.figlet_format("Login/ Register System", font='digital'))


def main():
    while True:
        print()
        print("1.Create a table\n2.Login\n3.Register\n4.Delete/ Drop Table\n5.Exit")
        choice = input("\nEnter: ")
        print()

        # Creating table
        if choice == '1':
            try:
                cur.execute('CREATE TABLE user (user_id INTEGER NOT NULL, username TEXT NOT NULL, name TEXT NOT NULL, email TEXT NOT NULL, password_hash TEXT NOT NULL, PRIMARY KEY(user_id))')
                cprint('Table created!', 'green')
            except:
                cprint("Table already exists!", 'green')

        # Exit
        elif choice == '5':
            print("Exiting program ..")
            time.sleep(.5)
            print('Exited!')
            exit(1)

        # Register
        elif choice == '3':
            username = False

            while True:
                username = input("Username :")
                check = cur.execute('SELECT * FROM user WHERE username = ?', [username])
                if not username:
                    cprint("Field cannot be blank.", 'red')

                elif len(check.fetchall()) != 0:
                    cprint("Username already taken. Try again.", 'red')
                else:
                    break

            userdata = []

            for x in check:
                userdata.append(x)

            '''while True:
                if len(userdata) != 0:
                    cprint("Username already taken. Try again.", 'red')
                    username = input("Username: ")
                else:
                    break'''

            variables = configureinput()
            name = variables[0]
            email = variables[1]
            password = variables[2]
            cur.execute('INSERT INTO user (username, name, email, password_hash) VALUES (?, ?, ?, ?)', (username, name, email, generate_password_hash(password)))

            con.commit()
            cprint("\nUser Registered!", 'green')


        # Login
        elif choice == '2':
            data = cur.execute("SELECT * FROM user")

            if len(data.fetchall()) == 0:
                cprint("Can't log you in. You have to register yourself first!", 'red')
                break

            username = False
            password = False

            while not username:
                username = input("Username: ")
                if not username:
                    cprint("Field cannot be blank!", 'red')

            while not password:
                password = pwinput.pwinput("Password: ")
                if not password:
                    cprint("Field cannot be blank!", 'red')

            # Checking for username in database
            user_data1 = cur.execute("SELECT * FROM user WHERE username = ?", [username])
            if len(user_data1.fetchall()) == 0:
                cprint("\nNo data exists for such username!", 'red')
                break

            # Copying all data of user into list
            user_data1 = cur.execute("SELECT * FROM user WHERE username = ?", [username])
            user_list = []
            for x in user_data1:
                user_list.append(x)

            if not check_password_hash(user_list[0][4], password):
                cprint("\nWrong Password!. Can't log you in.", 'red')
            else:
                print()
                cprint("You are successfully logged in! :)", 'green')
                print()
                print(f'Your name: "{user_list[0][2]}" and the password hash is:"{user_list[0][4]}"')
                print(f"Your username: '{user_list[0][1]}' and the email address is: '{user_list[0][3]}'")
                print()
                exit()

        elif choice == '4':
            print("1.Delete entire table data\n2.Drop table\n3.Exit")
            print()
            ch = input("Enter: ")

            if ch == '1':
                cur.execute("DELETE from user")
                con.commit()
                print()
                cprint("Table's content deleted!", 'green')
            elif ch == '2':
                cur.execute("DROP TABLE user")
                con.commit()
                print()
                cprint("Table Droped!", 'green')
            elif ch == '3':
                print()
                print("Exiting program ..")
                time.sleep(.5)
                print("Exited!")
                exit()
            else:
                print("Wrong Choice!")
        else:
            cprint("Wrong Choice!", 'red')

if __name__ == "__main__":
    header()
    main()