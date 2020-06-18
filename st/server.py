import socket
from _thread import *
from player import Sit
import pickle
import time

server = '127.0.0.1'
port = 5557

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(20)
print("Waiting for a connection, Server Started")
dic = {}

def threaded_client(conn, player):
    code = pickle.loads(conn.recv(2048))
    print("ok")
    idx = 0
    if code in dic:
        idx = 1
        dic[code].stage = 1
    else:
        dic[code] = Sit()
    
    while True:
        time.sleep(0.3)
        conn.send(pickle.dumps(-1))
        if(dic[code].stage == 1):
            conn.send(pickle.dumps(0))
            break
    conn.send(0)
    sleep(0.3)
    conn.send(pickle.dumps(idx))

    bd = pickle.loads(conn.recv(2048))
    dic[code].stage += 1
    dic[code].board[idx] = bd
    while True:
        time.sleep(0.3)
        conn.send(pickle.dumps(-1))
        if(dic[code].stage == 3):
            conn.send(pickle.dumps(0))
            break
    conn.send(pickle.dumps(dic[code].board[1-idx]))
    win = 0
    while dic[code].stage != 6:
        if dic[code].stage == 3 and idx == 0:
            dic[code].step[idx] = pickle.loads(conn.recv(2048))
            dic[code].stage = 5
        elif dic[code].stage != (idx + 4):
            sleep(0.3)
            conn.send(pickle.dumps(-1))
        else:
            conn.send(pickle.dumps(0))
            conn.send(pickle.dumps(dic[code].step[1-idx]))
            dic[code].step[idx] = pickle.loads(conn.recv(2048))
            t = pickle.loads(conn.recv(2048))
            if t == 1:
                dic[code].stage = 6
                win = 1
            elif t == 2:
                dic[code].stage = 6
                win = 2
    if win == 0:
        conn.send(pickle.dumps(0))
        conn.send(pickle.dumps(dic[code].step[1-idx]))
        del dic[code]
 

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn ,currentPlayer))
    currentPlayer += 1