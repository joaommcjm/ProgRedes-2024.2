import socket
import hashlib 
import os


DIRBASE = "files/"
SERVER = '127.0.0.1'
PORT = 12345

# Criação do socket TCP e conexão com o servidor
socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktcp.connect((SERVER, PORT))

# Loop principal para interação com o servidor
while True:
    # Exibe a lista de comandos disponíveis para o usuário
    print("\nLista de possíveis comandos:")
    print("A) list  -Lista arquivos presentes no servidor.")
    print("B) sget <nome_do_arquivo> -Solicita o download de um arquivo do servidor.")
<<<<<<< HEAD
    print("C) mget <máscara> (Ex: *.jpg) - Solicitar download de múltiplos arquivos.")
=======
    print("C) mget <máscara> - Solicitar download de múltiplos arquivos.")
>>>>>>> ad2659d999ba4d24fc0e66d2688315bb871ac278
    print("D) hash <nome_do_arquivo> <posição> - Calcula o hash do arquivo até uma posição especifica")
    print("E) cget <nome_do_arquivo> - Continua o download de um arquivo")
    print("F) exit -Encerra a conexão e o programa.")

<<<<<<< HEAD
    # Variável de controle para validar comandos
    comandoValido = False
    comando = input("\ncomando: ")

    # Loop para garantir que o comando seja válido
    while not comandoValido:
        try:
             # Comando para listar arquivos no servidor
            if comando == "list":
                socktcp.send(comando.encode('utf-8')) # Envia o comando ao servidor
                resposta = socktcp.recv(4096).decode('utf-8') # Recebe a resposta do servidor
                print("Arquivos disponíveis:")
                print(resposta)

                comandoValido = True

            # Comando para baixar um único arquivo    
            elif "sget" in comando:
                # Solicita ao servidor um arquivo específico 
                socktcp.send(comando.encode('utf-8'))
=======
    comandoValido = False
    comando = input("\ncomando: ")
    # Loop para garantir que o comando seja válido
    while not comandoValido:
        try:
            if comando == "list":
                #3 a) Solicitar listagem de arquivos ao servidor
                socktcp.send(comando.encode('utf-8'))
                resposta = socktcp.recv(4096).decode('utf-8')
                print("Arquivos disponíveis:")
                print(resposta)

                comandoValido = True
            elif "sget" in comando:
                # Solicitar um arquivo específico
                socktcp.send(comando.encode('utf-8'))
>>>>>>> ad2659d999ba4d24fc0e66d2688315bb871ac278
                try:
                    # Recebe o tamanho do arquivo em 8 bytes
                    resposta = socktcp.recv(8)
                    tamanho_arquivo = int.from_bytes(resposta, 'big')
                    print(f"Tamanho do arquivo: {tamanho_arquivo} bytes")

                    # Separa o sget e o nome do arquivo
                    comando, fileName = comando.split(maxsplit=1)

                    # Grava o arquivo localmente
                    print(f"Gravando arquivo localmente: {fileName}")
                    localFilePath = os.path.join(DIRBASE, fileName)
                    with open( localFilePath , 'wb') as file:
                        recebido = 0
<<<<<<< HEAD
                        count = 100         # Variável criada para printar bytes recebidos a cada 100 repetições do laço
                        
                        # Recebe o tamanho do arquivo em 8 bytes
=======
                        count = 100
>>>>>>> ad2659d999ba4d24fc0e66d2688315bb871ac278
                        while recebido < tamanho_arquivo:
                            data, source = socktcp.recvfrom(4096)
                            file.write(data)
                            recebido += len(data)
                            if count % 100 == 0:
                                print(f"Recebido {recebido}/{tamanho_arquivo} bytes...")
                            count += 1
                        print(f"Arquivo recebido com sucesso!\n")

                except Exception as e:
                    #Exibe erros que podem ocorrer durante o recebimento
                    print(f"Erro ao receber o arquivo: {str(e)}")
                comandoValido = True
<<<<<<< HEAD

            # Comando para baixar múltiplos arquivos    
            elif "mget" in comando:
                try:
                    # Envia o comando para obter vários arquivos
=======
            elif "mget" in comando:
                # Envia o comando para obter vários arquivos
                try:
>>>>>>> ad2659d999ba4d24fc0e66d2688315bb871ac278
                    socktcp.send(comando.encode('utf-8'))
                    resposta = socktcp.recv(4096).decode('utf-8')
                
                    if "Erro" in resposta:
<<<<<<< HEAD
                        print(resposta) # Exibe mensagem de erro do servidor
                        break
=======
                        print(resposta)
>>>>>>> ad2659d999ba4d24fc0e66d2688315bb871ac278
                    else:
                        # Número de arquivos que atenderam à máscara especificada
                        num_arquivos = int(resposta)
                        print(f"Número de arquivos encontrados: {num_arquivos}")
                    
                        for aux in range(num_arquivos):
                            try:
                                # Recebe o nome do arquivo 
                                fileName = socktcp.recv(512).decode('utf-8')
<<<<<<< HEAD
                                socktcp.send(b'1') # Confirmação para o servidor
                                fileSize = int.from_bytes(socktcp.recv(8), 'big')
                                socktcp.send(b'1') # Confirmação para o servidor

                                # Cria o arquivo localmente para gravar os dados recebidos
=======
                                socktcp.send(b'1')
                                fileSize = int.from_bytes(socktcp.recv(8), 'big')
                                socktcp.send(b'1')

