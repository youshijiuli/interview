import socket
import threading
import os
import json
import time
import stat
from database import UserDatabase
from crypto_utils import CryptoUtils


class FTPServer:
    def __init__(self, host='0.0.0.0', port=2121):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # {socket: {aes_key, current_dir, username}}
        self.online_users = {}  # {username: {socket, addr, aes_key}}
        self.db = UserDatabase()
        self.private_key, self.public_key = CryptoUtils.generate_rsa_keys()
        # 启动服务端消息发送线程
        threading.Thread(target=self.server_message_sender, daemon=True).start()

    def server_message_sender(self):
        """服务端主动发送消息的线程，增强连接状态检查"""
        while True:
            try:
                # 检查是否有在线用户（先清理无效连接）
                self._clean_invalid_users()
                if not self.online_users:
                    print("\n当前暂无用户登录")
                    time.sleep(1)
                    continue

                print("\n在线用户列表：")
                user_list = list(self.online_users.items())
                for i, (user, info) in enumerate(user_list, 1):
                    ip, port = info['addr']
                    print(f"{i}. {user} ({ip}:{port})")
                
                try:
                    choice = input("\n请选择要发送消息的用户编号(输入q退出): ").strip()
                    if choice.lower() == 'q':
                        continue
                    
                    target_index = int(choice) - 1
                    if 0 <= target_index < len(user_list):
                        target_username, target_info = user_list[target_index]
                        # 双重检查用户连接状态
                        if not self._is_user_connected(target_username):
                            print("\n该用户已断开连接")
                            continue
                            
                        message = input(f"请输入要发送给 {target_username} 的消息: ").strip()
                        if message:
                            try:
                                # 三重检查连接有效性
                                if not self._is_user_connected(target_username):
                                    print("\n该用户已断开连接")
                                    continue
                                    
                                # 直接从online_users获取最新信息
                                if target_username in self.online_users:
                                    target_info = self.online_users[target_username]
                                    
                                encrypted_msg = CryptoUtils.encrypt_with_aes(
                                    target_info['aes_key'], 
                                    f"[Server]: {message}".encode()
                                )
                                # 发送前检查套接字可写性
                                target_socket = target_info['socket']
                                # 发送少量数据测试连接
                                # test_data = b"TEST_CONNECTION"
                                # encrypted_test = CryptoUtils.encrypt_with_aes(target_info['aes_key'], test_data)
                                # target_socket.send(encrypted_test)
                                # 等待客户端确认
                                # try:
                                #     target_socket.settimeout(2)
                                #     response = target_socket.recv(1024)
                                #     decrypted_response = CryptoUtils.decrypt_with_aes(target_info['aes_key'], response)
                                #     if decrypted_response != test_data:
                                #         raise ConnectionResetError("Connection test failed")
                                # except:
                                #     raise ConnectionResetError("No response from client")
                                
                                target_socket.send(encrypted_msg)
                                print(f"消息已发送给 {target_username}")
                            except (ConnectionResetError, OSError, socket.timeout) as e:
                                print(f"\n发送消息时连接错误: {e}")
                                self._remove_user(target_username)
                            except Exception as e:
                                print(f"\n发送消息时出错: {e}")
                    else:
                        print("无效的用户编号")
                except ValueError:
                    print("请输入有效的数字")
                except Exception as e:
                    print(f"发送消息时处理错误: {e}")
                time.sleep(1)
            except Exception as e:
                print(f"服务端消息发送线程出错: {e}")
                time.sleep(1)

    def _is_user_connected(self, username):
        """严格检查用户连接是否有效"""
        if username not in self.online_users:
            return False
        try:
            self.online_users[username]['socket'].getpeername()
            return True
        except:
            return False

    def _clean_invalid_users(self):
        """清理无效的用户连接，增强异常处理"""
        users_to_remove = []
        for username in list(self.online_users.keys()):
            if not self._is_user_connected(username):
                users_to_remove.append(username)
        
        for username in users_to_remove:
            self._remove_user(username)

    def _remove_user(self, username):
        """移除用户连接，完善资源释放"""
        if username in self.online_users:
            info = self.online_users[username]
            print(f"\n用户 {username} ({info['addr'][0]}:{info['addr'][1]}) 已断开连接")
            # 关闭套接字
            try:
                info['socket'].shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                info['socket'].close()
            except:
                pass
            # 从字典中移除
            del self.online_users[username]
            # 移除clients中的对应项
            for client_socket, client_info in list(self.clients.items()):
                if client_info['username'] == username:
                    del self.clients[client_socket]
                    break
            # 广播更新
            self.broadcast_online_users()

    def broadcast_online_users(self):
        """广播在线用户列表，添加错误处理"""
        self._clean_invalid_users()
        if not self.online_users:
            return
            
        user_list = list(self.online_users.keys())
        message = f"ONLINE_USERS:{','.join(user_list)}".encode()
        for username in list(self.online_users.keys()):
            info = self.online_users[username]
            try:
                encrypted_msg = CryptoUtils.encrypt_with_aes(info['aes_key'], message)
                info['socket'].send(encrypted_msg)
            except:
                self._remove_user(username)

    def handle_client(self, client_socket):
        try:
            client_socket.send(self.public_key)
            client_addr = client_socket.getpeername()

            encrypted_aes_key = client_socket.recv(1024)
            if not encrypted_aes_key:
                print(f"连接 {client_addr} 接收密钥失败")
                return

            aes_key = CryptoUtils.decrypt_with_rsa(self.private_key, encrypted_aes_key)

            auth_data = client_socket.recv(1024)
            if not auth_data:
                print(f"连接 {client_addr} 接收认证数据失败")
                return

            decrypted_auth = CryptoUtils.decrypt_with_aes(aes_key, auth_data).decode()

            try:
                username, password = decrypted_auth.split(':')
            except ValueError:
                client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, b"AUTH_FAIL"))
                return

            if self.db.verify_user(username, password):
                # 清理旧连接（如果存在）
                if username in self.online_users:
                    old_socket = self.online_users[username]['socket']
                    try:
                        old_socket.shutdown(socket.SHUT_RDWR)
                        old_socket.close()
                    except:
                        pass
                    if old_socket in self.clients:
                        del self.clients[old_socket]
                    del self.online_users[username]
                    print(f"用户 {username} 的旧连接已关闭")
                    self.broadcast_online_users()

                # 添加新连接
                client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, b"AUTH_SUCCESS"))
                self.clients[client_socket] = {
                    'aes_key': aes_key,
                    'current_dir': os.getcwd(),
                    'username': username
                }
                self.online_users[username] = {
                    'socket': client_socket,
                    'addr': client_addr,
                    'aes_key': aes_key
                }
                print(f"用户 {username} ({client_addr[0]}:{client_addr[1]}) 已登录")
                
                # 显示在线用户
                self._clean_invalid_users()
                if self.online_users:
                    print("\n当前在线用户列表：")
                    user_list = list(self.online_users.items())
                    for i, (user, info) in enumerate(user_list, 1):
                        ip, port = info['addr']
                        print(f"{i}. {user} ({ip}:{port})")
                self.broadcast_online_users()
                self.process_commands(client_socket, aes_key)
            else:
                client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, b"AUTH_FAIL"))
        except ConnectionResetError:
            print(f"连接 {client_addr} 被客户端重置")
        except Exception as e:
            print(f"处理客户端连接时出错: {e}")
        finally:
            # 确保移除用户
            for username in list(self.online_users.keys()):
                if self.online_users[username]['socket'] == client_socket:
                    self._remove_user(username)
                    break
            try:
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
            except:
                pass
            if client_socket in self.clients:
                del self.clients[client_socket]

    def process_commands(self, client_socket, aes_key):
        client_info = self.clients[client_socket]
        current_dir = client_info['current_dir']

        while True:
            try:
                client_socket.settimeout(0.5)

                encrypted_cmd = client_socket.recv(4096)
                if not encrypted_cmd:
                    break

                command = CryptoUtils.decrypt_with_aes(aes_key, encrypted_cmd).decode()
                parts = command.split()
                cmd = parts[0].lower() if parts else ""

                response = None

                if cmd == "exit":
                    username = client_info['username']
                    print(f"\n用户 {username} 主动退出登录")
                    self._remove_user(username)
                    break

                elif cmd == "list":
                    files = os.listdir(current_dir)
                    file_list = []
                    for f in files:
                        full_path = os.path.join(current_dir, f)
                        is_dir = os.path.isdir(full_path)
                        size = os.path.getsize(full_path) if not is_dir else 0
                        file_type = "DIR" if is_dir else "FILE"
                        file_info = f"{file_type:<5} {f}"
                        if not is_dir:
                            if size < 1024:
                                size_str = f"{size} B"
                            elif size < 1024 * 1024:
                                size_str = f"{size / 1024:.2f} KB"
                            else:
                                size_str = f"{size / (1024 * 1024):.2f} MB"
                            file_info += f" ({size_str})"
                        file_list.append(file_info)
                    response = "\n".join(file_list).encode()

                # 其他命令处理...（保持不变）
                # ... 中间命令省略，与之前版本一致 ...
                elif cmd == "cd":
                    if len(parts) < 2:
                        response = b"Usage: cd <directory>"
                    else:
                        new_dir = parts[1]
                        base_dir = os.path.abspath(os.getcwd())
                        target_path = os.path.abspath(os.path.join(current_dir, new_dir))

                        if not target_path.startswith(base_dir):
                            response = b"Access denied: cannot access outside server root"
                        elif os.path.isdir(target_path):
                            current_dir = target_path
                            client_info['current_dir'] = current_dir
                            response = f"Current directory: {current_dir}".encode()
                        else:
                            response = b"Directory not found"

                elif cmd == "pwd":
                    response = current_dir.encode()

                elif cmd == "mkdir" and len(parts) > 1:
                    dir_path = os.path.join(current_dir, parts[1])
                    try:
                        os.mkdir(dir_path)
                        response = b"Directory created"
                    except FileExistsError:
                        response = b"Directory already exists"
                    except OSError as e:
                        response = f"Error: {str(e)}".encode()

                elif cmd == "get" and len(parts) > 1:
                    filename = parts[1]
                    filepath = os.path.join(current_dir, filename)
                    # 检查文件是否存在
                    if not os.path.exists(filepath):
                        response = b"File not found"
                        client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))
                        continue
                    if os.path.isdir(filepath):
                        response = b"Cannot download directories"
                        client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))
                        continue
                    # 确保是文件
                    if os.path.isfile(filepath):
                        file_size = os.path.getsize(filepath)
                        # 发送文件大小信息
                        size_info = f"FILE_SIZE:{file_size}".encode()
                        encrypted_size = CryptoUtils.encrypt_with_aes(aes_key, size_info)
                        try:
                            client_socket.sendall(encrypted_size)
                        except (ConnectionResetError, OSError) as e:
                            print(f"Error sending file size: {e}")
                            continue

                        # 文件传输处理
                        start_time = time.time()
                        try:
                            # 即使是0字节文件也打开文件
                            with open(filepath, 'rb') as f:
                                # 读取并发送文件内容
                                while True:
                                    # 检查超时
                                    if time.time() - start_time > 30:
                                        print(f"File transfer timeout for {filename}")
                                        break

                                    chunk = f.read(4096)
                                    if not chunk:
                                        break
                                    encrypted_chunk = CryptoUtils.encrypt_with_aes(aes_key, chunk)
                                    try:
                                        client_socket.sendall(encrypted_chunk)
                                    except (ConnectionResetError, OSError) as e:
                                        print(f"Error sending file chunk: {e}")
                                        break

                            # 等待客户端确认
                            try:
                                client_socket.settimeout(10)
                                end_signal_enc = client_socket.recv(1024)
                                if not end_signal_enc:
                                    response = b"Client disconnected during download"
                                else:
                                    decrypted_signal = CryptoUtils.decrypt_with_aes(aes_key, end_signal_enc)
                                    if decrypted_signal == b"DOWNLOAD_COMPLETE":
                                        response = b"File download successful"
                                    else:
                                        response = b"Download incomplete"
                            except socket.timeout:
                                response = b"Download confirmation timeout"
                            except Exception as e:
                                response = f"Download error: {str(e)}".encode()
                        except Exception as e:
                            response = f"File transfer error: {str(e)}".encode()
                        finally:
                            client_socket.settimeout(None)  # 重置超时设置
                            # 发送最终响应
                            try:
                                client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))
                            except:
                                print(f"Error sending final response for {filename}")

                elif cmd == "put" and len(parts) > 1:
                    filename = parts[1]
                    filepath = os.path.join(current_dir, filename)
                    # 确保接收缓冲区为空
                    try:
                        client_socket.settimeout(0.1)
                        temp = client_socket.recv(1)
                        if temp:
                            # 有残留数据，丢弃
                            client_socket.recv(4095)  # 清空缓冲区
                    except socket.timeout:
                        pass  # 无残留数据正常继续
                    # 接收文件大小
                    try:
                        client_socket.settimeout(5.0)
                        size_info_enc = client_socket.recv(4096)
                        size_info = CryptoUtils.decrypt_with_aes(aes_key, size_info_enc).decode()
                    except Exception as e:
                        response = f"Error receiving file size: {str(e)}".encode()
                        client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))
                        continue
                    # 检查文件大小格式
                    if not size_info.startswith("FILE_SIZE:"):
                        # 添加详细错误日志
                        print(f"Invalid size info: {size_info[:50]}...")
                        response = b"Invalid file transfer"
                        client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))
                        continue
                    file_size = int(size_info.split(":")[1])
                    # 处理0字节文件
                    if file_size == 0:
                        try:
                            open(filepath, 'wb').close()
                            # response = b"File uploaded successfully"
                        except Exception as e:
                            response = f"Error creating file: {str(e)}".encode()
                        # 立即发送响应
                        client_socket.sendall(CryptoUtils.encrypt_with_aes(aes_key, response))
                        continue
                    # 非0字节文件处理
                    received = 0
                    start_time = time.time()
                    with open(filepath, 'wb') as f:
                        while received < file_size:
                            try:
                                client_socket.settimeout(5.0)
                                encrypted_chunk = client_socket.recv(4096)
                                if not encrypted_chunk:
                                    print("Connection closed by client during upload")
                                    break
                                chunk = CryptoUtils.decrypt_with_aes(aes_key, encrypted_chunk)
                                remaining = file_size - received
                                if len(chunk) > remaining:
                                    chunk = chunk[:remaining]
                                f.write(chunk)
                                received += len(chunk)
                                # 添加超时检查（30秒无进展）
                                if time.time() - start_time > 30:
                                    print("File upload timeout")
                                    response = b"Upload timed out"
                                    break
                            except socket.timeout:
                                print("Socket timeout during upload")
                                response = b"Upload timed out"
                                break
                            except Exception as e:
                                print(f"Error receiving file: {e}")
                                response = f"Error receiving file: {str(e)}".encode()
                                break
                    if received == file_size:
                        response = b"File uploaded successfully"
                    else:
                        response = f"File transfer incomplete ({received}/{file_size} bytes)".encode()
                    client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))

                elif cmd == "attrib" and len(parts) > 1:
                    filename = parts[1]
                    filepath = os.path.join(current_dir, filename)
                    if os.path.exists(filepath):
                        stats = os.stat(filepath)
                        attrib = {
                            'size': stats.st_size,
                            'created': time.ctime(stats.st_ctime),
                            'modified': time.ctime(stats.st_mtime),
                            'is_dir': os.path.isdir(filepath),
                            'permissions': stat.filemode(stats.st_mode)
                        }
                        response = json.dumps(attrib).encode()
                    else:
                        response = b"File not found"
                        client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))

                elif cmd == "rename":
                    if len(parts) < 3:
                        response = b"Usage: rename <old_name> <new_name>"
                    else:
                        old_name = parts[1]
                        new_name = parts[2]
                        old_path = os.path.join(current_dir, old_name)
                        new_path = os.path.join(current_dir, new_name)
                        if ".." in old_name or ".." in new_name or "/" in old_name or "\\" in old_name:
                            response = b"Invalid name: cannot contain '..', '/' or '\\'"
                        elif not os.path.exists(old_path):
                            response = b"File/directory not found"
                        elif os.path.exists(new_path):
                            response = b"Target name already exists"
                        else:
                            os.rename(old_path, new_path)
                            response = b"Renamed successfully"

                elif cmd == "create" and len(parts) > 1:
                    filename = parts[1]
                    filepath = os.path.join(current_dir, filename)
                    if os.path.exists(filepath):
                        response = b"Error: File already exists"
                    else:
                        try:
                            with open(filepath, 'w'):
                                pass
                            response = b"File created"
                        except Exception as e:
                            response = f"Error: {str(e)}".encode()

                elif cmd == "add" and len(parts) == 3:
                    username = parts[1]
                    password = parts[2]
                    if self.db.add_user(username, password):
                        response = b"User added successfully"
                    else:
                        response = b"Failed to add user (username may exist)"

                elif cmd == "chat":
                    # 处理聊天命令
                    if len(parts) < 2:
                        response = b"Usage: chat <message>"
                    else:
                        message = " ".join(parts[1:])
                        print(f"\n[新消息] 来自 {client_info['username']}: {message}")
                        response = b"Message received"

                else:
                    response = b"Unknown command"
                # 发送响应
                if response is not None:
                    client_socket.send(CryptoUtils.encrypt_with_aes(aes_key, response))

            except socket.timeout:
                continue
            except (ConnectionResetError, BrokenPipeError):
                print("客户端连接已断开")
                break
            except Exception as e:
                print(f"命令处理出错: {e}")
                break

        # 清理连接
        if client_socket in self.clients:
            del self.clients[client_socket]
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
        except:
            pass

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"FTP Server started on {self.host}:{self.port}")

            while True:
                try:
                    client_socket, addr = self.server_socket.accept()
                    print(f"新连接来自 {addr}")
                    threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
                except KeyboardInterrupt:
                    print("\n服务器正在关闭...")
                    break
                except Exception as e:
                    print(f"接受新连接时出错: {e}")
                    continue
        except Exception as e:
            print(f"启动服务器时出错: {e}")
        finally:
            # 清理所有连接
            for client_socket in list(self.clients.keys()):
                try:
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                except:
                    pass
            try:
                self.server_socket.close()
            except:
                pass
            print("服务器已关闭")
            if self.db:
                self.db.close()


if __name__ == "__main__":
    server = FTPServer()
    try:
        server.start()
    finally:
        if hasattr(server, 'db') and server.db:
            server.db.close()