import sqlite3
import hashlib
import threading


class UserDatabase:
    def __init__(self, db_name='users.db'):
        # 使用线程局部存储确保每个线程有自己的连接
        self.local = threading.local()
        self.db_name = db_name
        self._create_table()
        self._create_default_admin()  # 添加默认管理员账户

    def _get_connection(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_name)
            self.local.cursor = self.local.conn.cursor()
        return self.local.conn, self.local.cursor

    def _create_table(self):
        conn, cursor = self._get_connection()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
        conn.commit()

    def _create_default_admin(self):
        """创建默认管理员账户"""
        conn, cursor = self._get_connection()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        if count == 0:
            # 没有用户时创建默认管理员
            username = "admin"
            password = "admin"  # 默认密码
            hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                               (username, hashed_pwd))
                conn.commit()
                print(f"Created default admin account: {username}/{password}")
            except sqlite3.IntegrityError:
                pass

    def add_user(self, username, password):
        conn, cursor = self._get_connection()
        hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, hashed_pwd))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        conn, cursor = self._get_connection()
        hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        return result and result[0] == hashed_pwd

    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()
            del self.local.conn
            del self.local.cursor