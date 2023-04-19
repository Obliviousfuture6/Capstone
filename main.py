import bcrypt
from datetime import datetime,date
import sqlite3
import csv

salt = bcrypt.gensalt()
connection = sqlite3.connect("Competency_db.db")
cursor = connection.cursor()

with open("schema.sql") as my_queries:
    queries = my_queries.read()

cursor.executescript(queries)


def add_user():
    print("\n ### New User ###\nfill out the form below:\n")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    password = input("Password: ")
    bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(bytes,salt)
    user_type = int(input("User Type (manager(0)/user(1)): "))
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = 'INSERT INTO Users (first_name, last_name, phone, email, password, date_created, user_type) values (?,?,?,?,?,?,?)'
    cursor.execute(query, (first_name,last_name,phone,email,hashed_password, date_created, user_type))
    connection.commit()
    print(f'{first_name} has been added to Users')


def add_competency():
    name = input("\n Enter Competency name: ")
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = 'INSERT INTO Competencies (name, date_created) values (?,?)'
    cursor.execute(query, (name,date_created))
    connection.commit()
    print(f'{name} has been added to Competencies')


def add_assessment():
    name = input("\nEnter Assessment name: ")
    view_data('competencies')
    competency_id = input("Enter Competency ID: ")
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = 'INSERT INTO Assessments (competency_id, name, date_created) values (?,?,?)'
    cursor.execute(query, (competency_id, name, date_created))
    connection.commit()
    print(f'{name} has been added to Assessments')


def add_results():
    print("\n ### Assessment Results ###\nfill out the form below:\n")
    view_data('all users')
    user = input("User ID: ")
    view_data('assessments')
    assessment = input("Assessment ID: ")
    score = input("Score (0-4): ")
    print("Enter date taken:\n")
    year = int(input('Enter a year: '))
    month = int(input('Enter a month: '))
    day = int(input('Enter a day: '))
    date_taken = date(year, month, day)
    view_data('all managers')
    manager = input("Manager ID: ")
    query = 'INSERT INTO Assessment_Resulsts (user_id, assessment_id, score, date_taken, manager_id) values (?,?,?,?,?)'
    cursor.execute(query, (user, assessment, score, date_taken, manager))
    connection.commit()
    print(f'Assessment Result has been Added')
    

def data_check(table, value):
    if table == 'Users':
        query = 'SELECT * FROM Users WHERE user_id = ?'     
        check = cursor.execute(query, (value,)).fetchall()
        return check
    if table == 'Competencies':
        query = 'SELECT * FROM Competencies WHERE competency_id = ?'
        check = cursor.execute(query, (value,)).fetchall()
        return check
    if table == 'Assessments':
        query = 'SELECT * FROM Assessments WHERE assessment_id = ?'
        check = cursor.execute(query, (value,)).fetchall()
        return check
    if table == 'Results':
        query = 'SELECT * FROM Assessment_Results WHERE result_id = ?'
        check = cursor.execute(query, (value,)).fetchall()
        return check
    

def remove_data(data,table,id,type_str):
    confirm = input(f"\nAre you SURE you want to permanently DELETE this {type_str} (Y/N)?\n>>> ")
    if confirm.upper() == "Y":
        delete = f'DELETE FROM {table} WHERE {id} = ?'
        cursor.execute(delete, (data,))
        connection.commit()
        print(f"\n{type_str} successfully deleted\n")


def user_edit_user(user_name):
    option_list = ["first name", "last name", "phone", "email", "password"]
    while True:
        option =  input("\nWhat would you like to do?\n(1)Edit first name\n(2)Edit last name\n(3)Edit phone number\n(4)Edit email\n(5)Edit password\n(Press 'Enter' to return to main menu)\n>>>")
        try:
            option = int(option)
        except:
            print("invalid input")
            continue
        if option == "":
            return
        query_update = "UPDATE Users SET first_name=? WHERE email=?" if option == 1 else ""
        query_update = "UPDATE Users SET last_name=? WHERE email=?" if option == 2 else query_update
        query_update = "UPDATE Users SET phone=? WHERE email=?" if option == 3 else query_update
        query_update = "UPDATE Users SET email=? WHERE email=?" if option == 4 else query_update
        query_update = "UPDATE Users SET password=? WHERE email=?" if option == 5 else query_update
        if query_update == "":
            print("Please input valid response")
            continue
        new_field = input(f"\nEnter new {option_list[(option-1)]}: ")
        if option == 5:
            bytes = new_field.encode('utf-8')
            new_field = bcrypt.hashpw(bytes,salt)
        cursor.execute(query_update, (new_field, user_name))
        connection.commit()
        break


