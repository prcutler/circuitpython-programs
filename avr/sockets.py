import socket


HOST = "192.168.1.119"
PORT = 23

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b"Z2CD\n")
    data = s.recv(1024)
    print("Done")
