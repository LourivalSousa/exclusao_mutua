import threading
import socket
import time

def iniciar(process,loops, k):
    for _ in range(loops):
        print(process)
        solicitar_secao_critica(process)
        entrar_secao_critica(process)

        time.sleep(k)
        sair_secao_critica(process)

def solicitar_secao_critica(process):
    mensagem = f"1-{process['pid']}|".ljust(process['size'], '0')
    enviar_mensagem(process,mensagem)

def enviar_mensagem(process, mensagem):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((process["ip"], process['port']))
    client.sendall(mensagem.encode())
    client.close()

def entrar_secao_critica(process):
    with open("resultado.txt", "a") as arquivo:
        hora_atual = time.strftime("%Y-%m-%d %H:%M:%S.%f")
        arquivo.write(f"Processo {process['pid']} entrou na seção crítica no horario: {hora_atual}\n")

def sair_secao_critica(process):
    with open("resultado.txt", "a") as arquivo:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S.%f")
        arquivo.write(f"Processo {process['pid']} saiu da seção crítica no horario {current_time}\n")

if __name__ == "__main__":
    quant_process = int(input("Insira a quantidade de processos: \n"))
    k = int(input("Insira o valor de k, o formato deve ser em segundos.: \n"))
    repet = int(input("Insira a quantidade de repeticoes: \n"))
    size = int(input("Insira em bytes o tamanho das mensagens: \n"))

    process_array = []

    for i in range(quant_process):
        pid = str(i + 1)
        
        process = {}

        process["pid"] = pid
        process["ip"] = "192.168.0.117"
        process["port"] = 5000
        process["message_size"] = size

        process_array.append(process)

    threads = []

    for process in process_array:
        thread = threading.Thread(target=iniciar, args=(process, repet, k))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()