def manager_edit_user():
    user = input("Enter the User ID for the user you'd like to edit/remove (Press 'Enter' to return to Main Menu)\n>>>")
    if not data_check('Users',user):
        print("invalid ID")
        return
    option_list = ["first name", "last name", "phone", "email", "active status", "hire date", "user type"]
    if user == "":
        return
    while True:
        option =  input("\nWhat would you like to do?\n(1)Edit first name\n(2)Edit last name\n(3)Edit phone number\n(4)Edit email\n(5)Edit active status\n(6)Edit hire date\n(7)Edit user type\n(8)Remove User\n>>>")
        try:
            option = int(option)
        except:
            print("invalid input")
            continue
        if option == 8:
            remove_data(user,"Users","user_id","User")
            return
        if option == 7:
            print("0 = admin \n1 = user")
        query_update = "UPDATE Users SET first_name=? WHERE user_id=?" if option == 1 else ""
        query_update = "UPDATE Users SET last_name=? WHERE user_id=?" if option == 2 else query_update
        query_update = "UPDATE Users SET phone=? WHERE user_id=?" if option == 3 else query_update
        query_update = "UPDATE Users SET email=? WHERE user_id=?" if option == 4 else query_update
        query_update = "UPDATE Users SET active=? WHERE user_id=?" if option == 5 else query_update
        query_update = "UPDATE Users SET hire_date=? WHERE user_id=?" if option == 6 else query_update
        query_update = "UPDATE Users SET user_type=? WHERE user_id=?" if option == 7 else query_update
        if query_update == "":
            print("Please input valid response")
            continue
        new_field = input(f"\nEnter new {option_list[(option-1)]}: ")
        cursor.execute(query_update, (new_field, user))
        connection.commit()
        break


def edit_competency():
    competency = input("Enter the Competency ID for the Competency you'd like to edit/remove (Press 'Enter' to return to Main Menu)\n>>>")
    if not data_check('Competencies',competency):
        print("invalid ID")
        return
    if competency == "":
        return
    while True:
        option = input("\nWhat would you like to do?\n(1)Change Competency name\n(2)Remove Competency\n>>>")
        try:
            option = int(option)
        except:
            print("invalid input")
            continue
        if  option == 1:
            new_name = input("\nEnter new Competency name: ")
            query = "UPDATE Competencies SET name=? WHERE competency_id=?"
            cursor.execute(query, (new_name,competency))
            connection.commit()
            break
        if option == 2:
            remove_data(competency,"Competencies","competency_id","Competency")
            break
        else:
            print("Please Enter valid input")


def edit_assessment():
    assessment = input("Enter the Assessment ID for the Assessment you'd like to edit/remove (Press 'Enter' to return to Main Menu)\n>>>")
    if not data_check('Assessments',assessment):
        print("invalid ID")
        return
    if assessment == "":
        return
    while True:
        option = input("\nWhat would you like to do?\n(1)Change Assessment name\n(2)Remove Assessment\n>>>")
        try:
            option = int(option)
        except:
            print("invalid input")
            continue
        if  option == 1:
            new_name = input("\nEnter new Assessment name: ")
            query = "UPDATE Assessments SET name=? WHERE assessment_id=?"
            cursor.execute(query, (new_name,assessment))
            connection.commit()
            break
        if option == 2:
            remove_data(assessment,"Assessments","assessment_id","Assessment")
            break
        else:
            print("Please Enter valid input")