>>>>>>> ad2659d999ba4d24fc0e66d2688315bb871ac278
                                localFilePath = os.path.join(DIRBASE, fileName)

                                print(f"Recendo arquivo: {fileName} com {fileSize} bytes.\n")
                                with (open(localFilePath, 'wb') as file):
                                    recebido = 0
<<<<<<< HEAD
                                    count = 100         # Variável criada para printar bytes recebidos a cada 100 repetições do laço

                                     # Recebe e grava o arquivo em partes
                                    while recebido < fileSize:
                                        chunk = socktcp.recv(4096)
                                        file.write(chunk)
                                        recebido += len(chunk)
                                        if count % 100 == 0:
                                            print(f"Recebidos {recebido} de {fileSize} do arquivo {fileName}.")
                                        count += 1
                                    print(f"\nArquivo {fileName} salvo em {localFilePath}.")
                            except Exception as e:
                                # Exibe erro que ocorrem durante o download de cada arquivo
                                print(f"Erro ao processar o arquivo {fileName}: {str(e)}")
                            comandoValido = True
            
                except Exception as e:
                    # Exibe erro relacionado ao comando 'mget'
                    print(f"Erro no comando 'mget': {str(e)}")         
            
            # Comando para calcular o hash até uma posição específica
            elif "hash" in comando:
                try:
                    socktcp.send(comando.encode('utf-8')) # Envia o comando ao servidor
                    resposta = socktcp.recv(4096).decode('utf-8')  # Recebe o hash calculado pelo servidor
                    print(f"Hash recebido do servidor: {resposta}")
                except Exception as e:
                    print(f"Erro ao solicitar o hash: {str(e)}")
                comandoValido = True
            
            # Comando para continuar o download de um arquivo
            elif "cget" in comando:
                try:
                    socktcp.send(comando.encode('utf-8'))
                    comando, fileName = comando.split(maxsplit=1)
                    localFilePath = os.path.join(DIRBASE, fileName)

                    if not os.path.exists(localFilePath):
                        print("Arquivo não encontrado localmente para continuar download.")
                    else:
                        # Calcula o tamanho e o hash da parte existente
                        local_size = os.path.getsize(localFilePath)
                        with open(localFilePath, 'rb') as f:
                            local_data = f.read()
                            local_hash = hashlib.sha1(local_data).hexdigest()

                        # Envia tamanho e hash local para o servidor
                        socktcp.send(local_size.to_bytes(8, 'big'))
                        socktcp.send(local_hash.encode('utf-8'))

                        # Recebe resposta do servidor sobre a continuidade
                        server_response = socktcp.recv(512).decode('utf-8')
                        if "Erro" in server_response:
                            print(server_response)
                        else:
                            # Continua o download a partir do tamanho local
                            fileSize = int(server_response)
                            with open(localFilePath, 'ab') as file:
                                recebido = local_size
                                while recebido < fileSize:
                                    chunk = socktcp.recv(4096)
                                    file.write(chunk)
                                    recebido += len(chunk)
                                print(f"Download concluído: {fileName}")
                    comandoValido = True
                except Exception as e:
                    print(f"Erro! Não foi possível continuar o download do arquivo: {str(e)}")
                    comandoValido = True

            # Encerra a conexão e o programa   
            elif comando == "exit":
                    print("Encerrando conexão com o servidor.")
                    socktcp.send(comando.encode('utf-8'))
                    socktcp.close()
                    exit()
            else:
                print("Comando inválido, tente novamente.")
                comando = input("\ncomando: ").strip()
        except Exception as e:
            # Exibe qualquer erro que ocorra durante o processamento de comandos
            print(f"Erro no processamento do comando: {str(e)}")
            
=======
                                    count = 100
                                    while recebido < fileSize:
                                        chunk = socktcp.recv(4096)
                                        file.write(chunk)
                                        recebido += len(chunk)
                                        if count % 100 == 0:
                                            print(f"Recebidos {recebido} de {tamanho_arquivo} do arquivo {fileName}.")
                                        count += 1
                                    print(f"\nArquivo {fileName} salvo em {localFilePath}.")
                            except Exception as e:
                                # Exibe erro que ocorrem durante o download de cada arquivo
                                print(f"Erro ao processar o arquivo {fileName}: {str(e)}")
                            comandoValido = True
            
                except Exception as e:
                    # Exibe erro relacionado ao comando 'mget'
                    print(f"Erro no comando 'mget': {str(e)}")         
            
            elif "hash" in comando:
                try:
                    socktcp.send(comando.encode('utf-8'))
                    resposta = socktcp.recv(4096).decode('utf-8')
                    print(f"Hash recebido do servidor: {resposta}")
                except Exception as e:
                    print(f"Erro ao solicitar o hash: {str(e)}")
                comandoValido = True
            
            elif "cget" in comando:
                try:
                

                except Exception as e:
                    print(f"Erro! Não foi possivel continuar o download do arquivo: {str(e)}")
                    comandoValido = True
            # Encerra a conexão e o programa   
            elif comando == "exit":
                    print("Encerrando conexão com o servidor.")
                    socktcp.send(comando.encode('utf-8'))
                    socktcp.close()
                    exit()
            else:
                print("Comando inválido, tente novamente.")
                comando = input("\ncomando: ").strip()
        except Exception as e:
            # Exibe qualquer erro que ocorra durante o processamento de comandos
            print(f"Erro no processamento do comando: {str(e)}")

    
>>>>>>> ad2659d999ba4d24fc0e66d2688315bb871ac278
