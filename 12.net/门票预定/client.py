import os
import socket


class TicketBookingClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        return client_socket

    def query_tickets(self, ticket_name):
        request = ticket_name.strip()
        client_socket = self.connect()
        client_socket.send(request.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        client_socket.close()

    def book_tickets(self, booking_info):
        request = booking_info.strip()
        client_socket = self.connect()
        client_socket.send(request.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        client_socket.close()

    def get_available_tickets(self):
        ticket_folder_path = "db/tickets"
        ticket_files = [file for file in os.listdir(ticket_folder_path) if file.endswith(".txt")]

        if not ticket_files:
            print("没有可用的门票。")
            return

        print("可用的门票：")
        for i, file in enumerate(ticket_files):
            print(f"{i + 1}. {file[:-4]}")

        choice = input("请选择票务编号: ")
        if choice.isdigit() and 1 <= int(choice) <= len(ticket_files):
            ticket_name = ticket_files[int(choice) - 1][:-4]
            self.query_tickets(ticket_name)
        else:
            print("无效的选择，请重试。")


if __name__ == "__main__":
    client = TicketBookingClient("localhost", 8888)

    while True:
        print("1. 查询票务")
        print("2. 预订门票")
        choice = input("请输入您的选择 (1/2): ")

        if choice == "1":
            client.get_available_tickets()
        elif choice == "2":
            booking_info = input("请输入预订信息 (票务名称-用户名称-预订数量): ")
            client.book_tickets(booking_info)
        else:
            print("无效的选择，请重试。")
