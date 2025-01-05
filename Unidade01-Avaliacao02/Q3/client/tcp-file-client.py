import socket
import hashlib 
import os

DIRBASE = "files/"
SERVER = '127.0.0.1'
PORT = 12345

socktcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktcp.connect((SERVER, PORT))

while True:
    print("\nLista de possíveis comandos:")
    print("A) list  -Lista arquivos presentes no servidor.")
    print("B) sget <nome_do_arquivo> -Solicita o download de um arquivo do servidor.")
    print("C) mget <máscara> - Solicitar download de múltiplos arquivos.")
    print("D) exit -Encerra a conexão e o programa.")
    
    comandoValido = False
    comando = input("\ncomando: ").strip()
    
    while not comandoValido:
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

            # Recebe o tamanho do arquivo em 8 bytess
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
                count = 100
                while recebido < tamanho_arquivo:
                    data, source = socktcp.recvfrom(4096)
                    file.write(data)
                    recebido += len(data)
                    if count % 100 == 0:
                        print(f"Recebido {recebido}/{tamanho_arquivo} bytes...")
                    count += 1
                print(f"Arquivo recebido com sucesso!\n")

            comandoValido = True
        elif "mget" in comando:
            try:
                socktcp.send(comando.encode('utf-8'))
                resposta = socktcp.recv(4096).decode('utf-8')
                
                if "Erro" in resposta:
                    print(resposta)
                else:
                    num_arquivos = int(resposta)
                    print(f"Número de arquivos encontrados: {num_arquivos}")

                    for aux in range(num_arquivos):
                        fileName = socktcp.recv(512).decode('utf-8')
                        socktcp.send(b'1')
                        fileSize = int.from_bytes(socktcp.recv(8), 'big')
                        socktcp.send(b'1')

                        localFilePath = os.path.join(DIRBASE, fileName)

                        print(f"Recendo arquivo: {fileName} com {fileSize} bytes.\n")
                        with (open(localFilePath, 'wb') as file):
                            recebido = 0
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
                print(f"Erro no comando 'mget': {str(e)}")

         # Encerra a conexão e o programa   
        elif comando == "exit":
            print("Encerrando conexão com o servidor.")
            socktcp.send(comando.encode('utf-8'))
            socktcp.close()
            exit()
        else:
            print("Comando inválido, tente novamente.")
            comando = input("\ncomando: ").strip()