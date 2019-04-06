import os, socket, threading, signal, time

IP = ''
PORTA_UDP = 7100
PORTA_TCP = 7200


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(5)
tcp.bind((IP, PORTA_TCP))
tcp.listen(1)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((IP, PORTA_UDP))
udp.settimeout(3)

class Rtt(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

    def run(self):
        while not self.shutdown_flag.is_set():
            try:
                data, addr = udp.recvfrom(1024)
                udp.sendto(data, addr)
            except socket.timeout:
                continue


def upload_cliente():
    f = open('30mb.bin','wb')
    parte = conn.recv(1024)
    while (parte):
        f.write(parte)
        parte = conn.recv(1024)
    f.close()
    
    
def download_servidor():
	global conn, addr, tcp
	f = open('30mb.bin','rb')
	inicio = time.time()
	l = f.read(1024)
	while (l):
		conn.send(l)
		l = f.read(1024)
	f.close()
	fim = time.time()
	print(((os.stat('recebido.bin').st_size) / (1024*1024 / 8)) / (fim - inicio + 1), "Mbps")

conn = ""
addr = ""
while True:
    conn, addr = tcp.accept()
    print("Conectado: ", addr)
    while True:
            data = conn.recv(1024)
            if(data.decode() == 'fazer rtt'):
                print("fazer rtt")
                t = Rtt()
                t.start()
                data = conn.recv(1024)
                print(data.decode())
                t.shutdown_flag.set()
                time.sleep(3)

            elif(data.decode() == 'fazer download'):
                print('fazer down')
                download_servidor()
                print('fim down')

            elif(data.decode() == 'fazer upload'):
                print('fazer up')
                upload_cliente()
                conn, addr = tcp.accept()
                print('fim up')

            elif(data.decode() == 'fim'):
                print("Desconectado: ", addr)
                conn.close()
                break

