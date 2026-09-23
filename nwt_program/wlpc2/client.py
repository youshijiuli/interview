import os
import socket
import sys
import threading
import getpass
from crypto_utils import CryptoUtils
import time


class FTPClient:
    def __init__(self, host='127.0.0.1', port=2121):
        self.file_transfer_active = False  # 文件传输状态标志
        self.chat_lock = threading.Lock()  # 聊天显示锁
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.aes_key = None
        self.connected = False
        self.online_users = []  # 存储在线用户列表

    def connect(self):
        self.sock.connect((self.host, self.port))

        # 接收服务器公钥
        server_public_key = self.sock.recv(4096)

        # 生成并发送AES密钥
        self.aes_key = CryptoUtils.generate_aes_key()
        encrypted_aes_key = CryptoUtils.encrypt_with_rsa(server_public_key, self.aes_key)
        self.sock.send(encrypted_aes_key)

        # 用户认证
        username = input("Username: ")
        password = self.get_password_with_asterisk("Password: ")
        auth_data = f"{username}:{password}".encode()
        encrypted_auth = CryptoUtils.encrypt_with_aes(self.aes_key, auth_data)
        self.sock.send(encrypted_auth)

        # 验证认证结果
        response = CryptoUtils.decrypt_with_aes(self.aes_key, self.sock.recv(1024))
        if response == b"AUTH_SUCCESS":
            print("Authentication successful")
            self.connected = True
            self.start_chat_thread()  # 启动聊天监听线程
            self.run_command_loop()
        else:
            print("Authentication failed")
            self.sock.close()

    def get_password_with_asterisk(self, prompt=''):
        if sys.platform.startswith('win'):
            import msvcrt
            print(prompt, end='', flush=True)
            password_chars = []
            while True:
                ch = msvcrt.getch()
                if ch in (b'\r', b'\n'):
                    print()
                    break
                elif ch == b'\x08':
                    if password_chars:
                        password_chars.pop()
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    if 32 <= ch[0] <= 126:
                        password_chars.append(ch)
                        sys.stdout.write('*')
                        sys.stdout.flush()
            return b''.join(password_chars).decode('utf-8')
        else:
            return getpass.getpass(prompt)

    def send_command(self, command):
        encrypted_cmd = CryptoUtils.encrypt_with_aes(self.aes_key, command.encode())
        self.sock.send(encrypted_cmd)

        # 接收响应
        encrypted_resp = self.sock.recv(4096)
        response = CryptoUtils.decrypt_with_aes(self.aes_key, encrypted_resp).decode()
        return response

    def run_command_loop(self):
        while self.connected:
            try:
                self.clear_socket_buffer()
                command = input("ftp_base> ").strip()
                if not command:
                    continue

                if command.lower() == "help" or command.lower() == "?":
                    self.show_help()
                    continue

                if command.lower() == "exit":
                    # 优雅地关闭连接
                    self.connected = False
                    try:
                        self.sock.shutdown(socket.SHUT_RDWR)
                    except:
                        pass
                    self.sock.close()
                    break

                if command.lower() == "users":
                    print("\n在线用户列表：")
                    for i, user in enumerate(self.online_users, 1):
                        print(f"{i}. {user}")
                    continue

                if command.startswith("get "):
                    self.handle_file_download(command)
                    continue

                if command.startswith("put "):
                    self.handle_file_upload(command)
                    continue

                if command.startswith("chat "):
                    # 直接发送加密后的命令，不等待响应
                    encrypted_cmd = CryptoUtils.encrypt_with_aes(self.aes_key, command.encode())
                    self.sock.send(encrypted_cmd)
                    continue

                # 特殊处理目录变更命令
                if command.lower().startswith("cd "):
                    # 修复：直接发送命令而不是使用send_command
                    encrypted_cmd = CryptoUtils.encrypt_with_aes(self.aes_key, command.encode())
                    self.sock.send(encrypted_cmd)

                    # 设置5秒超时接收响应
                    self.sock.settimeout(5.0)
                    try:
                        encrypted_resp = self.sock.recv(4096)
                        response = CryptoUtils.decrypt_with_aes(self.aes_key, encrypted_resp).decode()
                        print(response)
                    except socket.timeout:
                        print("cd: server response timeout")
                    except Exception as e:
                        print(f"cd: error receiving response: {e}")
                    finally:
                        self.sock.settimeout(None)  # 重置超时
                    continue

                # 普通命令处理
                encrypted_cmd = CryptoUtils.encrypt_with_aes(self.aes_key, command.encode())
                self.sock.send(encrypted_cmd)

                try:
                    # 设置接收超时
                    encrypted_resp = self.sock.recv(4096)
                    response = CryptoUtils.decrypt_with_aes(self.aes_key, encrypted_resp).decode()
                    print(response)
                except socket.timeout:
                    print("Server response timeout")

            except KeyboardInterrupt:
                self.connected = False
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                self.sock.close()
                break
            except Exception as e:
                print(f"Error: {e}")
                self.connected = False
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                self.sock.close()
                break

        self.connected = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.sock.close()

    def show_help(self):
        help_text = """
        FTP Client Commands:
        --------------------
        list                - List current directory contents
        cd <directory>      - Change current directory
        pwd                 - Show current working directory
        mkdir <dirname>     - Create new directory
        get <filename>      - Download file
        put <filename>      - Upload file
        rename <old> <new>  - Rename file/directory
        attrib <filename>   - View file attributes
        create <filename>   - Create empty file
        chat <message>      - Send message to server
        users               - Show online users
        add <user> <pass>   - Add new user (admin only)
        exit                - Exit client
        help                - Show this help
        """
        print(help_text)

    def handle_file_download(self, command):
        # 临时禁用聊天监听
        if not self.chat_lock.acquire(timeout=5):
            print("无法获取锁，下载操作被延迟")
            return
            
        try:
            self.file_transfer_active = True
            filename = command.split()[1]
            encrypted_cmd = CryptoUtils.encrypt_with_aes(self.aes_key, command.encode())
            self.sock.send(encrypted_cmd)

            # 接收响应
            size_info_enc = self.sock.recv(4096)
            try:
                size_info = CryptoUtils.decrypt_with_aes(self.aes_key, size_info_enc).decode()

                # 检查是否是错误消息
                if "not found" in size_info or "error" in size_info.lower():
                    print(f"\nError: {size_info}")
                    return

                file_size = int(size_info.split(":")[1])
                print(f"Downloading {filename} ({file_size} bytes)")

                # 处理同名文件
                if os.path.exists(filename):
                    # 生成带时间戳的文件名
                    name, ext = os.path.splitext(filename)
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    new_filename = f"{name}_{timestamp}{ext}"
                    print(f"File {filename} already exists, saving as {new_filename}")
                    filename = new_filename

            except Exception as e:
                print(f"Decrypt size info error: {e}")
                try:
                    error_msg = size_info_enc.decode('utf-8', errors='replace')
                    print(f"Server response: {error_msg}")
                except:
                    print("Received non-UTF8 response from server")
                return

            if not size_info.startswith("FILE_SIZE:"):
                print("File transfer error:", size_info)
                return

            file_size = int(size_info.split(":")[1])
            temp_filename = filename + ".tmp"
            
            try:
                # 创建临时文件
                with open(temp_filename, 'wb') as f:
                    received = 0
                    start_time = time.time()
                    
                    # 即使是0字节文件也进入循环
                    while received < file_size:
                        # 添加超时检查（30秒无进展）
                        if time.time() - start_time > 30:
                            print("\nDownload timed out")
                            return

                        # 接收数据（不固定大小）
                        encrypted_chunk = self.sock.recv(4096)
                        if not encrypted_chunk:
                            break

                        try:
                            chunk = CryptoUtils.decrypt_with_aes(self.aes_key, encrypted_chunk)
                        except Exception as e:
                            print(f"\nDecrypt error: {e}")
                            continue

                        # 确保不写入超过文件大小的数据
                        write_size = min(len(chunk), file_size - received)
                        f.write(chunk[:write_size])
                        f.flush()  # 确保数据写入磁盘
                        received += write_size

                        print(f"Downloaded {received}/{file_size} bytes ({received / file_size:.1%})",
                              end='\r', flush=True)

                        # 检查是否已完成
                        if received >= file_size:
                            break

                # 验证文件大小
                if os.path.getsize(temp_filename) != file_size:
                    print(f"\nError: Downloaded file size ({os.path.getsize(temp_filename)}) does not match expected size ({file_size})")
                    os.remove(temp_filename)  # 删除不完整的文件
                    return

                # 如果下载成功，重命名临时文件
                if os.path.exists(filename):
                    os.remove(filename)
                os.rename(temp_filename, filename)

                # 发送下载完成确认
                self.sock.send(CryptoUtils.encrypt_with_aes(self.aes_key, b"DOWNLOAD_COMPLETE"))

                # 接收服务器响应
                response_enc = self.sock.recv(4096)
                if not response_enc:
                    print("\nServer disconnected during download")
                    return
                    
                try:
                    response = CryptoUtils.decrypt_with_aes(self.aes_key, response_enc).decode()
                    print(f"\n{response}")
                except Exception as e:
                    print(f"\nError receiving download response: {e}")

            except Exception as e:
                print(f"\nError during file download: {e}")
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                return

        except Exception as e:
            print(f"\nError in file download process: {e}")
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        finally:
            self.file_transfer_active = False
            self.chat_lock.release()

    def handle_file_upload(self, command):
        try:
            if not self.connected:
                print("Not connected to server")
                return

            filename = command.split()[1]
            if not os.path.isfile(filename):
                print(f"File not found: {filename}")
                return

            file_size = os.path.getsize(filename)

            # 发送命令
            encrypted_cmd = CryptoUtils.encrypt_with_aes(self.aes_key, command.encode())
            self.sock.send(encrypted_cmd)

            # 清空可能存在的旧响应
            self.clear_socket_buffer()

            # 发送文件大小
            size_info = f"FILE_SIZE:{file_size}".encode()
            encrypted_size = CryptoUtils.encrypt_with_aes(self.aes_key, size_info)
            self.sock.send(encrypted_size)

            # 处理0字节文件
            if file_size == 0:
                print(f"Uploaded 0/0 bytes (100%)")
                try:
                    self.sock.settimeout(10)
                    response_enc = self.sock.recv(4096)
                    if response_enc:
                        response = CryptoUtils.decrypt_with_aes(self.aes_key, response_enc).decode()
                        print(f"\n{response}")
                    else:
                        print("\nReceived empty response from server")
                except socket.timeout:
                    print("\nServer response timeout")
                return

            # 非0字节文件处理
            with self.chat_lock:
                print(f"Uploading {filename} ({file_size} bytes)")

            # 发送文件内容
            sent = 0
            start_time = time.time()
            with open(filename, 'rb') as f:
                while sent < file_size:
                    # 添加超时检查（30秒无进展）
                    if time.time() - start_time > 30:
                        print("\nUpload timed out")
                        return

                    chunk = f.read(4096)
                    if not chunk:
                        break

                    encrypted_chunk = CryptoUtils.encrypt_with_aes(self.aes_key, chunk)
                    self.sock.sendall(encrypted_chunk)  # 使用sendall确保发送
                    sent += len(chunk)
                    with self.chat_lock:
                        print(f"Uploaded {sent}/{file_size} bytes", end='\r')

            # 等待服务器确认
            try:
                self.sock.settimeout(30)
                response_enc = self.sock.recv(4096)
                if response_enc:
                    response = CryptoUtils.decrypt_with_aes(self.aes_key, response_enc).decode()
                    with self.chat_lock:
                        print(f"\n{response}")
                else:
                    with self.chat_lock:
                        print("\nReceived empty response from server")
            except socket.timeout:
                with self.chat_lock:
                    print("\nServer response timeout")

        except Exception as e:
            with self.chat_lock:
                print(f"\nUpload error: {str(e)}")
        finally:
            self.file_transfer_active = False

    def chat_listener(self):
        import select
        while self.connected:
            # 如果文件传输活跃，等待一段时间后继续
            if self.file_transfer_active:
                time.sleep(0.5)
                continue

            try:
                # 使用select监听socket，设置0.5秒超时
                rlist, _, _ = select.select([self.sock], [], [], 0.5)
                if self.sock in rlist:
                    try:
                        # 获取锁
                        if not self.chat_lock.acquire(blocking=False):
                            continue

                        try:
                            encrypted_msg = self.sock.recv(4096)
                            if not encrypted_msg:
                                break

                            try:
                                decrypted_data = CryptoUtils.decrypt_with_aes(self.aes_key, encrypted_msg)
                                message = decrypted_data.decode('utf-8', errors='replace')

                                # 处理在线用户列表更新
                                if message.startswith("ONLINE_USERS:"):
                                    # self.online_users = message[13:].split(',')
                                    print("\n有新用户上线啦")
                                    # for i, user in enumerate(self.online_users, 1):
                                        # print(f"{i}. {user}")
                                    # print("ftp_base> ", end='', flush=True)
                                else:
                                    # 打印普通消息
                                    print(f"\n{message}")
                                    print("ftp_base> ", end='', flush=True)
                            except Exception as e:
                                if self.connected:  # 只在连接状态下打印错误
                                    print(f"\n消息解密或解码错误: {e}")
                                    print("ftp_base> ", end='', flush=True)
                        except socket.error as e:
                            # 忽略超时错误
                            if "timed out" not in str(e) and self.connected:
                                print(f"\n接收消息时发生错误: {e}")
                                print("ftp_base> ", end='', flush=True)
                    finally:
                        # 确保锁被释放
                        self.chat_lock.release()
            except Exception as e:
                if self.connected:  # 只在连接状态下打印错误
                    print(f"\n监听线程发生错误: {e}")
                    print("ftp_base> ", end='', flush=True)
                time.sleep(1)  # 发生错误时等待一秒再继续

    def is_likely_text(self, data):
        """检查数据是否可能是文本"""
        if not data:
            return False
        text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        return bool(data.translate(None, text_chars))

    def start_chat_thread(self):
        threading.Thread(target=self.chat_listener, daemon=True).start()

    def clear_socket_buffer(self):
        """清空套接字接收缓冲区"""
        self.sock.settimeout(0.1)  # 设置短暂超时
        try:
            while True:
                data = self.sock.recv(4096)
                if not data:
                    break
                # 可选：添加调试输出
                # print(f"Cleared buffer: {len(data)} bytes")
        except socket.timeout:
            pass  # 超时表示缓冲区已空
        finally:
            self.sock.settimeout(None)  # 重置超时设置

if __name__ == "__main__":
    client = FTPClient()
    client.connect()