# 导入OneApp模块中的create_app函数
from OneApp import create_app

# 当前脚本作为主程序运行时，执行以下代码
if __name__ == '__main__':
    # 调用create_app函数创建一个应用实例
    app = create_app()
    
    # 运行应用，开启调试模式，设置主机地址为本地IP（127.0.0.1），端口号为5000
    app.run(debug=True, host='127.0.0.1', port=5000)
