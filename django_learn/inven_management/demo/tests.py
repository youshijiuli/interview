from django.test import TestCase
import matplotlib.pyplot as plt
# Create your tests here.

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
# 绘制折线图
plt.plot(x, y)
# 保存图像文件到指定路径
save_path = '/templates/static/chart1.png'  # 替换为你想要保存的文件路径
plt.savefig('chart.png')
print("ok")
