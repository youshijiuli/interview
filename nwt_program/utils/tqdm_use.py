# from tqdm import tqdm
# import time
#
# for i in tqdm(range(10)):
#     time.sleep(0.5)


# from tqdm import tqdm
# import time
#
# my_list = [1, 2, 3, 4, 5]
# for element in tqdm(my_list):
#     time.sleep(0.5)
#     print(element)
#
# from tqdm import tqdm
# import time
#
# total_iterations = 20
# with tqdm(total=total_iterations,ascii=False,colour='green') as pbar:
#     for i in range(total_iterations):
#         time.sleep(0.2)
#         pbar.update(1)  # 每次更新进度条，增加1个单位的进度
#

from tqdm import tqdm
import time

# 自定义完整格式
for i in tqdm(
    range(10),
    # bar_format="{l_bar}{bar:10}{r_bar}{bar:-10b}",
    bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {unit} {rate_fmt} eta {remaining}',
    # ascii=" >",
    desc="Custom Progress",
    unit="item",
    unit_scale=True,
    colour='magenta',  # 进度条颜色
    ncols=100,         # 进度条宽度
):
    time.sleep(0.5)