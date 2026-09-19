from typing import Any
a: list[Any] = []
# value可以是 list[Any] 或者 int
b: dict[str, list[Any] | Any] = {'k1':a,'k2':a}
b['k1'].append(777)
print(b)
b['k1'] = 666
print(b)




# {'k1': [777], 'k2': [777]}
# {'k1': 666, 'k2': [777]}


# b={'k1':[],'k2':[]}
# b['k1'].append(777)
# print(b)
# b['k1']=666
# print(b)
# 输出结果：
# {'k1': [777], 'k2': [777]}
# {'k1': 666, 'k2': [777]}
# {'k1': [777], 'k2': []}
# {'k1': 666, 'k2': []}