def edit_results():
    result = input("Enter the Result ID for the Assessment Result you'd like to edit/remove (Press 'Enter' to return to Main Menu)\n>>>")
    if not data_check('Results',result):
        print("invalid ID")
        return
    if result == "":
        return
    while True:
        option = input("\nWhat would you like to do?\n(1)Edit Score\n(2)Edit date taken\n(3)Remove Assessment Results")
        try:
            option = int(option)
        except:
            print("invalid input")
            continue
        if  option == 1:
            new_score = input("\nEnter new Score: ")
            query = "UPDATE Assessment_Results SET score=? WHERE result_id=?"
            cursor.execute(query, (new_score,result))
            connection.commit()
            break
        if option == 2:
            year = int(input('Enter a year: '))
            month = int(input('Enter a month: '))
            day = int(input('Enter a day: '))
            date_taken = date(year, month, day)
            query = "UPDATE Assessment_Results SET date_taken=? WHERE result_id=?"
            cursor.execute(query, (date_taken,result))
        if option == 3:
            remove_data(result,"Assessment_Results", "result_id", "Assessment Result")
            break
        else:
            print("Please Enter valid input")


def view_data(key,username=None,ID=None):
    if key == 'all users':
        rows = cursor.execute('SELECT * FROM Users').fetchall()
        print(f'\n{"User ID":9}{"First Name":15}{"Last Name":15}{"Phone":12}{"Email":30}{"Active":8}{"Date Created":21}{"Hire Date":20}{"User Type"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:9}{row[1]:15}{row[2]:15}{row[3]:12}{row[4]:30}{row[6]:8}{row[7]:21}{row[8]:20}{row[9]}')
    
    if key == 'users search':
        while True:
            option = input("Search by:\n(1)First Name\n(2)Last Name\n>>")
            if option == "1":
                search = input("First Name: ")
                query = 'SELECT * FROM Users WHERE first_name LIKE ?'
                break
            if option == "2":
                search = input("Enter Last Name")
                query = 'SELECT * FROM Users WHERE last_name LIKE ?'
                break
            else:
                print("invalid input")
        rows = cursor.execute(query, (f'%{search}%',)).fetchall()
        print(f'\n{"User ID":9}{"First Name":15}{"Last Name":15}{"Phone":12}{"Email":30}{"Active":8}{"Date Created":21}{"Hire Date":20}{"User Type"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:9}{row[1]:15}{row[2]:15}{row[3]:12}{row[4]:30}{row[6]:8}{row[7]:21}{row[8]:20}{row[9]}')
    if key == 'all managers':
        rows = cursor.execute('SELECT * FROM Users WHERE user_type = 0').fetchall()
        print(f'\n{"User ID":9}{"First Name":15}{"Last Name":15}{"Phone":12}{"Email":30}{"Active":8}{"Date Created":21}{"Hire Date":20}{"User Type"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:9}{row[1]:15}{row[2]:15}{row[3]:12}{row[4]:30}{row[6]:8}{row[7]:21}{row[8]:20}{row[9]}')
    
    if key == 'competencies':
        rows = cursor.execute('SELECT * FROM Competencies').fetchall()
        print(f'\n{"Competency ID":15}{"Name":30}{"Date Created"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:15}{row[1]:30}{row[2]}')
    
    if key== 'assessments':
        rows = cursor.execute('SELECT * FROM Assessments').fetchall()
        print(f'\n{"Assessment ID":15}{"Competency ID":15}{"Name":30}{"Date Created"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:15}{row[1]:15}{row[2]:30}{row[3]}')
    
    if key == 'all results':
        rows = cursor.execute('SELECT * FROM Assessment_Results').fetchall()
        print(f'\n{"Result ID":11}{"User ID":9}{"Assessment ID":15}{"score":7}{"Date Taken":20}{"Manager ID"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:11}{row[1]:9}{row[2]:15}{row[3]:7}{row[4]:20}{row[5]}')
    
    if key == 'single user':
        print("\n+++ User Info +++")
        query = 'SELECT * FROM Users WHERE email=?'
        rows = cursor.execute(query, (username,)).fetchall()
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{"User ID:":15}{row[0]}\n{"First Name:":15}{row[1]}\n{"Last Name:":15}{row[2]}\n{"Phone:":15}{row[3]}\n{"Email:":15}{row[4]}\n{"Active:":15}{row[6]}\n{"Date Created:":15}{row[7]}\n{"Hire Date:":15}{row[8]}\n{"User Type: ":15}{row[9]}')
    
    if key == 'assessment history':
        query = 'SELECT * FROM Assessment_Results WHERE user_id = ?'
        rows = cursor.execute(query, (ID,)).fetchall()
        print(f'\n{"Result ID":11}{"User ID":9}{"Assessment ID":15}{"Score":7}{"Date Taken":20}{"Manager ID"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:11}{row[1]:9}{row[2]:15}{row[3]:7}{row[4]:20}{row[5]}')
    
    if key == 'single user competency':
        sum = 0
        count = 0
        query = '''
        SELECT c.name, score, u.first_name, u.last_name, u.email FROM Assessment_Results
        JOIN Assessments ON Assessment_Results.assessment_id = Assessments.assessment_id
        JOIN Competencies c ON Assessments.competency_id = c.competency_id
        JOIN Users u ON Assessment_Results.user_id = u.user_id
        WHERE u.user_id = ?
        GROUP BY Assessment_Results.user_id, Assessment_Results.assessment_id
        ORDER BY MAX(date_taken)'''
        rows = cursor.execute(query, (ID,)).fetchall()
        print(f'\n{"Competency Name":30}{"Score":7}{"First Name":15}{"Last Name":15}{"Email"}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:30}{row[1]:7}{row[2]:15}{row[3]:15}{row[4]}')
            sum += int(row[1])
            count += 1
        print(f'\n{"Average Competency Score:":30}{sum/count}')
    
    if key == 'all user result':
        sum = 0
        count = 0
        query = '''
        SELECT c.name, u.first_name, u.last_name, score, Assessments.Name, date_taken FROM Assessment_Results
        JOIN Assessments ON Assessment_Results.assessment_id = Assessments.assessment_id
        JOIN Competencies c ON Assessments.competency_id = c.competency_id
        JOIN Users u ON Assessment_Results.user_id = u.user_id
        WHERE c.competency_id = ?
        GROUP BY Assessment_Results.user_id, Assessment_Results.assessment_id
        ORDER BY MAX(date_taken)'''
        rows = cursor.execute(query, (ID,)).fetchall()
        print(f'\n{"Competency Name":30}{"First Name":15}{"Last Name":15}{"Score":7}{"Assessment Name":30}{"Date Taken":20}')
        for row in rows:
            row = [(str(i) if i or i == 0 else "None") for i in row]
            print(f'{row[0]:30}{row[1]:15}{row[2]:15}{row[3]:7}{row[4]:30}{row[5]:20}')
            count += 1
            sum += int(row[3])
        print(f'\n{"Average Competency Score:":30}{sum/count}')
        

