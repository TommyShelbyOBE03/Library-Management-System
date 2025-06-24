#MY SERVER
import socket
import threading
import pickle
import os
import portalocker

# Global library data
library_data = {
    'books': {},
    'members': {
        'admin': {'password': 'admin', 'role': 'admin'}
    }
}
library_file = 'library_data.pkl'
lock = threading.Lock()

def load_data():
    if os.path.exists(library_file):
        with open(library_file, 'rb') as f:
            portalocker.lock(f, portalocker.LOCK_SH)
            data = pickle.load(f)
            portalocker.unlock(f)
            return data
    return {'books': {}, 'members': {'admin': {'password': 'admin', 'role': 'admin'}}}

def save_data(data):
    with open(library_file, 'wb') as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        pickle.dump(data, f)
        portalocker.unlock(f)

def handle_client(client_socket):
    global library_data

    while True:
        try:
            request = client_socket.recv(4096)
            if not request:
                break

            request_data = pickle.loads(request)
            action = request_data.get('action')
            response = {}

            lock.acquire()

            try:
                if action == 'login':
                    username = request_data.get('username')
                    password = request_data.get('password')
                    if username in library_data['members'] and library_data['members'][username]['password'] == password:
                        response['status'] = 'success'
                        response['role'] = library_data['members'][username]['role']
                    else:
                        response['status'] = 'fail'
                
                elif action == 'add_book':
                    book_id = request_data.get('book_id')
                    book_info = request_data.get('book_info')
                    library_data['books'][book_id] = book_info
                    response['status'] = 'success'
                    save_data(library_data)
                
                elif action == 'delete_book':
                    book_id = request_data.get('book_id')
                    if book_id in library_data['books']:
                        del library_data['books'][book_id]
                        response['status'] = 'success'
                        save_data(library_data)
                    else:
                        response['status'] = 'fail'
                
                elif action == 'modify_book':
                    book_id = request_data.get('book_id')
                    book_info = request_data.get('book_info')
                    if book_id in library_data['books']:
                        library_data['books'][book_id] = book_info
                        response['status'] = 'success'
                        save_data(library_data)
                    else:
                        response['status'] = 'fail'

                elif action == 'search_book':
                    book_id = request_data.get('book_id')
                    book_info = library_data['books'].get(book_id, 'Not found')
                    response['status'] = 'success'
                    response['book_info'] = book_info

                elif action == 'add_member':
                    username = request_data.get('username')
                    password = request_data.get('password')
                    role = request_data.get('role')
                    if username not in library_data['members']:
                        library_data['members'][username] = {'password': password, 'role': role}
                        response['status'] = 'success'
                        save_data(library_data)
                    else:
                        response['status'] = 'fail'

                elif action == 'delete_member':
                    username = request_data.get('username')
                    if username in library_data['members']:
                        del library_data['members'][username]
                        response['status'] = 'success'
                        save_data(library_data)
                    else:
                        response['status'] = 'fail'
            finally:
                lock.release()

            client_socket.send(pickle.dumps(response))
        
        except Exception as e:
            print(f"Exception: {e}")
            break

    client_socket.close()

def main():
    global library_data

    library_data = load_data()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)

    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()

