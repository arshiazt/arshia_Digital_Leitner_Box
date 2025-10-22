from db import get_connection
import datetime
from random import shuffle
def show_box(user_id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT s.id,s.name,s.review_interval,COUNT(c.id) AS card_count" \
    " FROM slots s LEFT JOIN cards c ON s.id=c.slot_id" \
    " AND c.user_id=%s GROUP BY s.id,s.name ORDER BY s.id",(user_id,))
    rows=cur.fetchall()
    for i in rows:
        print('-'*80)
        if i[0] == 1:
            print(f'* ({i[1]} : cards in it must be reviewed everyday) | Number of Cards : {i[3]}')
        elif i[0] != 6:
            print(f'* ({i[1]} : cards in it must be reviewed every {i[2]} days) | Number of Cards : {i[3]}')
        else:
            print(f'* ({i[1]} : Learned cards!) | Number of Cards: {i[3]}')
    print('-'*80)    
    
    while True:
        choice=input('Do you want to see inside a specific slot? (Enter y ' \
        ' press any button to exit the show box) :').strip().lower()
        if choice=='y':
            try:
                slot_id=str(int(input('Slot id : ')))
            except:
                print('-'*32)
                print('Please enter number.')
                print('-'*32)
                continue
            cur.execute("SELECT id,question,answer,next_review " \
            " FROM cards WHERE user_id=%s AND slot_id=%s ORDER BY id",(user_id,slot_id))
            cards=cur.fetchall()
            if not cards:
                print('-'*32)
                print('There is no card.')
                print('-'*32)
            elif slot_id == '6':
                for card in cards:
                    print('-'*80)
                    card_id,question,answer,next_review=card
                    print(f'ID:{card_id} | Question:{question} | Answer:{answer} ')
                print('-'*80)
            else:
                for card in cards:
                    print('-'*80)
                    card_id,question,answer,next_review=card
                    print(f'ID:{card_id} | Question:{question} | Answer:{answer} | Next review:{next_review}')
                print('-'*80)
        else:
            break

def add_card(user_id):
    conn=get_connection()
    cur=conn.cursor()
    question=input('Question : ')
    answer=input('Answer : ')
    today=datetime.date.today()
    next_review=today
    query="INSERT INTO cards (user_id,question,answer,slot_id,last_review,next_review) VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(query,(user_id,question,answer,1,today,next_review))
    conn.commit()
    conn.close()
    print('-'*32)
    print('Card added successfully.')

def review_card(user_id,slot_id):
    today=datetime.datetime.today()
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT id,question,answer,slot_id FROM cards WHERE user_id=%s AND slot_id=%s AND next_review<=%s"
    cur.execute(query,(user_id,slot_id,today))
    cards=cur.fetchall()
    if not cards:
        print('-'*32)
        print('No cards to review today.')
        return
    shuffle(cards)
    for card in cards:
        print('-'*32)
        print(f'Question : {card[1]}')
        input('Press enter to see the answer ...')
        print(f'Answer : {card[2]}')
        learn=input('Did you learn it ? (Enter y) : ').lower()
        slot=card[3]
        day=[1,3,7,14,30,0]
        if learn=='y' and slot<6:
            new_slot=slot+1
        else:
            new_slot=slot
        next_review=today+datetime.timedelta(day[new_slot-1])
        conn=get_connection()
        cur=conn.cursor()
        query="UPDATE cards SET slot_id=%s,last_review=%s,next_review=%s WHERE id=%s"
        if next_review != today:
            cur.execute(query,(new_slot,today,next_review,card[0]))
        else:
            cur.execute(query,(new_slot,today,None,card[0]))
        conn.commit()
    conn.close()

def modify_card(user_id):
    conn=get_connection()
    cur=conn.cursor()
    print('-'*10+'Modify  Card'+'-'*10)
    while True:
        try:
            slot_id=int(input('Slot id : '))
            if not 0<slot_id<6:
                raise 
        except:
            print('The slot id must be a number between 1,2,3,4,5')
            continue
        query="SELECT id,question,answer FROM cards WHERE user_id=%s AND slot_id=%s ORDER BY id"
        cur.execute(query,(user_id,slot_id))
        cards=cur.fetchall()
        if not cards:
            print('-'*32)
            print('There is no card.')
            break
        for card in cards:
            print('-'*32)
            print(f'ID :{card[0]} | Question :{card[1]} | Answer :{card[2]}')
        print('-'*32)
        try:
            card_id=str(int(input("Card ID : ")))
        except:
            print('-'*32)
            print('Plaese enter number.')
            print('-'*32)
            continue
        query2="SELECT id,question,answer FROM cards WHERE id=%s AND user_id=%s AND slot_id=%s"
        cur.execute(query2,(card_id,user_id,slot_id))
        card=cur.fetchone()
        if not card:
            print('-'*32)
            print('No such card exists.')
            print('-'*32)
            continue
        print('-'*32)
        act=input('1)Delete 2)Edit : ')
        if act=='1':
            query3="DELETE FROM cards WHERE id=%s AND user_id=%s"
            cur.execute(query3,(card_id,user_id))
            print('-'*32)
            print(f'Card id : {card_id} ===> Delete.')
            conn.commit()
            conn.close()
            break
        elif act=='2':
            print('-'*32)
            print('Leave blank if you do not want to change.')
            new_q=input('Question : ').strip()
            new_a=input('Answer : ').strip()
            if new_a=='':
                new_a=card[2]
            if new_q=='':
                new_q=card[1]
            query4="UPDATE cards SET question=%s,answer=%s WHERE id=%s AND user_id=%s"
            cur.execute(query4,(new_q,new_a,card_id,user_id))
            print('-'*32)
            print(f'Card id : {card_id} ===> Changed.')
            conn.commit()
            conn.close()
            break
        else:
            print('-'*32)
            print('Please enter 1 or 2.')
            print('-'*32)
            continue
        conn.close()

def update_time_card(user_id):
    today=datetime.date.today()
    conn=get_connection()
    cur=conn.cursor()
    query="SELECT id,slot_id,next_review  FROM cards WHERE user_id=%s AND slot_id<6 AND next_review<%s - INTERVAL '2 days'"
    cur.execute(query,(user_id,today))
    result=cur.fetchall()
    if not result:
        return
    time={1:0,2:3,3:7,4:14,5:30}
    for i in result:
        card_id,slot_id,next_review=i
        if slot_id>1:
            new_slot_id=slot_id-1
        else:
            new_slot_id=slot_id
        next_review=today+datetime.timedelta(time[new_slot_id])
        cur.execute("UPDATE cards SET slot_id=%s,next_review=%s WHERE id=%s",(new_slot_id,next_review,card_id))
    conn.commit()
    conn.close()
