import socket
import select


HEADER_LENGTH = 10
IP = "0.0.0.0"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP,PORT))

server_socket.listen()

sockets_list = [server_socket]

name_map = dict()

clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            print(500)
            return False

        message_length = int(message_header.decode("utf-8").strip())
        message = client_socket.recv(message_length).decode("utf-8")
        print("***  " + message)
        return message

    except Exception as e:
        print(e)
        return ""

while True:
    read_sockets, _, except_socket = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        current_client = notified_socket
        if notified_socket is server_socket:
            # new user come in
            current_client, address = notified_socket.accept()
            sockets_list.append(current_client)
            msg = receive_message(current_client)
            name_map[current_client] = msg
            continue
        message = receive_message(current_client)
        if not message:
            continue
        message = message.encode('utf-8')
        for socket_ in sockets_list:
            if socket_ is not current_client and socket_ is not server_socket:
                name = name_map[current_client]
                print(f"{name} > {message}")
                name = name.encode('utf-8')
                encode_name = f"{len(name) :< {HEADER_LENGTH}}".encode("utf-8") + name
                encode_content = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8") + message
                socket_.send(encode_name + encode_content)
