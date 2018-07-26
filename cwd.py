import os
print(os.listdir(os.getcwd()))
print(os.getcwd())
if 'image' not in os.listdir(os.getcwd()):
    print('1')
    os.makedirs('image')
else:
    print('0')