def import_csv():
    with open ('import.csv', 'r') as f:
        reader = csv.reader(f)
        columns = next(reader) 
        query = 'INSERT INTO Assessment_Results({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))
        for data in reader:
            cursor.execute(query, data)
        connection.commit()
        print("Successfully imported data")


def export_csv():
    export = input("What would you like to export?\n(1)User List\n(2)Competency List\n>>>")
    if export.upper() == "1":
        fields = ['user_id','first_name','last_name','phone','email','active','date_created','hire_date','user_type']
        with open('export.csv', 'w', newline='') as f:
            wrt = csv.writer(f)
            wrt.writerow(fields)
            rows = cursor.execute('SELECT * FROM Users').fetchall()
            for row in rows:
                row = [(str(i) if i or i == 0 else "None") for i in row]
                wrt.writerow([row[0],row[1],row[2],row[3],row[4],row[6],row[7],row[8],row[9]])
        print("Succesfully exported User List")
    elif export.upper() == "2":
        fields = ['competency_id','name','date_created']
        with open('export.csv', 'w', newline='') as f:
            wrt = csv.writer(f)
            rows = cursor.execute('SELECT * FROM Competencies').fetchall()
            for row in rows:
                row = [(str(i) if i or i == 0 else "None") for i in row]
                wrt.writerow([row[0],row[1],row[2]])

        print("Succesfully exported Competency List")



