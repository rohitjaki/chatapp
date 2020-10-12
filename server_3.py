import socket
import select
from datetime import date
from send_mail import *
from database_3 import *

PORT = 5002
SERVER = ""
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = 'disconnect'
b_format = 'UTF-8'
# temp_database = {'rohit': {'email': 'rohitsakar@gamil.com', 'name': 'deku', 'pheone': '99999999999'}}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def send(conn, mess):
    #alog side the length there will be the function name to interact with
    # print(len(mess))
    print('send')
    h = str({'header': '{:<10}'.format(len(str(mess)))})
    h = h.encode(b_format)
    # print(h)
    conn.send(h)
    mess = str(mess)
    mess = mess.encode(b_format)
    conn.send(mess)

def recieve(conn):
    #alog side the length there will be a the function id
    mssg = b''
    length = 24
    function_id=''
    print('recv')
    l = conn.recv(length)
    print(type(l)," ",l)
    mssgl = int(eval(l)['header'])
    if mssgl < length:
        mssg = conn.recv(mssgl)
        # mssg = mssg.decode(b_format)
        print( mssg)
        return eval(mssg)
    while True:
        l = conn.recv(length)
        mssg += l
        mssgl -= len(l)
        if mssgl <= length:
            mssg += conn.recv(mssgl)
            # mssg=mssg.decode(b_format)
            print(mssg)
            return eval(mssg)

def user_login(conn):
    while True:
        print('user is asking for login')
        auth_data = recieve(conn)
        #here is have to check is the user exist or not
        auth_data=auth_data
        print(auth_data)
        user=user_checker(auth_data['email'])
        if user == True:
            details=get_user_details(auth_data['email'])
            print(details)
            send(conn, 'True')
            send(conn,details)
            user_login = recieve(conn)
            if user_login == True:
                print('user is logined')
                break
        else:
            print('user doesnt exist')
            send(conn, 'False')

        #here recieve if the user is authenticated aor not



def user_registration(conn):
    while True:
        print('user is asking for registration')
        user_reg_data = recieve(conn)
        user_reg_data=user_reg_data
        print(user_reg_data)
        #chcek if the user exist or not
        user=user_checker(user_reg_data['email'])
        print(user)
        if user==False:
            code=send_mail(user_reg_data['email'])
            send(conn,code)
            while True:
                email_verified = recieve(conn)
                if email_verified==True:
                    break
            create_user(user_reg_data)
            send(conn,'True')
            # send(conn,code)
            break
        else:
            send(conn,'False')
    print('going out of the registration')

def client_authentication(conn):
    while True:
        user_choice=recieve(conn)
        if user_choice==1:
            user_login(conn)
        elif user_choice==2:
            user_registration(conn)
            user_login(conn)


def client_interact(conn, addr):
    print(f'from {addr} user connected ')
    client_authentication(conn)

def start():
    server.listen()
    print(server)
    while True:
        connected_conn, _, error_cc = select.select([server], [], [server])
        for i in connected_conn:
            conn, addr = server.accept()
            client_interact(conn, addr)


print('-----SERVER IS STARTING-----')
start()