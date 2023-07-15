import socket
import sys
import threading

IP = '192.168.0.117'
PORT = 5000
CONECTION_LIMIT = 10
process_queue = []  
process = {}  
lock = threading.Lock()

def grant_acess():
    while True:
        if process_queue:
            pid = process_queue[0]
            send_message(pid, "GRANT")
            print("Processo ", pid, "na regiao critica.\n")
            process_queue.pop(0)

def handle_conections():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((IP, PORT))
  server.listen(CONECTION_LIMIT)

  while True:
      client, client_addr = server.accept()
      thread_client = threading.Thread(target=handle_process, args=(client,))
      thread_client.start()
  
def handle_process(client):
  pid = client.recv(1024).decode()
  process[pid] = client
  lock.acquire()
  process_queue.append(pid)
  lock.release()
  print("Processo", pid, "conectado ao coordenador!\n")


def send_message(pid, message):
    if pid in process:
        socket_cliente = process[pid]
        socket_cliente.send(message.encode())

def show_queue():
    print("\nProcesso na fila: \n")
   
    lock.acquire()
    if process_queue:
        for pid in process_queue:
            print("Processo de id: ", pid,"\n")
    else:
        print("Nenhum processo na fila.\n")
    lock.release()

def conected_process():
    print("\nProcessos conectados: \n")
    lock.acquire()
    if process:
        for pid, client in process.items():
            print(f"Processo {pid} - Atendido", client, "\n")
    else:
        print("Nenhum processo conectado\n")
    lock.release()

def start_coordinator():
    thread_conect = threading.Thread(target=handle_conections)
    thread_conect.start()
    thread_execute = threading.Thread(target=grant_acess)
    thread_execute.start()

    while True:
        option = input("\nOpcoes: \n1-> Mostrar lista de processos \n2-> Mostrar fila \n3-> Sair\n")
        
        if option == "1":
            conected_process()  
        elif option == "2":
            show_queue() 
        elif option == "3":
            print('Saindo...')
            sys.exit(0)
        else:
            print('Opcao invalida.\n')

if __name__ == "__main__":
     start_coordinator()

