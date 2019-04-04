import socket, time, sys, urllib.request, urllib.parse, urllib.error

## ip servidor
IP = "127.0.0.1"
## porta
PORTA = 5002
## mensagem a ser enviada
MENSAGEM = "Ping!" 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.250)

pacotesEnviar = 0
rttSoma = 0
pacotesEnviados = 0
pacotesRecebidos = 0
pacotesPerdidos = 0

primeiroPacoteRecebido = False
ultimoRtt = 0
somaJitter = 0

print("Estatísticas para {0}:".format(IP))
for i in range(pacotesEnviar):
    time.sleep(1)
    pacotesEnviados += 1
    tempoEnvio = time.time()
    sock.sendto(bytes(MENSAGEM, "utf-8"), (IP, PORTA))
    try:
        resposta, server = sock.recvfrom(1024)
        tempoChegada = time.time()
        rtt = (tempoChegada - tempoEnvio) * 1000 # armazenando o tempo em ms
        rttSoma += rtt

        if(primeiroPacoteRecebido):
          somaJitter += abs(ultimoRtt - rtt)
        else:
          primeiroPacoteRecebido = True 

        ultimoRtt = rtt

        ## printando a chegada do pacote
        print("Resposta de {0}: bytes={1} tempo={2}ms".format(IP, sys.getsizeof(resposta), round(rtt, 2)))
        pacotesRecebidos += 1

    except socket.timeout:
        ## printando a perda do pacote
        print('Esgotado o tempo limite.')
        pacotesPerdidos += 1

## informacoes do ping
if(pacotesEnviar > 1):
    print("\nTestando Ping:".format(IP))
    print("    Pacotes: Enviados = {0}, Recebidos = {1}, Perdidos = {2} ({3:.2f}% de perdas)".format(pacotesEnviados, pacotesRecebidos, pacotesPerdidos, ( (pacotesPerdidos / pacotesEnviar) * 100 ) ))
    print("    Média de Ping = {0}ms".format( round( (rttSoma / pacotesRecebidos), 2) ) )
    if(pacotesEnviar > 2):
        print("    Jitter = {0}ms".format( round( (somaJitter / (pacotesRecebidos - 1) ), 2) ) )


print("\nTestando o Download: ")
url = "https://www.amd.com/system/files/TechDocs/24593.pdf"
tempo = time.time()
f = urllib.request.urlopen(url)
data = f.read()
print(len(data))
print((len(data) / (1024*1024 / 8)) / (time.time() - tempo), "Mbps")
#with open("arq.pdf", "wb") as code:
#    code.write(data)
