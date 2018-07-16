# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 13:35:59 2018

@author: Zhou Renjie
"""

import sqlite3

def create_table(): 
    conn = sqlite3.connect('qns.db') #this connects to a database. If the database doesnt exist, it will create a new database and then connects to it from the second time onwards
    c = conn.cursor() #this is where the current cursor is at in the database
    c.execute("CREATE TABLE IF NOT EXISTS qns(id INTEGER PRIMARY KEY ASC, qn TEXT, op1 TEXT, op2 TEXT, op3 TEXT, op4 TEXT, hint1 TEXT, hint2 TEXT, hint3 TEXT, hint4 TEXT, correct_ans TEXT)") 
    #use SQL query language to create a database table called uname_psw
    #the CURSOR, c! does all the SQL queries
    
def data_entry(ID, QN, OP1, OP2, OP3, OP4, H1, H2, H3, H4, ANS):
    conn = sqlite3.connect('qns.db') #this connects to a database. If the database doesnt exist, it will create a new database and then connects to it from the second time onwards
    c = conn.cursor() #this is where the current cursor is at in the database
    c.execute("INSERT INTO qns (id, qn, op1, op2, op3, op4, hint1, hint2, hint3, hint4, correct_ans) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ID, QN, OP1, OP2, OP3, OP4, H1, H2, H3, H4, ANS)) #follow the same order as attributes when building the database table
    conn.commit() #always commit when making modifications, eg. inputing data
    c.close()
    conn.close()

def qn_retrieval(qnID):
    conn = sqlite3.connect('qns.db') #this connects to a database. If the database doesnt exist, it will create a new database and then connects to it from the second time onwards
    c = conn.cursor() #this is where the current cursor is at in the database
    #c.execute("SELECT * FROM qns WHERE id = ?", (qnID, )) #in SQL command, you can't just parse in a python variable
    c.execute("SELECT * FROM qns")
    one_question = c.fetchall()
    #print(one_question)
    c.close()
    conn.close()
    return one_question

def add_column():
    conn = sqlite3.connect('qns.db') #this connects to a database. If the database doesnt exist, it will create a new database and then connects to it from the second time onwards
    c = conn.cursor() #this is where the current cursor is at in the database
    c.execute("ALTER TABLE qns ADD COLUMN hint2 TEXT hint3 TEXT hint4 TEXT correct_ans TEXT")
    conn.commit()
    c.close()
    conn.close()    
    
def drop_table():
    conn = sqlite3.connect('qns.db') #this connects to a database. If the database doesnt exist, it will create a new database and then connects to it from the second time onwards
    c = conn.cursor()
    c.execute("DROP TABLE qns")
    c.close()
    conn.close()
    
#drop_table()  
#create_table()    
#data_entry(1, "asd", "a", "b", "c", "d")
#data_entry(1, "If Jenna has a dozen apples and she ate two-thirds of it, how many does she have left?", "3", "4", "8", "12","TMubSggUOVE","AsQ_uJDBrIU","9hZkk73nJ_Y","BiCUCqiWOlo","2")
#data_entry(2, "Jenna is twenty one years old now. If she was two-third zhilin’s age 19 years ago, how old is Zhilin now?", "3", "20", "22", "23","TMubSggUOVE","AsQ_uJDBrIU","9hZkk73nJ_Y","BiCUCqiWOlo","2" )
#data_entry(3, "If one apple and 2 pencils cost $1.10 and 2 apples and 1 pencil costs $2.05. Wht is the difference between the cost of an apple and a pencil?", "$0.05", "$0.10", "$0.95", "$1.05", "TMubSggUOVE","AsQ_uJDBrIU","9hZkk73nJ_Y","BiCUCqiWOlo","3")
#print(qn_retrieval(1))