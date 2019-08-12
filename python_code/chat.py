import socket
import select
import errno
import sys      
import os
import threading
import time


# below is the client of chat.

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
console_line_content = []


my_username = input("Username: ")
console_line_content.append("Name: " + my_username + ", Here is my chat console.")
os.system('clear')
for line in console_line_content:
    print(line)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)


def receive_thing():
    while True:
        try:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")
            content_show = f"{username} >>> {message}"
            print('', end='\r')
            print(content_show, end='\r\n')

        except IOError as e:
            if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
                print('reading error', str(e))
                sys.exit()
            else:
                # check the server information every 1 second.
                time.sleep(1)
        except Exception as e:
            print("General error", str(e))
            #sys.exit()

threading.Thread(target=receive_thing).start()

while True:
    message = input(my_username + " > ")    
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
        #print(f"{my_username} > {message}" + " (sended) ")


