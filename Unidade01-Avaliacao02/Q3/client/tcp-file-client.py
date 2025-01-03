import socket
import hashlib 

DIRBASE = "files/"
SERVER = '127.0.0.1'
PORT = 12345

socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktcp.connect((SERVER, PORT))

while True:
    comando = input("Digite 'list' para listar arquivos ou o nome de um arquivo para baixá-lo: ").strip()
    
    if comando == "list":
        #3 a) Solicitar listagem de arquivos ao servidor
        socktcp.send(comando.encode('utf-8'))
        resposta = socktcp.recv(4096).decode('utf-8')
        print("Arquivos disponíveis:")
        print(resposta)
    else:
        # Solicitar um arquivo específico
        socktcp.send(comando.encode('utf-8'))

        try:
            tamanho_arquivo = int.from_bytes(tamanho_arquivo, 'big')
            print(f"Tamanho do arquivo: {tamanho_arquivo} bytes")

            # Grava o arquivo localmente
            print(f"Gravando arquivo localmente: {comando}")
            with open(DIRBASE + comando, 'wb') as file:
                recebido = 0
                while recebido < tamanho_arquivo:
                    data, source = socktcp.recvfrom(4096)
                    file.write(data)
                    recebido += len(data)
                print(f"Arquivo {comando} recebido com sucesso!")
        except ValueError:
            # Trata mensagem de erro do servidor
            resposta = socktcp.recv(4096).decode('utf-8')
            print(f"Erro recebido do servidor: {resposta}")

    # Fecha o socket ao final
    socktcp.close()
    exit()