def user_menu(username):
    query = "SELECT user_id FROM Users where email = ?"
    get_user_id = cursor.execute(query, (username,)).fetchone()
    user_id = get_user_id[0]
    while True:
        menu = input("\n+++ User Menu +++\n(1)View User Info\n(2)Edit User Info\n(3)View Assessment History\n(4)View Competency\n(5)Quit\n>>>")
        if menu == "1":
            view_data("single user", username)
        elif menu == "2":
            user_edit_user(username)
        elif menu == "3":
            view_data('assessment history', ID=user_id)
        elif menu == "4":
            view_data('single user competency',ID=user_id)
        elif menu == "5":
            print("Goodbye!")
            break


def manager_menu(username):
    while True:
        menu = input("\n+++ Manager Menu +++\n(1)View all users\n(2)View Users (Search)\n(3)View report of all users for Competency\n(4)View Competency level report for individual\n(5)view Assessment History for individual\n(6)Add User/Competency/Assessment/Assessment result\n(7)Edit User/Competency/Assessment/Assessment\n(8)Import Assessment Data\n(9)Export User List or Competency List\n(10)Quit\n>>>")
        if menu == "1":
            view_data("all users")
        elif menu == "2":
            view_data("users search")
        elif menu == "3":
            view_data("competencies")
            competency_id = input("Enter Competency ID: ")
            view_data('all user result', ID=competency_id)
        elif menu == "4":
            view_data("all users")
            user_id = input("Enter user ID: ")
            view_data("single user competency", ID=user_id)
        elif menu == "5":
            view_data("all users")
            user_id = input("Enter user ID: ")
            view_data("assessment history", ID=user_id)
        elif menu == "6":
            while True:
                menu = input("\nWhat would you like to add?\n\n(1)Add User\n(2)Add Competency\n(3)Add Assessment\n(4)Add Assessment Result\n(Press 'Enter' to return)\n>>>")
                if menu == "":
                    break
                if menu == "1":
                    add_user()
                    break
                elif menu == "2":
                    add_competency()
                    break
                elif menu == "3":
                    add_assessment()
                elif menu == "4":
                    add_results()
        elif menu == "7":
            while True:
                menu = input("\nWhat would you like to edit?\n(0)Edit Own User\n(1)Edit User\n(2)Edit Competency\n(3)Edit Assessment\n(4)Edit Assessment Result\n(Press 'Enter' to return)\n>>>")
                if menu == "":
                    break
                if menu == "0":
                    user_edit_user(username)
                if menu == "1":
                    view_data("all users")
                    manager_edit_user()
                    break
                elif menu == "2":
                    view_data("competencies")
                    edit_competency()
                    break
                elif menu == "3":
                    view_data("assessments")
                    edit_assessment()
                elif menu == "4":
                    view_data("all results")
                    edit_results()
        elif menu == "8":
            import_csv()
        elif menu == "9":
            export_csv()
        elif menu == "10":
            print("Goodbye")
            break
        else:
            print("invalid input")


def login():
    while True:
        login = input("+++Competency Program+++\n(1)Log in\n(2)Quit\n>>>")
        if login == "2":
            print("Goodbye!")
            break
        if login == "1":
            username = input("Username (email): ")
            query = "SELECT password FROM Users WHERE email=? and Active = 1"
            pass_check = cursor.execute(query, (username,)).fetchone()
            password = input("Password : ")
            bytes = password.encode('utf-8')
            if bcrypt.checkpw(bytes,pass_check[0]):
                query = "SELECT user_type FROM Users WHERE email =?"
                user_type = cursor.execute(query, (username,)).fetchone()
                if user_type[0] == 0:
                    manager_menu(username)
                if user_type[0] == 1:
                    user_menu(username)
            else:
                print("Incorrect password or username")
        else:
            print("invalid input")


if not cursor.execute("SELECT * FROM Users").fetchall():
    add_user()
login()