from db import create_database,create_tables
from start_menu import register,login
from dashboard_user import show_box,add_card,review_card,modify_card,update_time_card
import os
from time import sleep

def clear():
    if os.name=='nt':
        os.system("cls")
    else:
        os.system("clear")

def start():
    while True:
        clear()
        print('='*10+' Start Menu '+'='*10)
        print('1) Register\n2) Login\n3) Exit')
        choice=input('Enter your choice : ')
        if choice == '1':
            reg=register()
            if reg == False:
                sleep(1.5)
                continue
            sleep(1.5)
        elif choice == '2':
            user_id,user_name=login()
            if user_id == False:
                sleep(1.5)
                continue
            return user_id,user_name
        elif choice == '3':
            clear()
            print('Good bye my friend!')
            sleep(1.5)
            clear()
            return False,False
        else:
            print('-'*32)
            print('Please enter correct number.')
            print('-'*32)
            sleep(1.5)

def main():
    clear()
    create_database()
    create_tables()
    sleep(1.5)
    while True:
        clear()
        user_id,user_name=start()
        if user_id == False:
            break
        print('-'*32)
        print(f'Welcome my friend {user_name}')
        print('-'*32)
        sleep(1.5)
        clear()
        count=0
        while True:
            count+=1
            if count == 3:
                print('-'*32)
                c=input('Do you want to clear terminal(y) : ').lower()
                if c == 'y':
                    count=1
                    clear()
            update_time_card(user_id)
            print('-'*32)
            print('1) Show Box\n2) Add Card\n3) Modify Card\n4) Review Cards\n5) Logout')
            choice=input('Enter your choice : ')
            if choice == '1':
                show_box(user_id)
            elif choice == '2':
                add_card(user_id)
            elif choice == '3':
                modify_card(user_id)
            elif choice == '4':
                try:
                    slot_id=int(input('Slot id : '))
                    if slot_id>5:
                        raise
                except:
                    print('-'*32)
                    print('Please enter number(1,2,3,4,5).')
                    continue
                review_card(user_id,slot_id)
            elif choice == '5':
                clear()
                print(f'Thank you,{user_name} for using our application')
                sleep(1.5)
                break
            else:
                print('-'*32)
                print('Please enter correct number.')
                print('-'*32)
                sleep(2)
                clear()

if __name__ == "__main__": 
    main()