import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.45"
port = 5555

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()       


#Socket program
def start_server():
    #Binding to port 9999
    #Only two clients can connect 
    try:
        s.bind((host, port))
        print("PVP tank server started \nBinding to port", port)
        s.listen(2) 
        accept_players()
        handle_client()
    except socket.error as e:
        print("Server binding error:", e)
    

#Accept player
#Send player number
def accept_players():
    try:
        for i in range(2):
            conn, addr = s.accept()
            msg = "<<< You are player {} >>>".format(i+1)
            conn.send(str(i+1).encode())
            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))
    
            threading.Thread(target=handle_client, args=(conn,)).start()
        # start_game()
        s.close()
    except socket.error as e:
        print("Player connection error", e)
    except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            exit()
    except Exception as e:
        print("Error occurred:", e)



def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            print("Received from client:", data)
            
            if not data:
                break
            
            # Xử lý dữ liệu từ client tại đây
            if data == "":
                break
            other_conn = [c for c in playerConn if c != conn]
            if other_conn:
                other_conn[0].sendall(data.encode())
                
        except socket.error as e:
            print("Error receiving data from client:", e)
            break

start_server()