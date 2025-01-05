import socket
import struct
import os
import hashlib
import glob


DIRBASE = "files/"
INTERFACE = '127.0.0.1'
PORT = 12345

socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktcp.bind((INTERFACE, PORT))
socktcp.listen(1)

print("Escutando em ...", (INTERFACE, PORT))

while True:
    try:
        # Recebe a conexão
        conn, addr = socktcp.accept() 
        print(f"Conexão recebida de: {addr}")
        while True:
            print("\n Aguardando comando...\n")
            # Recebe o comando do cliente
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

                    # Envia a listagem de arquivos para o cliente
                    print("Enviando lista de arquivos...")
                    print(finalFiles)
                    conn.send(finalFiles.encode())

                except Exception as e:
                    erro = f"Erro ao listar arquivos: {str(e)}"
                    print(erro)
                    conn.send(erro.encode('utf-8'))

            # Envia o arquivo solicitado        
            elif "sget" in comando:
                try:
                    # Separa os argumentos do comando
                    comando, fileName = comando.split(maxsplit=1)
                    filePath = os.path.join(DIRBASE, fileName)

                    # Verifica se o arquivo existe
                    if not os.path.isfile(filePath):
                        erro = f"Erro: Arquivo '{fileName}' não encontrado."
                        print(erro)
                        conn.send(erro.encode('utf-8')) # Envia a mensagem de erro para o cliente.

                    # Processa o arquivo caso ele exista
                    else:
                        with open(DIRBASE + fileName, 'rb') as file:
                            file.seek(0, 2)                                 # Percorre o arquivo do inicio ao fim
                            tamanho_arquivo = file.tell()                   # Pega o tamanho do arquivo
                            print(f"Tamanho do arquivo: {tamanho_arquivo}")
                            file.seek(0)                                    # Volta para o início do arquivo
                            conn.send(tamanho_arquivo.to_bytes(8, 'big'))   # Envia o tamanho do arquvio ao cliente

                            print(f"Enviando o conteúdo do arquivo: {fileName}")
                            # Lê o arquivo em blocos de 4096, := atribui o resultado à chunk e verifica se ela não está vazia.
                            bytes_enviados = 0
                            count = 100
                            while chunk := file.read(4096):
                                conn.send(chunk)
                                bytes_enviados += len(chunk)
                                if count % 100 == 0:
                                    print(f"Enviando {bytes_enviados} de {tamanho_arquivo} do arquivo: {fileName}")
                                count += 1

                except Exception as e:
                    print("Erro no comando 'sget': {e}")
                    print(erro)
                    conn.send(erro.encode('utf-8'))
            # Multiplas solicitações de arquivos
            elif "mget" in comando:
                
                    comando, mask = comando.split(maxsplit=1)

                    # Busca arquivos correspondentes a máscara
                    filePaths = glob.glob(os.path.join(DIRBASE, mask))

                    if not filePaths:
                        msg = f"Erro: Nenhum arquivo encontrada com a máscara."
                        print(msg)
                        conn.send(msg.encode('utf-8'))
                    else:
                        # Envia a quantidade de arquivos encontrados para o cliente
                        conn.send(str(len(filePaths)).encode('utf-8'))
                        for filePath in filePaths:
                            fileName = os.path.basename(filePath)
                            fileSize = os.path.getsize(filePath)

                            # Envia as informações do arquivo
                            conn.send(fileName.encode('utf-8'))
                            conn.recv(1) 
                            conn.send(fileSize.to_bytes(8,'big'))
                            conn.recv(1)

                            # Envia o arquivo
                            with open(filePath, 'rb') as file:
                                print(f"Enviando arquivo {fileName} com {fileSize} bytes.")
                                while chunk := file.read(4096):
                                    conn.send(chunk)
                            print("Arquivo enviado.")
                
            # Encerra a conexão e o programa
            elif "exit" in comando:
                print("Encerrando servidor...")
                conn.close()
                socktcp.close()
                exit()
            else:
                msg = "Erro: Comando inválido."
                print(msg)
                conn.send(msg.encode('utf-8'))
    except Exception as e:
        print(f"Erro: {e}")
        
    finally:
        conn.close()
        print("Conexão encerrada.")
        exit()
