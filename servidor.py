import socket

IP = ''
PORTA_UDP = 7100
PORTA_TCP = 7200

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((IP, PORTA_TCP))
tcp.listen(1)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((IP, PORTA_UDP))
udp.listen(1)

conn, addr = tcp.accept()
while True:
	data = conn.recv(1024)
	if(data.decode() == 'fazer ping'):
		conn_udp, addr_udp = udp.accept()
		while True:
			data = conn_udp.recv(1024)
			if(data.decode() == 'fim ping'):
				conn_udp.close();
				break;
			else:
				conn_udp.send(message)  # echo
		
	if(data.decode() == 'fazer download'):
		#vai usar a mesma conexao tcp
		while True:
			##enviar arquivo
			
	if(data.decode() == 'fazer upload'):
		#vai usar a mesma conexao tcp
		while True:
			##receber arquivo
			
	if(data.decode() == 'fim'):
		conn.close();
		break;


'''		
conn, addr = s.accept()
print 'Endereco de conexao: ', addr
data = conn.recv(1024) #Tamanho do buffer.
print ("Mensagem Recebida:", data.decode())
message = data.upper()
conn.send(message)
while data != "exit":
	data = conn.recv(1024) #Tamanho do buffer.
	print ("Mensagem Recebida:", data.decode())
	message = data.upper()
	conn.send(message)  # echo
conn.close()
'''
