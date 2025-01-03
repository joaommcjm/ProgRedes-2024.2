import socket

DIRBASE = "files/"
INTERFACE = '127.0.0.1'
PORT = 12345

socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktcp.bind((INTERFACE, PORT))
socktcp.listen(1)

print("Escutando em ...", (INTERFACE, PORT))
while True:
    #3 a) Recebe o comando do cliente
    conn, addr = socktcp.accept() #
    print(f"Conexão recebida de: {addr}")
    comando = conn.recv(512).decode('utf-8')
    print(f"Comando recebido: {comando}")

    if comando == "list":
            fileName = comando
            print(f"Recebi pedido para o arquivo: {fileName}")

    try:
        with open(DIRBASE + fileName, 'rb') as file:
            file.seek(0, 2) #percorre o arquivo do inicio ao fim
            tamanho_arquivo = file.tell() #pega o tamanho do arquivo
            file.seek(0) #volta para o inicio do arquivo
            print(f"Tamanho do arquivo: {tamanho_arquivo}")
            conn.send(tamanho_arquivo.to_bytes(8, 'big')) #envia o tamanho do arquvio ao cliente

    # Lê o conteúdo do arquivo e envia ao cliente
            print (f"Enviando arquivo: {fileName}")
            fileData = file.read(4096)
            while fileData:
                conn.send(fileData)
                fileData = file.read(4096)
                print("Arquivo enviado com sucesso!")
    except FileNotFoundError:
        erro = "Erro: Arquivo não encontrado"
        print("Arquivo não encontrado:", fileName)
        conn.send(erro.encode('utf-8'))
        
    conn.close()
    socktcp.close()