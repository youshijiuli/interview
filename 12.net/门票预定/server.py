import socket
import threading
import os


class TicketBookingServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ticket_db = "db/tickets"
        self.user_db = "db/users/"

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Ticket booking server started.")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address[0]}:{client_address[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode()
        print(f"Received request: {request}")

        if "-" in request:
            self.process_booking_request(client_socket, request)
        else:
            self.process_query_request(client_socket, request)

        client_socket.close()

    def process_query_request(self, client_socket, request):
        query_str = request.strip()
        ticket_file_path = self.ticket_db + "/" + query_str + ".txt"

        try:
            with open(ticket_file_path, "r") as ticket_file:
                ticket_count = int(ticket_file.read().strip())
                response = f"Available tickets for {query_str}: {ticket_count}"
        except FileNotFoundError:
            response = f"Cannot find tickets for {query_str}"

        client_socket.send(response.encode())

    def process_booking_request(self, client_socket, request):
        booking_info = request.strip().split("-")
        query_str, user_name, ticket_count = booking_info[0], booking_info[1], int(booking_info[2])
        ticket_file_path = self.ticket_db + "/" + query_str + ".txt"
        user_dir_path = self.user_db + user_name
        user_file_path = user_dir_path + "/" + query_str + ".txt"

        try:
            with open(ticket_file_path, "r") as ticket_file:
                available_tickets = int(ticket_file.read().strip())
                if available_tickets >= ticket_count:
                    with open(ticket_file_path, "w") as ticket_file:
                        ticket_file.write(str(available_tickets - ticket_count))

                    if not os.path.exists(user_dir_path):
                        os.makedirs(user_dir_path)

                    with open(user_file_path, "a", encoding='utf-8') as user_file:
                        user_file.write(f"Booked {ticket_count} tickets for {query_str}\n")

                    with open(ticket_file_path, "r") as updated_ticket_file:
                        updated_ticket_count = int(updated_ticket_file.read().strip())
                        response = f"Ticket booking for {query_str} successful. Remaining tickets: {updated_ticket_count}"
                else:
                    response = f"Not enough tickets available for {query_str}. Tickets remaining: {available_tickets}"
        except FileNotFoundError:
            response = f"Cannot find tickets for {query_str}"

        client_socket.send(response.encode())


if __name__ == "__main__":
    server = TicketBookingServer("localhost", 8888)
    server.start()
