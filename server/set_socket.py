import socket

server_ip = 'localhost'
#server_ip =

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((server_ip, 10000))
main_socket.setblocking(False)
main_socket.listen(5)
print('server socket is working')