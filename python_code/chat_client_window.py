import socket
import sys
import errno


# python 3.6+

class ChatClient:
    def __init__(self, server_ip='127.0.0.1', server_port=1234):
        self.server_port = server_port
        self.server_ip = server_ip
        self.header_length = 10
        self.console_line_content = []
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        '''
        start the client
        1,set server config
        2,connect server
        3,set user informaiton
        4,start the dialog with other clients
        '''
        while True:
            self._start_page()
            try:
                self.client_socket.connect((self.server_ip, int(self.server_port)))
                self.client_socket.setblocking(False)
            except Exception:
                print('Can not connect the server you just pointed. Please set the IP and PORT of server again.')
                continue
            else:
                break
        print('Connection is established, Please finish your information!')
        self._set_user_info()
        self._start_dialog_loop()

    def _start_page(self):
        '''
        welocome page for input the information of server
        '''
        ip = input('Please input the IP of chat server : ')
        port = input('Please input the PORT of chat server : ')
        self.server_ip = ip if ip else self.server_ip
        self.server_port = port if port else self.server_port
        # TODO: check the server_ip and server_port.

    def _set_user_info(self):
        self.username = input("Username: ")
        print("Name: " + self.username + ", Here is my chat console.")
        self._send_message_to_server(self.username)

    def _send_message_to_server(self, content):
        content = content.encode('utf-8')
        connect_header = f"{len(content):<{self.header_length}}".encode("utf-8")
        # send user info to server
        self.client_socket.send(connect_header + content)

    def _start_dialog_loop(self):
        '''
        start a dialog with other clients.
        '''
        while True:
            my_input = input(f"{self.username} > ")
            self._send_message_to_server(my_input)
            print(12)
            self._receive_thread()
            print(34)

    def _receive_thread(self):
        messages = self.receive_messages()
        for message in messages:
            print(message)

    def _print_before_last_line(self, messages):
        '''
        print the messages before the last line.
        :param messages:
        :return:
        '''


    def receive_messages(self):
        '''
        receive messages from sever.
        :return:
        '''
        messages = []
        try:
            # in the loop, check all the messages from server.
            while True:
                username_header = self.client_socket.recv(self.header_length)
                if not len(username_header):
                    print("connection closed by the server")
                    sys.exit()
                username_length = int(username_header.decode("utf-8").strip())
                username = self.client_socket.recv(username_length).decode("utf-8")
                message_header = self.client_socket.recv(self.header_length)
                message_length = int(message_header.decode("utf-8").strip())
                message = self.client_socket.recv(message_length).decode("utf-8")
                messages.append(f"{username} >>> {message}")

        except IOError as e:
            if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
                print('reading error', str(e))
                sys.exit()
            else:
                return messages
        except Exception as e:
            print("General error", str(e))
            sys.exit()


if __name__ == '__main__':
    chat_client = ChatClient()
    chat_client.start()
    # sys.stdout.write("\033[K") # Clear to the end of line
