import socket
import time
import sys
import urllib.request
import urllib.parse
import urllib.error
import os

# ip servidor
IP = "ibiza.dcc.ufla.br"
#IP = "localhost"
# portas
PORTA_UDP = 7100
PORTA_TCP = 7200
# mensagem a ser enviada
MENSAGEM = "Rtt!"

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock_tcp.settimeout(5)
destino_tcp = (IP, PORTA_TCP)

sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_udp.settimeout(3)
destino_udp = (IP, PORTA_UDP)


def rtt():
    rttSoma = 0
    pacotesEnviados = 0
    pacotesRecebidos = 0
    pacotesPerdidos = 0
    ultimoRtt = 0
    somaJitter = 0
    primeiroPacoteRecebido = False

    pacotesEnviar = input("\nPacotes a serem enviados: ")
    pacotesEnviar = int(pacotesEnviar)

    print("\nTestando RTT + Jitter: ")
    time.sleep(1)
    for i in range(pacotesEnviar):
        time.sleep(1)
        pacotesEnviados += 1
        tempoEnvio = time.time()
        sock_udp.sendto(MENSAGEM.encode(), destino_udp)

        try:
            resposta = sock_udp.recvfrom(1024)
            tempoChegada = time.time()
            rtt = (tempoChegada - tempoEnvio) * 1000 # armazenando o tempo em ms
            rttSoma += rtt

            if (primeiroPacoteRecebido):
                somaJitter += abs(ultimoRtt - rtt)
            else:
                primeiroPacoteRecebido = True 

            ultimoRtt = rtt

            # printando a chegada do pacote
            print("Resposta de {0}: bytes={1} tempo={2}ms".format(IP, sys.getsizeof(resposta), round(rtt, 2)))
            pacotesRecebidos += 1

        except socket.timeout:
            # printando a perda do pacote
            print('Esgotado o tempo limite.')
            pacotesPerdidos += 1

    # informacoes do rtt
    if (pacotesRecebidos > 0):
        print("\nEstatísticas para {0}:".format(IP))
        print("    Pacotes: Enviados = {0}, Recebidos = {1}, Perdidos = {2} ({3:.2f}% de perdas)".format(pacotesEnviados, pacotesRecebidos, pacotesPerdidos, ( (pacotesPerdidos / pacotesEnviar) * 100 ) ))
        if(pacotesRecebidos > 0):
            print("    Média de RTT = {0}ms".format( round( (rttSoma / pacotesRecebidos), 2) ) )
        if(pacotesEnviar >= 2 and pacotesRecebidos > 1):
            print("    Jitter = {0}ms".format( round( (somaJitter / (pacotesRecebidos - 1) ), 2) ) )
        else:
            print("    Não é possível calcular o Jitter")
        print("\n")


def download():
    global sock_tcp
    f = open('recebidoD.bin','wb')
    i = 1
    inicio = time.time()
    parte = sock_tcp.recv(1024)
    while(parte):
        i = i + 1
        f.write(parte)
        parte = sock_tcp.recv(1024)
        
    fim = time.time()
    f.close()
    
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.settimeout(5)
    sock_tcp.connect(destino_tcp)
    
    print( ( ((os.stat('recebidoD.bin').st_size) * 8) / (1024*1024) ) / (fim - inicio), "Mbps")
    

def upload():
    global sock_tcp
    f = open('30mb.bin','rb')
    inicio = time.time()
    l = f.read(1024)
    while (l):
        sock_tcp.send(l)
        l = f.read(1024)
        
    fim = time.time()
    f.close()
    sock_tcp.shutdown(socket.SHUT_WR) # forma de avisar que a transferencia terminou
    sock_tcp.close()

    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.settimeout(5)
    sock_tcp.connect(destino_tcp)

    print( ( ((os.stat('30mb.bin').st_size) * 8) / (1024*1024) ) / (fim - inicio), "Mbps")


sock_tcp.connect(destino_tcp)
while True:
    print("\n+-------- Menu --------+")
    print("| 1 - RTT + Jitter     |")
    print("| 2 - Download         |")
    print("| 3 - Upload           |")
    print("| 4 - Todas            |")
    print("| Outros - Sair        |")
    print("+----------------------+\n")

    op = input("Escolha uma opcao: ")

    if (op == '1'):
        print("\nTestando o RTT + Jitter:")
        sock_tcp.send('fazer rtt'.encode())
        rtt()
        sock_tcp.send('fim rtt'.encode())
        time.sleep(3)

    elif (op == '2'):
        print("\nTestando o download:")
        sock_tcp.send('fazer download'.encode())
        download()

    elif (op == '3'):
        print("\nTestando o upload:")
        sock_tcp.send('fazer upload'.encode())
        upload()

    elif (op == '4'):
        sock_tcp.send('fazer rtt'.encode())
        print("\nTestando o RTT + Jitter:")
        rtt()
        sock_tcp.send('fim rtt'.encode())
        time.sleep(3)
        sock_tcp.send('fazer download'.encode())
        print("\nTestando o download:")
        download()
        time.sleep(3)
        sock_tcp.send('fazer upload'.encode())
        print("\nTestando o upload:")
        upload()

    else:
        sock_tcp.send('fim'.encode())
        break
