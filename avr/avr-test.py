import wifi
import socketpool

HOST = "192.168.1.119"
PORT = 23

pool = socketpool.SocketPool(wifi.radio)
sock = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

sock.connect((HOST, PORT))
sock.send(b"Z2TUNER\n")
# data = sock.recv(1024)
print("Done")