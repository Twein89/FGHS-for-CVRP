'''
Created on 2014/11/11

@author: Administrator
'''
from operator import itemgetter
from file_reader import DIMENSION,vehicle_num
import random
from file_reader import matrix, customers

import copy
from ftplib import FTP



DIMENSION = DIMENSION - 1
CAPACITY =100

def ranked_sol(sol):
    a=[[i+1,sol[i]]for i in range(0,DIMENSION)]
    a=sorted(a, key=itemgetter(1))
    b=[i[0] for i in a] 
    return b

def initial_co_sol():
    sol=[i+1 for i in range(0,DIMENSION)]
    random.shuffle(sol)
    path=initial_vehicle_path(sol)
    co_sol=[]
    UB=1
    for vehicle in path:
        for i in range(0,len(vehicle)-2):
            co_sol.append(random.uniform(UB-1,UB))
        UB=UB+1
    sol=p_to_sol(path,co_sol)       
    return sol

def initial_vehicle_path(sol):
    vehicle=[0]
    path =[]
    capacity = CAPACITY
    for eachNum in sol:
        capacity = capacity - customers[eachNum]['Demand']
        if capacity > 0:
            vehicle.append(eachNum)
        else:
            vehicle.append(0)
            path.append(vehicle)
            vehicle = [0]
            vehicle.append(eachNum)
            capacity = CAPACITY - customers[eachNum]['Demand']
    vehicle.append(0)
    path.append(vehicle)
    return path

def vehicle_path(sol):
    a=[[i+1,sol[i]]for i in range(0,DIMENSION)]
    a=sorted(a, key=itemgetter(1))
    b=[i[0] for i in a]
    vehicle=[0]
    path=[]
    m=0
    for num in b:
        if sol[num-1]<m+1:
            vehicle.append(num)
        else:
            vehicle.append(0)
            path.append(vehicle)
            vehicle=[0]
            vehicle.append(num)
            m=m+1
    vehicle.append(0)
    path.append(vehicle)
    return path

def path_cal(vehicle):
    prior = 0 
    cal =0
    sum=0
    for site in vehicle:
        cal = cal + matrix[site][prior]
        prior = site
        sum=sum+customers[site]['Demand']
    if sum>CAPACITY:
        cal=cal+10000
    return cal       

def path_to_sol(path):
    sol = []
    for vehicle in path:
        sol = sol + vehicle[1:len(vehicle)-1]
    return sol


def fitness(sol):
    path = vehicle_path(sol)
    total_d = 0
    for vehicle in path:
        total_d = total_d + path_cal(vehicle)
    return total_d

def fitness_p(path):
    total_d = 0
    for vehicle in path:
        total_d = total_d + path_cal(vehicle)
    return total_d

def swap(vehicle,i,j):
    head = vehicle[0:i]
    tail = vehicle[j:len(vehicle)]
    rev = vehicle[i:j]
    rev.reverse()
    new_vehicle = head + rev +tail
    return new_vehicle

def swap_opt(vehicle):
    stop = len(vehicle)-1
    score = path_cal(vehicle)
    for i in range(1,stop):
        k=1
        while(k<i):
            if len(vehicle[k:i])>=2:
                new_vehicle = swap(vehicle,k,i)
                cal = path_cal(new_vehicle)
                if cal < score:
                    vehicle = new_vehicle
                    score = cal
            k=k+1
        while(k<stop):
            k=k+1
            if len(vehicle[i:k])>=2:
                new_vehicle = swap(vehicle,i,k)
                cal = path_cal(new_vehicle)
                if cal < score:
                    vehicle = new_vehicle 
                    score = cal          
    return vehicle  
     
def local_search(sol):
    path = vehicle_path(sol)
    new_path = []
    for vehicle in path:
        new_path.append(swap_opt(vehicle))
    new_sol = path_to_sol(new_path)
    return new_sol
def local_search_p(path):
    new_path = []
    for vehicle in path:
        new_path.append(swap_opt(vehicle))
    return new_path
def p_to_sol(path,sol):
    p=path_to_sol(path)
    temp=sorted(sol)
    j=0
    for i in p:
        sol[i-1]=temp[j]
        j=j+1
    return sol
# sol=[1.0391993007700253, 0.04896396445199325, 1.8574099340803432, 0.7952027723968549, 1.4910850221613454, 1.4886231677623527, 0.41075857855953624, 0.8808550412761718]
# print(vehicle_path(sol))
# print (sorted(sol))
# path=vehicle_path(sol)
# p=local_search_p(path)
# print (p)
# sol=p_to_sol(p,sol)
# print (sol)
# print (vehicle_path(sol))
# print (path)
# p=local_search_p(path)
# print (p)
# print (fitness_p(p))
# sol=initial_co_sol()
# path=vehicle_path(sol)
# print(sol)
# print(path)
# print(fitness_p(path))
