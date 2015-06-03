'''

@author: Administrator
'''
import math
import random
from file_reader import DIMENSION
def logistic_map(x):
    x = 4*x*(1-x)
    return x
    
a = random.random()
x = 5*logistic_map(a)
print (x)
def c_sin(x):
    x=0.2*math.sin(2/x)
    return x
def c_list():
    a=[]
    n=random.uniform(-1,1)
    for i in range(0,DIMENSION-1):
        n=c_sin(n)
        a.append(n)
    return a
# for i in range(0,100):
#     a=c_list()
#     print (a)