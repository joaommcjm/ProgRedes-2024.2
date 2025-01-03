import socket
import struct
import os
import hashlib


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

    # Lista os arquivos presentes no servidor
    if comando == "list":
        try:
            serverFiles = os.listdir(DIRBASE)
            finalFiles = ''
            for file in serverFiles:
                filePath = os.path.join(DIRBASE, file)
                if os.path.isfile(filePath):
                    fileSize = os.path.getsize(filePath)
                    finalFiles += "{:<20} {:>15} bytes.\n".format(file, fileSize)
                    
            # Envia a listagem de diretórios para o cliente
            print("Enviando lista de arquivos...")
            print(finalFiles)
            conn.send(finalFiles.encode())
        except FileNotFoundError:
            print("O diretório não foi encontrado.")
        except NotADirectoryError:
            print("O caminho especificado não é um diretório.")
        except PermissionError:
            print("Permissão negada para acessar o diretório.")
            
        #with open(DIRBASE + fileName, 'rb') as file:
        #    file.seek(0, 2) #percorre o arquivo do inicio ao fim
        #    tamanho_arquivo = file.tell() #pega o tamanho do arquivo
        #    file.seek(0) #volta para o inicio do arquivo
        #    print(f"Tamanho do arquivo: {tamanho_arquivo}")
        #    conn.send(tamanho_arquivo.to_bytes(8, 'big')) #envia o tamanho do arquvio ao cliente

    # Lê o conteúdo do arquivo e envia ao cliente
    #        print (f"Enviando arquivo: {fileName}")
    #        fileData = file.read(4096)
    #        while fileData:
    #            conn.send(fileData)
    #            fileData = file.read(4096)
    #            print("Arquivo enviado com sucesso!")
    #except FileNotFoundError:
    #    erro = "Erro: Arquivo não encontrado"
    #    print("Arquivo não encontrado:", fileName)
    #    conn.send(erro.encode('utf-8'))
        
    conn.close()
    socktcp.close()
    break