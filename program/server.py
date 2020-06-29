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
    while True:
        code = pickle.loads(conn.recv(2048))
        print("got code")
        print(code)
        if code == "disconnected":
            return
        print("ok")
        idx = 0
        if code in dic:
            idx = 1
            dic[code].stage = 1
        else:
            dic[code] = Sit()
        print(idx)
        while True:
            time.sleep(0.3)
            conn.send(pickle.dumps(-1))
            if(dic[code].stage == 1):
                break
        if dic[code].disconnect == 1:
            #conn.send(pickle.dumps('disconnect'))
            break
        conn.send(pickle.dumps(0))
        time.sleep(0.3)
        if dic[code].disconnect == 1:
            #conn.send(pickle.dumps('disconnect'))
            break
        conn.send(pickle.dumps(idx))

        bd = pickle.loads(conn.recv(2048))
        if bd == "disconnected":
            dic[code].disconnect = 1
            return
        dic[code].stage += 1
        dic[code].board[idx] = bd
        while True:
            time.sleep(0.3)
            if dic[code].disconnect == 1:
                conn.send(pickle.dumps('disconnect'))
                del dic[code]
                return
            conn.send(pickle.dumps(-1))
            if(dic[code].stage == 3):
                if dic[code].disconnect == 1:
                    conn.send(pickle.dumps('disconnect'))
                    del dic[code]
                    return
                conn.send(pickle.dumps(0))
                break
        time.sleep(0.3)
        if dic[code].disconnect == 1:
            conn.send(pickle.dumps('disconnect'))
            del dic[code]
            return
        conn.send(pickle.dumps(dic[code].board[1-idx]))
        win = 0
        while dic[code].stage != 6:
            if dic[code].disconnect == 1:
                #conn.send(pickle.dumps('disconnect'))
                break
            time.sleep(0.3)
            if dic[code].stage == 3 and idx == 0:
                temp = pickle.loads(conn.recv(2048))
                if temp == "disconnected" or temp == 'finished':
                    win = 1
                    dic[code].disconnect = 1
                    break
                dic[code].board[idx] = temp
                dic[code].stage = 5
            elif dic[code].stage != (idx + 4):
                if dic[code].disconnect == 1:
                    #conn.send(pickle.dumps('disconnect'))
                    break
                conn.send(pickle.dumps(-1))
            else:
                if dic[code].disconnect == 1:
                    #conn.send(pickle.dumps('disconnect'))
                    break
                conn.send(pickle.dumps(0))
                time.sleep(0.3)
                if dic[code].disconnect == 1:
                    #conn.send(pickle.dumps('disconnect'))
                    break
                conn.send(pickle.dumps(dic[code].board[1-idx]))
                temp = pickle.loads(conn.recv(2048))
                if temp == "disconnected" or temp == 'finished':
                    win = 1
                    dic[code].disconnect = 1
                    break
                dic[code].board[idx] = temp
                # t = pickle.loads(conn.recv(2048))
                t = 0
                if t == 1:
                    dic[code].stage = 6
                    win = 1
                elif t == 2:
                    dic[code].stage = 6
                    win = 2
                else:
                    dic[code].stage = 9 - dic[code].stage
        """if win == 0:
            conn.send(pickle.dumps(0))
            time.sleep(0.3)
            if code not in dic:
                break
            conn.send(pickle.dumps(dic[code].board[1-idx]))"""
        if win == 0:
            del dic[code]


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn ,currentPlayer))
    currentPlayer += 1