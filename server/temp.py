import os

x = ['./example.png', 'config.json']

for i in range(len(x)):
    x[i] = os.path.abspath(x[i])
# print(x)
y = os.path.abspath(a) 
# print(os.path.abspath('./configsdf.fjson'))