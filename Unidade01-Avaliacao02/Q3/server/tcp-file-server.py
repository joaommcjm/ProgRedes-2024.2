import socket
import os
import hashlib
import glob


DIRBASE = "files/"
INTERFACE = '127.0.0.1'
PORT = 12345

# Criação do socket TCP
socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktcp.bind((INTERFACE, PORT)) # Associa o socket ao endereço e porta especificados
socktcp.listen(1) # O servidor começa a escutar conexões

print("Escutando em ...", (INTERFACE, PORT))

# Laço principal para aceitar conexões de clientes
while True:
    #3 a)
    try:
        # Recebe a conexão
        conn, addr = socktcp.accept() 
        print(f"Conexão recebida de: {addr}")
        
        # Laço de processamento dos comandos
        while True:
            print("\n Aguardando comando...\n")
            # Recebe o comando do cliente
            comando = conn.recv(512).decode('utf-8')
            print(f"Comando recebido: {comando}")

            # Lista os arquivos presentes no servidor
            if comando == "list":
                try:
                    # Obtém a lista de arquivos no diretório base
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
                
                # Trata erros ao listar os arquivos
                except Exception as e:
                    erro = f"Erro ao listar arquivos: {str(e)}"
                    print(erro)
                    conn.send(erro.encode('utf-8'))

            # Envia o arquivo solicitado pelo cliente   
            elif "sget" in comando:
                try:
                    # Separa os argumentos do comando
                    comando, fileName = comando.split(maxsplit=1)
                    filePath = os.path.join(DIRBASE, fileName)
                    
                    # Garante que o caminho está dentro de DIRBASE
                    if not os.path.realpath(filePath).startswith(os.path.realpath(DIRBASE)):
                        erro = f"Erro: Acesso ao arquivo '{fileName}' negado."
                        print(erro)
                        conn.send(erro.encode('utf-8'))

                    # Verifica se o arquivo existe
                    elif not os.path.isfile(filePath):
                        erro = f"Erro: Arquivo '{fileName}' não encontrado."
                        print(erro)
                        conn.send(erro.encode('utf-8')) # Envia a mensagem de erro para o cliente.
                    
                    # Processa o arquivo caso ele exista
                    else:
                        with open(filePath, 'rb') as file:
                            file.seek(0, 2) # Percorre o arquivo do inicio ao fim
                            tamanho_arquivo = file.tell() # Pega o tamanho do arquivo
                            print(f"Tamanho do arquivo: {tamanho_arquivo}")
                            file.seek(0) # Volta para o início do arquivo
                            conn.send(tamanho_arquivo.to_bytes(8, 'big')) # Envia o tamanho do arquvio ao cliente

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
                
                # Trata exceções no comando sget
                except Exception as e:
                    print(f"Erro no comando 'sget': {str(e)}")
                    conn.send(f"Erro no comando 'sget': {str(e)}".encode('utf-8'))
            # Multiplas solicitações de arquivos
            elif "mget" in comando:
                try:
                    # Divide o comando e a máscara fornecida
                    comando, mask = comando.split(maxsplit=1)

                    # Busca arquivos correspondentes a máscara
                    filePaths = glob.glob(os.path.join(DIRBASE, mask))
                    safePaths = [fp for fp in filePaths if os.path.realpath(fp).startswith(os.path.realpath(DIRBASE))]

                    # Caso nenhum arquivo seja encontrado ou não exista caminho seguro envia uma mensagem de erro
                    if not filePaths or not safePaths:
                        msg = f"Erro: Máscara inválida."
                        print(msg)
                        conn.send(msg.encode('utf-8'))
                        break
                    else:
                        # Envia a quantidade de arquivos encontrados para o cliente
                        conn.send(str(len(safePaths)).encode('utf-8'))
                        for filePath in safePaths:
                            fileName = os.path.basename(filePath)
                            fileSize = os.path.getsize(filePath)

                            # Envia o nome e tamanho do arquivo
                            conn.send(fileName.encode('utf-8'))
                            conn.recv(1) 
                            conn.send(fileSize.to_bytes(8,'big'))
                            conn.recv(1)

                            # Envia o conteúdo do arquivo
                            with open(filePath, 'rb') as file:
                                print(f"Enviando arquivo {fileName} com {fileSize} bytes.")
                                while chunk := file.read(4096):
                                    conn.send(chunk)
                            print("Arquivo enviado.")    

                except Exception as e:
                    erro = f"Erro no comando 'mget': {str(e)}\nSiga o padrão de comando: 'mget <máscara> (Ex: *.jpg)'"
                    print(erro)
                    conn.send(erro.encode('utf-8'))

            # Implementação do cálculo de hash até uma posição específica
            elif "hash" in comando:
                try:
                    # Divide o comando, nome do arquivo e posição
                    comando, fileName, pos = comando.split(maxsplit=2)
                    filePath = os.path.join(DIRBASE, fileName)

                    # Verifica se o arquivo existe
                    if not os.path.isfile(filePath):
                        erro = f"Erro: Arquivo '{fileName}' não encontrado."
                        print(erro)
                        conn.send(erro.encode('utf-8'))
                    else:
                        # Lê o conteúdo do arquivo até a posição especificada
                        pos = int(pos)
                        with open(filePath, 'rb') as file:
                            data = file.read(pos)
                            hash_value = hashlib.sha1(data).hexdigest() # Calcula o hash SHA-1 do conteúdo lido
                            conn.send(hash_value.encode('utf-8')) # Envia o valor do hash para o cliente
                            print(f"Hash SHA-1 até a posição {pos} do arquivo {fileName}: {hash_value}")
                except Exception as e:
                    # Trata erros durante o cálculo do hash
                    erro = f"Erro ao calcular o hash: {str(e)}"
                    print(erro)
                    conn.send(erro.encode('utf-8'))
          
            elif "cget" in comando:
                try:
                    # Separa o comando e o nome do arquivo
                    comando, fileName = comando.split(maxsplit=1)
                    filePath = os.path.join(DIRBASE, fileName)

                    # Verifica se o arquivo existe no servidor
                    if not os.path.isfile(filePath):
                        erro = f"Erro: Arquivo '{fileName}' não encontrado no servidor."
                        conn.send(erro.encode('utf-8'))
                    else:
                        # Recebe tamanho e hash do cliente da parte existente no cliente
                        client_size = int.from_bytes(conn.recv(8), 'big')
                        client_hash = conn.recv(40).decode('utf-8')

                        # Calcula o hash da parte correspondente no servidor
                        with open(filePath, 'rb') as file:
                            server_data = file.read(client_size)
                            server_hash = hashlib.sha1(server_data).hexdigest()
                            
                            #print(f"{client_hash}\n{server_hash}")
                            # Verifica se o hash recebido do cliente coincide com o do servidor
                            if client_hash != server_hash:
                                erro = "Erro: Hash da parte existente não coincide com o servidor."
                                conn.send(erro.encode('utf-8'))
                            else:
                                # Envia o tamanho total do arquivo
                                fileSize = os.path.getsize(filePath)
                                conn.send(str(fileSize).encode('utf-8'))
                                file.seek(client_size)
                                # Envia o restante do arquivo a partir da posição onde o cliente parou
                                file.seek(client_size)
                                while chunk := file.read(4096):
                                    conn.send(chunk)
                                    
                # Trata erros durante o comando 'cget'
                except Exception as e:
                    erro = f"Erro no comando 'cget': {str(e)}"
                    conn.send(erro.encode('utf-8'))

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
        
