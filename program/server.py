import socket
from _thread import *
from player import Sit
import pickle
import time

server = '127.0.0.1'
#server = '210.71.78.200'
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
        dc = 0
        try:
            code = pickle.loads(conn.recv(2048))
        except:
            return
        print("code")
        print(code)
        idx = 0
        if code in dic:
            idx = 1
            dic[code].stage = 1
        else:
            dic[code] = Sit()
        while True:
            time.sleep(0.3)
            if(dic[code].stage == 1):
                break
            try:
                conn.send(pickle.dumps(-1))
            except:
                del dic[code]
                return
        if dic[code].duan == 1:
            try:
                conn.send(pickle.dumps('disconnected'))
            except:
                print('888')
            del dic[code]
            continue
            
        try:
            conn.send(pickle.dumps(0))
        except:
            if dic[code].duan == 1:
                del dic[code]
            else:
                dic[code].duan = 1
            return
        time.sleep(0.3)
        if dic[code].duan == 1:
            try:
                conn.send(pickle.dumps('disconnected'))
            except:
                print('888')
            del dic[code]
            continue
        try:
            conn.send(pickle.dumps(idx))
        except:
            if dic[code].duan == 1:
                del dic[code]
            else:
                dic[code].duan = 1
            return
        try:
            bd = pickle.loads(conn.recv(2048))
        except:
            if dic[code].duan == 1:
                del dic[code]
            else:
                dic[code].duan = 1
            return
        dic[code].stage += 1
        dic[code].board[idx] = bd
        while True:
            time.sleep(0.3)
            if dic[code].duan == 1:
                try:
                    conn.send(pickle.dumps('disconnected'))
                except:
                    print('888')
                del dic[code]
                dc = 1
                break
            try:
                conn.send(pickle.dumps(-1))
            except:
                if dic[code].duan == 1:
                    del dic[code]
                else:
                    dic[code].duan = 1
                return
            if(dic[code].stage == 3):
                if dic[code].duan == 1:
                    try:
                        conn.send(pickle.dumps('disconnected'))
                    except:
                        print('888')
                    del dic[code]
                    dc = 1
                    break
                try:
                    conn.send(pickle.dumps(0))
                except:
                    if dic[code].duan == 1:
                        del dic[code]
                    else:
                        dic[code].duan = 1
                    return
                break
        time.sleep(0.3)
        if dc == 1:
            continue
        if dic[code].duan == 1:
            try:
                conn.send(pickle.dumps('disconnected'))
            except:
                print('888')
            del dic[code]
            continue
        try:
            conn.send(pickle.dumps(dic[code].board[1-idx]))
        except:
            if dic[code].duan == 1:
                del dic[code]
            else:
                dic[code].duan = 1
            return
        win = 0
        while dic[code].stage != 6:
            if dic[code].disconnect == 1:
                break
            time.sleep(0.3)
            if dic[code].stage == 3 and idx == 0:
                try:
                    temp = pickle.loads(conn.recv(2048))
                except:
                    if dic[code].duan == 1:
                        del dic[code]
                    else:
                        dic[code].duan = 1
                    return
                if temp == 'finished':
                    win = 1
                    dic[code].disconnect = 1
                    break
                dic[code].board[idx] = temp
                dic[code].stage = 5
            elif dic[code].stage != (idx + 4):
                if dic[code].disconnect == 1:
                    #conn.send(pickle.dumps('disconnect'))
                    break
                if dic[code].duan == 1:
                    try:
                        conn.send(pickle.dumps('disconnected'))
                    except:
                        print('888')
                    
                    del dic[code]
                    dc = 1
                    break
                try:
                    conn.send(pickle.dumps(-1))
                except:
                    if dic[code].duan == 1:
                        del dic[code]
                    else:
                        dic[code].duan = 1
                    return
            else:
                if dic[code].disconnect == 1:
                    #conn.send(pickle.dumps('disconnect'))
                    break
                if dic[code].duan == 1:
                    try:
                        conn.send(pickle.dumps('disconnected'))
                    except:
                        print('888')
                    del dic[code]
                    dc = 1
                    break
                try:
                    conn.send(pickle.dumps(0))
                except:
                    if dic[code].duan == 1:
                        del dic[code]
                    else:
                        dic[code].duan = 1
                    return
                time.sleep(0.3)
                if dic[code].disconnect == 1:
                    #conn.send(pickle.dumps('disconnect'))
                    break
                if dic[code].duan == 1:
                    try:
                        conn.send(pickle.dumps('disconnected'))
                    except:
                        print('888')
                    del dic[code]
                    dc = 1
                    break
                try:
                    conn.send(pickle.dumps(dic[code].board[1-idx]))
                    temp = pickle.loads(conn.recv(2048))
                except:
                    if dic[code].duan == 1:
                        del dic[code]
                    else:
                        dic[code].duan = 1
                    return
                if temp == 'finished':
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
        if dc == 1:
            continue
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