#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ftplib import FTP, error_perm
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText
import threading
import datetime
import socket
import platform
import subprocess

class FTPClient:
    def __init__(self, root):
        self.root = root
        self.root.title("局域网FTP文件交互工具")
        self.root.geometry("1200x700")
        
        # FTP连接变量
        self.ftp = None
        self.connected = False
        self.current_local_dir = os.path.expanduser("~")
        self.current_remote_dir = ""
        self.connection_timeout = 10  # 10秒连接超时
        self.use_passive_mode = tk.BooleanVar(value=True)  # 默认使用被动模式
        
        # 创建主框架
        self.create_widgets()
        
        # 初始化本地文件列表
        self.update_local_files()
    
    def create_widgets(self):
        # 主分割面板
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板 - 本地文件
        self.local_frame = ttk.LabelFrame(self.main_paned, text="本地文件")
        self.main_paned.add(self.local_frame, weight=1)
        
        # 右侧面板 - 远程文件
        self.remote_frame = ttk.LabelFrame(self.main_paned, text="远程文件")
        self.main_paned.add(self.remote_frame, weight=1)
        
        # 底部状态栏
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.status_label = ttk.Label(self.status_frame, text="就绪", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT)
        
        # 连接信息面板
        self.connection_frame = ttk.LabelFrame(self.root, text="FTP服务器连接")
        self.connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 连接信息输入
        conn_input_frame = ttk.Frame(self.connection_frame)
        conn_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(conn_input_frame, text="服务器:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.host_entry = ttk.Entry(conn_input_frame, width=15)
        self.host_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        self.host_entry.insert(0, "127.0.0.1")
        
        ttk.Label(conn_input_frame, text="端口:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.port_entry = ttk.Entry(conn_input_frame, width=5)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        self.port_entry.insert(0, "21")
        
        ttk.Label(conn_input_frame, text="用户名:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.username_entry = ttk.Entry(conn_input_frame, width=10)
        self.username_entry.grid(row=0, column=5, sticky=tk.W, padx=5, pady=2)
        self.username_entry.insert(0, "anonymous")
        
        ttk.Label(conn_input_frame, text="密码:").grid(row=0, column=6, sticky=tk.W, padx=5, pady=2)
        self.password_entry = ttk.Entry(conn_input_frame, width=10, show="*")
        self.password_entry.grid(row=0, column=7, sticky=tk.W, padx=5, pady=2)
        
        # 被动模式选项
        passive_checkbox = ttk.Checkbutton(conn_input_frame, text="被动模式", 
                                         variable=self.use_passive_mode)
        passive_checkbox.grid(row=0, column=8, padx=5, pady=2)
        
        # 连接按钮
        self.connect_button = ttk.Button(conn_input_frame, text="连接", command=self.connect)
        self.connect_button.grid(row=0, column=9, padx=5, pady=2)
        
        self.test_button = ttk.Button(conn_input_frame, text="测试连接", command=self.test_connection)
        self.test_button.grid(row=0, column=10, padx=5, pady=2)
        
        self.disconnect_button = ttk.Button(conn_input_frame, text="断开", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.grid(row=0, column=11, padx=5, pady=2)
        
        # 配置本地文件面板
        self.setup_local_panel()
        
        # 配置远程文件面板
        self.setup_remote_panel()
    
    def setup_local_panel(self):
        # 本地路径显示和导航
        local_path_frame = ttk.Frame(self.local_frame)
        local_path_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(local_path_frame, text="路径:").pack(side=tk.LEFT, padx=2)
        self.local_path_var = tk.StringVar()
        self.local_path_var.set(self.current_local_dir)
        local_path_entry = ttk.Entry(local_path_frame, textvariable=self.local_path_var)
        local_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        local_browse_button = ttk.Button(local_path_frame, text="浏览...", command=self.browse_local_directory)
        local_browse_button.pack(side=tk.LEFT, padx=2)
        
        local_up_button = ttk.Button(local_path_frame, text="上一级", command=self.go_to_parent_local)
        local_up_button.pack(side=tk.LEFT, padx=2)
        
        local_refresh_button = ttk.Button(local_path_frame, text="刷新", command=self.update_local_files)
        local_refresh_button.pack(side=tk.LEFT, padx=2)
        
        # 本地文件树形视图
        local_tree_frame = ttk.Frame(self.local_frame)
        local_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.local_files_tree = ttk.Treeview(local_tree_frame, columns=("size", "modified", "type"))
        self.local_files_tree.heading("#0", text="名称")
        self.local_files_tree.heading("size", text="大小")
        self.local_files_tree.heading("modified", text="修改时间")
        self.local_files_tree.heading("type", text="类型")
        
        self.local_files_tree.column("#0", width=250)
        self.local_files_tree.column("size", width=100)
        self.local_files_tree.column("modified", width=150)
        self.local_files_tree.column("type", width=80)
        
        local_scrollbar_y = ttk.Scrollbar(local_tree_frame, orient=tk.VERTICAL, command=self.local_files_tree.yview)
        self.local_files_tree.configure(yscrollcommand=local_scrollbar_y.set)
        
        local_scrollbar_x = ttk.Scrollbar(local_tree_frame, orient=tk.HORIZONTAL, command=self.local_files_tree.xview)
        self.local_files_tree.configure(xscrollcommand=local_scrollbar_x.set)
        
        self.local_files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        local_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        local_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 双击打开目录或文件
        self.local_files_tree.bind("<Double-1>", self.on_local_double_click)
        
        # 本地文件操作按钮
        local_buttons_frame = ttk.Frame(self.local_frame)
        local_buttons_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(local_buttons_frame, text="上传到服务器", command=self.upload_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(local_buttons_frame, text="创建文件夹", command=self.create_local_directory).pack(side=tk.LEFT, padx=2)
        ttk.Button(local_buttons_frame, text="删除", command=self.delete_local_item).pack(side=tk.LEFT, padx=2)
    
    def setup_remote_panel(self):
        # 远程路径显示和导航
        remote_path_frame = ttk.Frame(self.remote_frame)
        remote_path_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(remote_path_frame, text="路径:").pack(side=tk.LEFT, padx=2)
        self.remote_path_var = tk.StringVar()
        remote_path_entry = ttk.Entry(remote_path_frame, textvariable=self.remote_path_var, state="readonly")
        remote_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        remote_up_button = ttk.Button(remote_path_frame, text="上一级", command=self.go_to_parent_remote)
        remote_up_button.pack(side=tk.LEFT, padx=2)
        
        remote_refresh_button = ttk.Button(remote_path_frame, text="刷新", command=self.update_remote_files)
        remote_refresh_button.pack(side=tk.LEFT, padx=2)
        
        # 远程文件树形视图
        remote_tree_frame = ttk.Frame(self.remote_frame)
        remote_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.remote_files_tree = ttk.Treeview(remote_tree_frame, columns=("size", "modified", "type"))
        self.remote_files_tree.heading("#0", text="名称")
        self.remote_files_tree.heading("size", text="大小")
        self.remote_files_tree.heading("modified", text="修改时间")
        self.remote_files_tree.heading("type", text="类型")
        
        self.remote_files_tree.column("#0", width=250)
        self.remote_files_tree.column("size", width=100)
        self.remote_files_tree.column("modified", width=150)
        self.remote_files_tree.column("type", width=80)
        
        remote_scrollbar_y = ttk.Scrollbar(remote_tree_frame, orient=tk.VERTICAL, command=self.remote_files_tree.yview)
        self.remote_files_tree.configure(yscrollcommand=remote_scrollbar_y.set)
        
        remote_scrollbar_x = ttk.Scrollbar(remote_tree_frame, orient=tk.HORIZONTAL, command=self.remote_files_tree.xview)
        self.remote_files_tree.configure(xscrollcommand=remote_scrollbar_x.set)
        
        self.remote_files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        remote_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        remote_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 双击打开目录或文件
        self.remote_files_tree.bind("<Double-1>", self.on_remote_double_click)
        
        # 远程文件操作按钮
        remote_buttons_frame = ttk.Frame(self.remote_frame)
        remote_buttons_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(remote_buttons_frame, text="下载到本地", command=self.download_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(remote_buttons_frame, text="创建文件夹", command=self.create_remote_directory).pack(side=tk.LEFT, padx=2)
        ttk.Button(remote_buttons_frame, text="删除", command=self.delete_remote_item).pack(side=tk.LEFT, padx=2)
    
    def connect(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # 连接前先禁用连接按钮，防止重复点击
        self.connect_button.config(state=tk.DISABLED)
        self.test_button.config(state=tk.DISABLED)
        
        try:
            self.status_label.config(text=f"正在连接到 {host}:{port}...")
            self.root.update()
            
            # 首先检查主机是否可达
            if not self.is_host_reachable(host):
                self.handle_connection_error(f"无法访问主机 {host}，请检查主机地址或网络连接。")
                return
                
            # 使用单独线程尝试连接，防止UI卡死
            connection_thread = threading.Thread(target=self._connect_thread, 
                                               args=(host, port, username, password))
            connection_thread.daemon = True
            connection_thread.start()
            
            # 显示连接中的进度指示器
            self.show_connection_progress(connection_thread)
            
        except Exception as e:
            self.handle_connection_error(f"连接初始化失败: {str(e)}")
    
    def _connect_thread(self, host, port, username, password):
        """在单独线程中执行连接操作"""
        try:
            self.ftp = FTP()
            self.ftp.connect(host, port, timeout=self.connection_timeout)
            self.ftp.login(username, password)
            
            # 设置FTP模式（主动/被动）
            if self.use_passive_mode.get():
                self.ftp.set_pasv(True)
            else:
                self.ftp.set_pasv(False)
            
            # 将成功标志设为True
            self.connection_success = True
            self.connection_result = "连接成功"
            
        except socket.timeout:
            self.connection_success = False
            self.connection_result = f"连接超时，服务器未响应。请检查主机地址和端口号是否正确。"
        except socket.gaierror:
            self.connection_success = False
            self.connection_result = f"无法解析主机名 {host}。请检查主机地址是否正确。"
        except ConnectionRefusedError:
            self.connection_success = False
            self.connection_result = f"连接被拒绝。请检查FTP服务是否在远程主机上运行，以及端口 {port} 是否正确。"
        except error_perm as e:
            self.connection_success = False
            if "530" in str(e):
                self.connection_result = "用户名或密码错误，无法登录。"
            else:
                self.connection_result = f"FTP权限错误: {str(e)}"
        except Exception as e:
            self.connection_success = False
            self.connection_result = f"连接错误: {str(e)}"
    
    def show_connection_progress(self, connection_thread):
        """显示连接进度，并在连接完成后更新UI"""
        if not hasattr(self, 'connection_success'):
            # 连接还在进行中
            self.status_label.config(text=f"正在连接，请稍候...({self.connection_timeout}秒超时)")
            self.root.after(100, lambda: self.show_connection_progress(connection_thread))
        else:
            # 连接尝试已完成
            if self.connection_success:
                # 连接成功
                self.current_remote_dir = self.ftp.pwd()
                self.remote_path_var.set(self.current_remote_dir)
                
                self.connected = True
                self.connect_button.config(state=tk.DISABLED)
                self.test_button.config(state=tk.DISABLED)
                self.disconnect_button.config(state=tk.NORMAL)
                
                self.status_label.config(text=f"已连接到 {self.host_entry.get()}:{self.port_entry.get()}")
                
                # 更新远程文件列表
                self.update_remote_files()
            else:
                # 连接失败，处理错误
                self.handle_connection_error(self.connection_result)
                
            # 重置连接状态变量
            delattr(self, 'connection_success')
            delattr(self, 'connection_result')
    
    def handle_connection_error(self, error_message):
        """处理连接错误，提供友好的错误信息和恢复选项"""
        self.connect_button.config(state=tk.NORMAL)
        self.test_button.config(state=tk.NORMAL)
        self.status_label.config(text="连接失败")
        
        # 创建自定义错误对话框
        error_window = tk.Toplevel(self.root)
        error_window.title("连接失败")
        error_window.geometry("500x350")
        error_window.transient(self.root)
        error_window.grab_set()
        
        # 添加错误图标
        # 这里可以添加错误图标，如果有的话
        
        # 错误信息
        ttk.Label(error_window, text="连接FTP服务器失败", font=("", 12, "bold")).pack(pady=10)
        
        # 错误详情
        error_frame = ttk.LabelFrame(error_window, text="错误详情")
        error_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        error_text = ScrolledText(error_frame, wrap=tk.WORD, height=6)
        error_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        error_text.insert(tk.END, error_message)
        error_text.config(state=tk.DISABLED)
        
        # 可能的解决方案
        solutions_frame = ttk.LabelFrame(error_window, text="可能的解决方案")
        solutions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        solutions_text = ScrolledText(solutions_frame, wrap=tk.WORD, height=6)
        solutions_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 根据错误类型提供解决方案
        if "超时" in error_message:
            solutions = """
1. 检查服务器地址是否正确
2. 确认FTP服务器是否在运行
3. 检查网络连接是否正常
4. 检查防火墙设置是否阻止了FTP连接
5. 尝试增加连接超时时间
            """
        elif "无法访问主机" in error_message or "无法解析主机名" in error_message:
            solutions = """
1. 检查主机名或IP地址是否正确
2. 确保目标计算机已开机并连接到网络
3. 确认您的计算机已连接到网络
4. 尝试使用IP地址代替主机名
            """
        elif "连接被拒绝" in error_message:
            solutions = """
1. 确认FTP服务在远程主机上正在运行
2. 检查端口号是否正确（默认通常是21）
3. 确认服务器的防火墙允许FTP连接
4. 尝试使用被动模式连接
            """
        elif "用户名或密码错误" in error_message:
            solutions = """
1. 检查用户名和密码是否正确
2. 确认您有权访问该FTP服务器
3. 尝试使用匿名登录（用户名：anonymous，密码留空或使用邮箱）
            """
        else:
            solutions = """
1. 检查FTP服务器地址和端口是否正确
2. 确认FTP服务器是否开启并正常运行
3. 确认网络连接是否正常
4. 检查防火墙设置
5. 联系服务器管理员获取帮助
            """
        
        solutions_text.insert(tk.END, solutions)
        solutions_text.config(state=tk.DISABLED)
        
        # 网络诊断按钮
        buttons_frame = ttk.Frame(error_window)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="网络诊断", 
                  command=lambda: self.run_network_diagnostics(self.host_entry.get(), error_window)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="重试连接", 
                  command=lambda: [error_window.destroy(), self.connect()]).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="关闭", 
                  command=error_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def test_connection(self):
        """测试与FTP服务器的连接而不实际连接"""
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        
        self.status_label.config(text=f"正在测试连接到 {host}:{port}...")
        self.root.update()
        
        # 禁用测试按钮防止重复点击
        self.test_button.config(state=tk.DISABLED)
        
        # 在单独线程中执行测试
        test_thread = threading.Thread(target=self._test_connection_thread, args=(host, port))
        test_thread.daemon = True
        test_thread.start()
        
        # 显示测试进度
        self.show_test_progress(test_thread)
    
    def _test_connection_thread(self, host, port):
        """在单独线程中执行连接测试"""
        try:
            # 检查主机是否可达
            ping_result = self.ping_host(host)
            
            # 测试端口是否开放
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                self.test_success = True
                self.test_result = f"测试成功：主机 {host} 可访问，端口 {port} 开放\n\n"
                if ping_result:
                    self.test_result += f"Ping结果：{ping_result}"
            else:
                self.test_success = False
                self.test_result = f"测试失败：主机 {host} 可能可达，但端口 {port} 未开放\n\n"
                if ping_result:
                    self.test_result += f"Ping结果：{ping_result}"
        except socket.gaierror:
            self.test_success = False
            self.test_result = f"测试失败：无法解析主机名 {host}"
        except Exception as e:
            self.test_success = False
            self.test_result = f"测试失败：{str(e)}"
    
    def show_test_progress(self, test_thread):
        """显示测试进度，并在测试完成后更新UI"""
        if not hasattr(self, 'test_success'):
            # 测试还在进行中
            self.status_label.config(text="正在测试连接，请稍候...")
            self.root.after(100, lambda: self.show_test_progress(test_thread))
        else:
            # 测试已完成
            self.test_button.config(state=tk.NORMAL)
            
            # 创建测试结果对话框
            test_window = tk.Toplevel(self.root)
            test_window.title("连接测试结果")
            test_window.geometry("400x300")
            test_window.transient(self.root)
            test_window.grab_set()
            
            # 测试结果标题
            ttk.Label(test_window, 
                     text="连接测试" + ("成功" if self.test_success else "失败"), 
                     font=("", 12, "bold")).pack(pady=10)
            
            # 测试结果详情
            result_frame = ttk.Frame(test_window)
            result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            result_text = ScrolledText(result_frame, wrap=tk.WORD)
            result_text.pack(fill=tk.BOTH, expand=True)
            result_text.insert(tk.END, self.test_result)
            result_text.config(state=tk.DISABLED)
            
            # 按钮框架
            button_frame = ttk.Frame(test_window)
            button_frame.pack(fill=tk.X, padx=10, pady=10)
            
            if self.test_success:
                ttk.Button(button_frame, text="连接", 
                          command=lambda: [test_window.destroy(), self.connect()]).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(button_frame, text="关闭", 
                      command=test_window.destroy).pack(side=tk.RIGHT, padx=5)
            
            # 更新状态栏
            if self.test_success:
                self.status_label.config(text="连接测试成功")
            else:
                self.status_label.config(text="连接测试失败")
            
            # 重置测试状态变量
            delattr(self, 'test_success')
            delattr(self, 'test_result')
    
    def run_network_diagnostics(self, host, parent_window=None):
        """运行网络诊断并显示结果"""
        if parent_window:
            parent_window.destroy()
        
        # 创建诊断窗口
        diag_window = tk.Toplevel(self.root)
        diag_window.title(f"网络诊断 - {host}")
        diag_window.geometry("600x400")
        diag_window.transient(self.root)
        diag_window.grab_set()
        
        # 诊断结果文本框
        diag_frame = ttk.LabelFrame(diag_window, text="诊断结果")
        diag_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        diag_text = ScrolledText(diag_frame, wrap=tk.WORD)
        diag_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        diag_text.insert(tk.END, f"正在诊断与主机 {host} 的网络连接，请稍候...\n\n")
        
        # 按钮框架
        button_frame = ttk.Frame(diag_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        close_button = ttk.Button(button_frame, text="关闭", command=diag_window.destroy)
        close_button.pack(side=tk.RIGHT)
        
        # 在单独线程中运行诊断
        diag_thread = threading.Thread(target=self._run_diagnostics_thread, 
                                      args=(host, diag_text, close_button))
        diag_thread.daemon = True
        diag_thread.start()
    
    def _run_diagnostics_thread(self, host, text_widget, close_button):
        """在单独线程中运行网络诊断"""
        close_button.config(state=tk.DISABLED)
        
        try:
            # 收集系统信息
            text_widget.insert(tk.END, "==== 系统信息 ====\n")
            text_widget.insert(tk.END, f"操作系统: {platform.system()} {platform.release()}\n")
            text_widget.insert(tk.END, f"Python版本: {platform.python_version()}\n\n")
            text_widget.see(tk.END)
            
            # Ping测试
            text_widget.insert(tk.END, f"==== Ping测试: {host} ====\n")
            ping_result = self.ping_host(host)
            text_widget.insert(tk.END, ping_result + "\n\n")
            text_widget.see(tk.END)
            
            # 路由跟踪
            text_widget.insert(tk.END, f"==== 路由跟踪: {host} ====\n")
            trace_result = self.trace_route(host)
            text_widget.insert(tk.END, trace_result + "\n\n")
            text_widget.see(tk.END)
            
            # 端口扫描 (只扫描FTP相关端口)
            port = int(self.port_entry.get())
            text_widget.insert(tk.END, f"==== 端口扫描: {host}:{port} ====\n")
            port_result = self.scan_port(host, port)
            text_widget.insert(tk.END, port_result + "\n\n")
            text_widget.see(tk.END)
            
            # 诊断完成
            text_widget.insert(tk.END, "==== 诊断完成 ====\n")
            text_widget.insert(tk.END, "如果您仍然无法连接到FTP服务器，请检查以下事项：\n")
            text_widget.insert(tk.END, "1. 确认FTP服务器正在运行\n")
            text_widget.insert(tk.END, "2. 检查防火墙设置\n")
            text_widget.insert(tk.END, "3. 检查用户名和密码是否正确\n")
            text_widget.insert(tk.END, "4. 联系网络管理员获取帮助\n")
            text_widget.see(tk.END)
            
        except Exception as e:
            text_widget.insert(tk.END, f"诊断出错: {str(e)}\n")
        
        finally:
            close_button.config(state=tk.NORMAL)
    
    def ping_host(self, host):
        """Ping主机并返回结果"""
        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "4", host]
            else:  # Linux/Mac
                cmd = ["ping", "-c", "4", host]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()
            
            if error:
                return f"Ping错误: {error}"
            else:
                return output
                
        except Exception as e:
            return f"Ping执行失败: {str(e)}"
    
    def trace_route(self, host):
        """执行路由跟踪并返回结果"""
        try:
            if platform.system().lower() == "windows":
                cmd = ["tracert", "-d", "-w", "1000", host]
            else:  # Linux/Mac
                cmd = ["traceroute", "-n", host]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()
            
            if error:
                return f"路由跟踪错误: {error}"
            else:
                return output
                
        except Exception as e:
            return f"路由跟踪执行失败: {str(e)}"
    
    def scan_port(self, host, port):
        """扫描指定端口是否开放"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return f"端口 {port} 开放"
            else:
                return f"端口 {port} 关闭 (错误码: {result})"
                
        except socket.gaierror:
            return f"无法解析主机名 {host}"
        except Exception as e:
            return f"端口扫描失败: {str(e)}"
    
    def is_host_reachable(self, host):
        """检查主机是否可达"""
        try:
            # 先尝试使用socket连接
            socket.gethostbyname(host)
            return True
        except:
            return False
    
    def disconnect(self):
        """断开与FTP服务器的连接"""
        if self.ftp:
            try:
                self.ftp.quit()
            except:
                self.ftp.close()
            
            self.ftp = None
            self.connected = False
            
            self.connect_button.config(state=tk.NORMAL)
            self.test_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            
            self.remote_files_tree.delete(*self.remote_files_tree.get_children())
            self.remote_path_var.set("")
            
            self.status_label.config(text="已断开连接")
    
    def update_local_files(self):
        self.local_files_tree.delete(*self.local_files_tree.get_children())
        
        try:
            self.local_path_var.set(self.current_local_dir)
            
            # 添加上一级目录
            parent_dir = os.path.dirname(self.current_local_dir)
            if self.current_local_dir != parent_dir:  # 不是根目录
                self.local_files_tree.insert("", "end", text="..", values=("", "", "目录"), tags=("dir",))
            
            # 列出所有文件和目录
            for item in os.listdir(self.current_local_dir):
                fullpath = os.path.join(self.current_local_dir, item)
                try:
                    stat_info = os.stat(fullpath)
                    size = stat_info.st_size
                    modified = datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    
                    if os.path.isdir(fullpath):
                        self.local_files_tree.insert("", "end", text=item, values=(f"{size:,} 字节", modified, "目录"), tags=("dir",))
                    else:
                        self.local_files_tree.insert("", "end", text=item, values=(f"{size:,} 字节", modified, "文件"), tags=("file",))
                except Exception as e:
                    print(f"无法访问 {fullpath}: {e}")
            
            self.status_label.config(text=f"本地目录: {self.current_local_dir}")
            
        except Exception as e:
            messagebox.showerror("错误", f"读取本地目录时出错: {str(e)}")
    
    def update_remote_files(self):
        if not self.connected:
            return
        
        self.remote_files_tree.delete(*self.remote_files_tree.get_children())
        
        try:
            self.current_remote_dir = self.ftp.pwd()
            self.remote_path_var.set(self.current_remote_dir)
            
            # 添加上一级目录
            if self.current_remote_dir != "/":
                self.remote_files_tree.insert("", "end", text="..", values=("", "", "目录"), tags=("dir",))
            
            # 获取目录列表
            dir_list = []
            self.ftp.dir(".", dir_list.append)
            
            # 分析目录列表
            for line in dir_list:
                parts = line.split(None, 8)
                if len(parts) >= 9:
                    perms, _, _, _, size, month, day, time_or_year, name = parts
                    
                    # 判断是否为目录
                    is_dir = perms.startswith("d")
                    
                    # 添加到树形视图
                    if is_dir:
                        self.remote_files_tree.insert("", "end", text=name, values=(size, f"{month} {day} {time_or_year}", "目录"), tags=("dir",))
                    else:
                        self.remote_files_tree.insert("", "end", text=name, values=(size, f"{month} {day} {time_or_year}", "文件"), tags=("file",))
            
            self.status_label.config(text=f"远程目录: {self.current_remote_dir}")
            
        except Exception as e:
            messagebox.showerror("错误", f"读取远程目录时出错: {str(e)}")
    
    def on_local_double_click(self, event):
        selected_item = self.local_files_tree.selection()
        if not selected_item:
            return
        
        item_text = self.local_files_tree.item(selected_item, "text")
        
        if item_text == "..":
            self.go_to_parent_local()
            return
        
        values = self.local_files_tree.item(selected_item, "values")
        if values[2] == "目录":
            new_path = os.path.join(self.current_local_dir, item_text)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_local_dir = new_path
                self.update_local_files()
    
    def on_remote_double_click(self, event):
        if not self.connected:
            return
        
        selected_item = self.remote_files_tree.selection()
        if not selected_item:
            return
        
        item_text = self.remote_files_tree.item(selected_item, "text")
        
        if item_text == "..":
            self.go_to_parent_remote()
            return
        
        values = self.remote_files_tree.item(selected_item, "values")
        if values[2] == "目录":
            try:
                self.ftp.cwd(item_text)
                self.update_remote_files()
            except Exception as e:
                messagebox.showerror("错误", f"无法打开远程目录: {str(e)}")
    
    def go_to_parent_local(self):
        parent_dir = os.path.dirname(self.current_local_dir)
        if self.current_local_dir != parent_dir:  # 不是根目录
            self.current_local_dir = parent_dir
            self.update_local_files()
    
    def go_to_parent_remote(self):
        if not self.connected:
            return
        
        if self.current_remote_dir != "/":
            try:
                self.ftp.cwd("..")
                self.update_remote_files()
            except Exception as e:
                messagebox.showerror("错误", f"无法切换到上级目录: {str(e)}")
    
    def browse_local_directory(self):
        dir_path = filedialog.askdirectory(initialdir=self.current_local_dir)
        if dir_path:
            self.current_local_dir = dir_path
            self.update_local_files()
    
    def create_local_directory(self):
        dir_name = simpledialog.askstring("创建目录", "请输入新目录名称:")
        if dir_name:
            new_dir_path = os.path.join(self.current_local_dir, dir_name)
            try:
                os.makedirs(new_dir_path, exist_ok=True)
                self.update_local_files()
            except Exception as e:
                messagebox.showerror("错误", f"无法创建目录: {str(e)}")
    
    def create_remote_directory(self):
        if not self.connected:
            return
        
        dir_name = simpledialog.askstring("创建远程目录", "请输入新目录名称:")
        if dir_name:
            try:
                self.ftp.mkd(dir_name)
                self.update_remote_files()
            except error_perm as e:
                if "550" in str(e):
                    messagebox.showerror("权限错误", 
                                      "无法创建远程目录: 权限被拒绝\n\n"
                                      "可能的原因:\n"
                                      "1. 您的用户账户没有创建目录的权限\n"
                                      "2. 如果使用匿名账户，服务器可能不允许目录创建\n"
                                      "3. 服务器可能设置为只读访问\n\n"
                                      "建议解决方法:\n"
                                      "1. 使用具有适当权限的账户登录\n"
                                      "2. 联系服务器管理员获取权限\n"
                                      "3. 尝试切换FTP连接模式（主动/被动）")
                else:
                    messagebox.showerror("错误", f"无法创建远程目录: {str(e)}")
            except Exception as e:
                messagebox.showerror("错误", f"无法创建远程目录: {str(e)}")
    
    def delete_local_item(self):
        selected_items = self.local_files_tree.selection()
        if not selected_items:
            return
        
        for item_id in selected_items:
            item_text = self.local_files_tree.item(item_id, "text")
            if item_text == "..":
                continue
            
            item_path = os.path.join(self.current_local_dir, item_text)
            
            try:
                if os.path.isdir(item_path):
                    confirm = messagebox.askyesno("确认删除", f"确定要删除目录 '{item_text}' 及其所有内容吗?")
                    if confirm:
                        import shutil
                        shutil.rmtree(item_path)
                else:
                    confirm = messagebox.askyesno("确认删除", f"确定要删除文件 '{item_text}' 吗?")
                    if confirm:
                        os.remove(item_path)
            except Exception as e:
                messagebox.showerror("错误", f"无法删除 '{item_text}': {str(e)}")
        
        self.update_local_files()
    
    def delete_remote_item(self):
        if not self.connected:
            return
        
        selected_items = self.remote_files_tree.selection()
        if not selected_items:
            return
        
        for item_id in selected_items:
            item_text = self.remote_files_tree.item(item_id, "text")
            if item_text == "..":
                continue
            
            item_type = self.remote_files_tree.item(item_id, "values")[2]
            
            try:
                if item_type == "目录":
                    confirm = messagebox.askyesno("确认删除", f"确定要删除远程目录 '{item_text}' 吗?")
                    if confirm:
                        self.ftp.rmd(item_text)
                else:
                    confirm = messagebox.askyesno("确认删除", f"确定要删除远程文件 '{item_text}' 吗?")
                    if confirm:
                        self.ftp.delete(item_text)
            except Exception as e:
                messagebox.showerror("错误", f"无法删除远程项目 '{item_text}': {str(e)}")
        
        self.update_remote_files()
    
    def upload_selected(self):
        if not self.connected:
            messagebox.showwarning("未连接", "请先连接到FTP服务器")
            return
        
        selected_items = self.local_files_tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请选择要上传的文件或目录")
            return
        
        for item_id in selected_items:
            item_text = self.local_files_tree.item(item_id, "text")
            if item_text == "..":
                continue
            
            item_path = os.path.join(self.current_local_dir, item_text)
            item_type = self.local_files_tree.item(item_id, "values")[2]
            
            if item_type == "文件":
                self.upload_file(item_path, item_text)
            else:
                messagebox.showinfo("提示", f"目录上传尚未实现: {item_text}")
        
        self.update_remote_files()
    
    def upload_file(self, local_path, remote_filename):
        try:
            self.status_label.config(text=f"正在上传: {remote_filename}...")
            self.root.update()
            
            with open(local_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {remote_filename}', file)
            
            self.status_label.config(text=f"上传完成: {remote_filename}")
        except error_perm as e:
            if "550" in str(e):
                messagebox.showerror("权限错误", 
                                  f"上传文件失败: 权限被拒绝\n\n"
                                  f"文件: {remote_filename}\n\n"
                                  f"可能的原因:\n"
                                  f"1. 您的用户账户没有上传文件的权限\n"
                                  f"2. 如果使用匿名账户，服务器可能不允许文件上传\n"
                                  f"3. 服务器可能设置为只读访问\n"
                                  f"4. 远程目录可能没有写入权限\n\n"
                                  f"建议解决方法:\n"
                                  f"1. 使用具有适当权限的账户登录\n"
                                  f"2. 联系服务器管理员获取权限\n"
                                  f"3. 尝试切换FTP连接模式（主动/被动）")
            else:
                messagebox.showerror("上传错误", f"上传文件失败: {str(e)}")
            self.status_label.config(text=f"上传失败: {remote_filename}")
        except Exception as e:
            messagebox.showerror("上传错误", f"上传文件失败: {str(e)}")
            self.status_label.config(text=f"上传失败: {remote_filename}")
    
    def download_selected(self):
        if not self.connected:
            return
        
        selected_items = self.remote_files_tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请选择要下载的文件")
            return
        
        for item_id in selected_items:
            item_text = self.remote_files_tree.item(item_id, "text")
            if item_text == "..":
                continue
            
            item_type = self.remote_files_tree.item(item_id, "values")[2]
            
            if item_type == "文件":
                local_path = os.path.join(self.current_local_dir, item_text)
                self.download_file(item_text, local_path)
            else:
                messagebox.showinfo("提示", f"目录下载尚未实现: {item_text}")
        
        self.update_local_files()
    
    def download_file(self, remote_filename, local_path):
        try:
            self.status_label.config(text=f"正在下载: {remote_filename}...")
            self.root.update()
            
            with open(local_path, 'wb') as file:
                self.ftp.retrbinary(f'RETR {remote_filename}', file.write)
            
            self.status_label.config(text=f"下载完成: {remote_filename}")
        except Exception as e:
            messagebox.showerror("下载错误", f"下载文件失败: {str(e)}")
            self.status_label.config(text=f"下载失败: {remote_filename}")

def main():
    root = tk.Tk()
    app = FTPClient(root)
    root.mainloop()

if __name__ == "__main__":
    main() 