import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import sqlite3

conn = sqlite3.connect('store.db')                 #DATABASE CREATION      
c = conn.cursor()
c.execute('DELETE FROM bill')

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS bill(name TEXT, price REAL)") #TABLE CREATION
def scan():
    l=[]
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN

    while True:
        _, frame = cap.read()

        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            #print("Data ->", obj.data)
            cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                        (255, 0, 0), 3)
            a=str(obj.data)         
            l.append(a)          
            
        cv2.imshow("SCAN HERE", frame)

        key = cv2.waitKey(1)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            cap.release()
    	    break
    return list(set(l))
def ins(l):                                                                 #TABLE INSERTION
    for i in l:
        c.execute('SELECT price FROM inv WHERE name=?', (i,))
        b = c.fetchall()
        b=b[0][0]
        c.execute("INSERT INTO bill (name,price) VALUES (?, ?)",(i,b))
        
    conn.commit()
def bill(l):                                                             #BILL CREATION
    sum=0
    p=len(l)
    for i in l:
        c.execute('SELECT price FROM bill WHERE name=?', (i,))
        b = c.fetchall()
        b=b[0][0]
        sum=sum+b
    print("**************************BILL*************************\n")
    print("SR no.     ITEM  |  PRICE\n")
    for i in l:
        c.execute('SELECT price FROM inv WHERE name=?', (i,))
        b = c.fetchall()
        b=b[0][0]
        print(str(p)+"     "+i+"  | "+str(b)+"\n")
        p=p-1
    print("\n\n Your Total is :"+ str(sum))    
    print("\n*******************************************************")    
create_table()            
l=scan()
ins(l)
bill(l)
cv2.destroyAllWindows()
