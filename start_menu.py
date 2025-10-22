import getpass
from db import get_connection

def password_check(password):
    point=0
    if len(password)>8:
        point+=1
    for char in password:
        if char.isupper():
            point+=1
            break
    for char in password:
        if char.islower():
            point+=1
            break
    for num in password:
        if num.isdigit():
            point+=1
            break
    return point

def input_user_pass():
    while True:
        print('-'*32)
        user_name=input('User name : ')
        password=getpass.getpass('Password : ')
        password2=getpass.getpass('Confirm password : ')
        if password != password2:
            print('-'*32)
            print('Passwords do not match.')
            print('-'*32)
            return False,False
        point=password_check(password)
        if point != 4:
            print('='*32)
            print('At least 8 characters\nContains uppercase and lowercase letters \nContains numbers')
            print('='*32)
            return False,False
        return user_name,password

def register():
    while True:
        user_name,password=input_user_pass()
        if user_name == False:
            break
        conn=get_connection()
        cur=conn.cursor()
        query="SELECT username FROM users WHERE username=%s"
        cur.execute(query,(user_name,))
        result=cur.fetchone()
        if result:
            print('-'*32)
            print('This username is available.')
            print('-'*32)
            conn.close()
            return False
        query2="INSERT INTO users (username,password) VALUES (%s,%s)"
        cur.execute(query2,(user_name,password))
        conn.commit()
        conn.close()
        print('-'*32)
        print(f'You are registered.')
        print('-'*32)
        break

def login():
    print('-'*32)
    user_name=input('User name : ')
    password=getpass.getpass('Password : ')
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT id,password FROM users WHERE username=%s"
    cur.execute(query,(user_name,))
    result=cur.fetchone()
    conn.close()
    if not result:
        print('-'*32)
        print('There is no username!')
        print('-'*32)
        return False,False
    if result[1] == password:
        return result[0],user_name
    else:
        print('-'*32)
        print('The password is incorrect!')
        print('-'*32)
        return False,False