from core import main

class ManagementTool(object):
    """
    负责对用户输入的指令进行解析，并调用相应的模块处理

    """

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
        print(self.sys_argv)
        self.verify_argv()

    def verify_argv(self):
        """验证指令是否合法"""
        if len(self.sys_argv) < 2:  # 命令长度不能小于2
            self.help_msg()
        cmd = self.sys_argv[1]
        if not hasattr(self, cmd):
            print("invalid argument!")
            self.help_msg()

    def help_msg(self):
        msg = """
        strat      start FTP server
        stop       stop FTP server
        restrat    restart FTP server
        createuser   username        create a ftp_base user
        """
        exit(msg)

    def execute(self):
        """解析并执行指令"""
        cmd = self.sys_argv[1]
        func = getattr(self, cmd)
        func()

    def start(self):
        """start ftp_base server"""
        server = main.FTPSever(self)
        server.run_forever()

