# 导入OneApp模块中的create_app函数
from OneApp import create_app

# 判断当前脚本是否作为主程序运行
if __name__ == '__main__':
    # 调用create_app函数创建应用实例
    app = create_app()

    # 以调试模式运行应用，监听本地IP地址127.0.0.1的5000端口
    app.run(debug=True, host='127.0.0.1', port=5000)
