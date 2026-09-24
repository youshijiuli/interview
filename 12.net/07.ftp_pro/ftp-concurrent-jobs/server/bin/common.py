'''公共接口'''
import time
def progress(percent):
    # 进度条
    if percent > 1:
        percent = 1
    res = int(50 * percent) * '>'
    print('\r[%-50s] %d%%' % (res, percent * 100), end='')
