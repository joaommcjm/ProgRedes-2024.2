import socket

DIRBASE = "files/"
INTERFACE = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((INTERFACE, PORT))

print("Escutando em ...", (INTERFACE, PORT))


while True:
        # Recebe o nome do arquivo a servir
        data, source = sock.recvfrom(512)
        fileName = data.decode('utf-8')
        print(f"Recebi pedido para o arquivo: {fileName}")

        try:
            with open(DIRBASE + fileName, 'rb') as file:
                file.seek(0, 2) #percorre o arquivo do inicio ao fim
                tamanho_arquivo = file.tell() #pega o tamanho do arquivo
                file.seek(0) #volta para o inicio do arquivo
                print(f"Tamanho do arquivo: {tamanho_arquivo}")
                sock.sendto(tamanho_arquivo.to_bytes(8, 'big'), source) #envia o tamanho do arquvio ao cliente

        # Lê o conteúdo do arquivo e envia ao cliente
                print (f"Enviando arquivo: {fileName}")
                fileData = file.read(4096)
                while fileData:
                    sock.sendto(fileData, source)
                    fileData = file.read(4096)
                print("Arquivo enviado com sucesso!")
        except FileNotFoundError:
            erro = "Erro: Arquivo não encontrado".encode()
            print("Arquivo não encontrado:", fileName)
            sock.sendto(erro, source)

        # Fecha o socket e sai do loop
        sock.close()
        break