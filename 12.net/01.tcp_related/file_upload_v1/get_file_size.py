import os

# size = os.path.getsize('./951738511565_.pic.jpg')

base_dir = os.path.dirname(os.path.abspath(__file__))

print(base_dir)

# print(os.listdir(base_dir))

files = os.listdir(base_dir)

for item in files:
    size = os.path.getsize(item)
    print(item,size)

# print(size)
