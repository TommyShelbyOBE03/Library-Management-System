#MY CLIENT 
import socket
import pickle

def make_request(action, params):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9999))

    req = {'action': action}
    req.update(params)

    sock.send(pickle.dumps(req))
    res = pickle.loads(sock.recv(4096))
    sock.close()

    return res

def admin_panel():
    while True:
        print("\nAdmin Panel: add_book, remove_book, edit_book, find_book, create_member, remove_member, logout")
        selection = input("Select an option: ")

        if selection == 'add_book':
            book_id = input("Enter Book ID: ")
            book_info = input("Enter Book Information. Example - Point Blank by Daniel Craig ")
            res = make_request('add_book', {'book_id': book_id, 'book_info': book_info})
            if(res['status'] == 'fail'):
                print(res)
            	print("Enter a 4 digit bookID")
            else:
            	print(res)

        elif selection == 'remove_book':
            book_id = input("Enter Book ID: ")
            res = make_request('delete_book', {'book_id': book_id})
            print(res)

        elif selection == 'edit_book':
            book_id = input("Enter Book ID: ")
            book_info = input("Enter New Book Information: ")
            res = make_request('modify_book', {'book_id': book_id, 'book_info': book_info})
            print(res)

        elif selection == 'find_book':
            book_id = input("Enter Book ID: ")
            res = make_request('search_book', {'book_id': book_id})
            print(res)

        elif selection == 'create_member':
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            role = input("Enter Role (admin/user): ")
            res = make_request('add_member', {'username': username, 'password': password, 'role': role})
            print(res)

        elif selection == 'remove_member':
            username = input("Enter Username: ")
            res = make_request('delete_member', {'username': username})
            print(res)

        elif selection == 'logout':
            break

def user_panel():
    while True:
        print("\nUser Panel: find_book, logout")
        selection = input("Select an option: ")

        if selection == 'find_book':
            book_id = input("Enter Book ID: ")
            res = make_request('search_book', {'book_id': book_id})
            print(res)

        elif selection == 'logout':
            break

def main():
    print("Welcome to the Online Library Management System")
    while True:
        print("\nOptions: login, exit")
        choice = input("Enter choice: ")

        if choice == 'login':
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            res = make_request('login', {'username': username, 'password': password})
            print(res)
            if res['status'] == 'success':
                if res['role'] == 'user':
                    	user_panel()
                else:
                	admin_panel()
                    

        elif choice == 'exit':
            break

if __name__ == "__main__":
    main()
