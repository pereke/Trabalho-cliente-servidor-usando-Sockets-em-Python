
import socket

TCP_IP = ''
TCP_PORT = 7100

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
 
conn, addr = s.accept()
#print 'Endereco de conexao: ', addr

while True:
	data = conn.recv(1024) #Tamanho do buffer.
	print "Mensagem Recebida:", data
	message = data.upper()
	conn.send(message)  # echo

conn.close()
