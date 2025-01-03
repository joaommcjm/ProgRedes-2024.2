import socket

DIRBASE = "files/"
SERVER = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Lê do usuário o nome do arquivo a pedir ao servidor
    fileName = input("Arquivo a pedir ao servidor: ")

    # Envia ao servidor o nome do arquivo desejado pelo usuário
    print(f"Enviando pedido a {SERVER}:{PORT} para {fileName}")
    sock.sendto(fileName.encode('utf-8'), (SERVER, PORT))

    # Recebe o tamanho do arquivo
    tamanho_arquivo, source = sock.recvfrom(8)
    try:
        tamanho_arquivo = int.from_bytes(tamanho_arquivo, 'big')
        print(f"Tamanho do arquivo: {tamanho_arquivo} bytes")

        # Grava o arquivo localmente
        print(f"Gravando arquivo localmente: {fileName}")
        with open(DIRBASE + fileName, 'wb') as file:
            recebido = 0
            while recebido < tamanho_arquivo:
                data, source = sock.recvfrom(4096)
                file.write(data)
                recebido += len(data)
                print(f"Recebido: {recebido}/{tamanho_arquivo} bytes")
        print("Arquivo recebido com sucesso!")
    except ValueError:
        # Trata mensagem de erro do servidor
        print("Erro recebido do servidor:", tamanho_arquivo.decode('utf-8'))
        
    # Fecha o socket ao final
    sock.close()
    exit()