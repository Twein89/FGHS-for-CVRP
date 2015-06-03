from operator import itemgetter
from file_reader import DIMENSION,vehicle_num
import random
import math
import time
from logistic_map import c_list, logistic_map

# from pso import swarm
import vrp_sol
from vrp_sol import fitness,vehicle_path, local_search_p,p_to_sol,initial_co_sol


DIMENSION = DIMENSION-1
HMCR = 0.9
PAR = 0.2
MAXH = 100000
hm_size=30

PAR_max=0.3
PAR_min=0.1
bw_max=0.3
bw_min=0.1

C_max=0.5
C_min=0.1




def initial_hm(size):
    hm=[]
    for i in range(size):
        x=[]
        h=initial_co_sol()
        x.append(h)
        x.append(fitness(h))
        hm.append(x)
    return hm 
def c_initial_hm(size):
    hm=[]
    for i in range(size):
        x=[]
        h=initial_sol()
        x.append(h)
        x.append(fitness(h))
        hm.append(x)
    return hm 

def initial_sol():
#     sol=[[i,random.uniform(0,vehicle_num)]for i in range(1,DIMENSION+1)]
    sol=[random.uniform(0,vehicle_num)for i in range(1,DIMENSION+1)]
    return sol

def initial_int_sol():
    sol=[i+1 for i in range(0,DIMENSION)]
    random.shuffle(sol)
    return sol

# def initial_hm(size):
#     hm=[]
#     for i in range(size):
#         x=[]
#         h=initial_sol()
#         x.append(h)
#         x.append(fitness(h))
#         hm.append(x)
#     return hm 


def random_choice():
    x=random.uniform(0,vehicle_num)
    return x

def hm_choice(hm, i):
    x=hm[random.randint(0,hm_size-1)][0][i]
    return x

def d(a,b):
    c=[(a[i]-b[i])**2 for i in range(0,DIMENSION)]
    d=sum(c)
    return d

def beta(a,b):
    beta=1*math.exp((-1)*d(a,b))
    return beta

def light(a,b,i):
    li=i*math.exp(-1*math.sqrt(d(a,b)))
    return li


def improvisation(hm,gb,t):
#     PART=PAR_min+(PAR_max-PAR_min)/MAXH*t
#     BWT=bw_max*math.exp(math.log(bw_min/bw_max,math.e)/MAXH*t)
#SGHS BWT
#     BWT=bw_max-(bw_max-bw_min)/MAXH*t
    newh = []
    for i in range(DIMENSION):
        if random.random() > HMCR:
            x = random_choice()
        else:
#             x = hm_choice(hm, i)
            index=random.randint(0,hm_size-1)
            x=hm[index][0][i]
#SGHS HMCR
#             x=hm[index][0][i]+BWT*random.uniform(-1,1)
#             if x<0:
#                 x = 0
#             elif x>vehicle_num:
#                 x = vehicle_num
            if  random.random() < PAR:
#HS
#                 x=x+0.2*random.uniform(-1,1)
#                 if x<0:
#                     x = 0
#                 elif x>vehicle_num:
#                     x = vehicle_num
#GHS             
#                 x=gb[random.randint(0,DIMENSION-1)]


#FGHS
                x=x+beta(gb,hm[index][0])*(gb[i]-x)+0.3*(random.uniform(0,1)-0.5)
                if x<0:
                    x = 0
                elif x>vehicle_num:
                    x = vehicle_num
#                 x=gb[i]
                
        newh.append(x)    
    return newh


def NGHS_improvisation(hm,gb):
    newh=[]
    for i in range(DIMENSION):
        xw=hm[hm_size-1][0][i]
        xr=2*gb[i]-xw
        if xr < 0:
            xr=0
        elif xr>vehicle_num:
            xr=vehicle_num
        x=xw+random.random()*(xr-xw)
        if random.random()<0.1:
            x=random_choice()
        newh.append(x)
    return newh

def EGHS_improvisation(hm,gb,t):
    newh=[]
    C=C_max-(t/MAXH)*(C_max-C_min)
    for i in range(DIMENSION):
        xb=gb[i]
        xw=hm[hm_size-1][0][i]
        if random.random()<0.9:
            x=xb-C*random.random()*(xb-xw)
        else:
            x=random_choice()
        newh.append(x)
    return newh

def EFGHS_improvisation(hm,gb,t):
    newh=[]
#     C=C_max-(t/MAXH)*(C_max-C_min)
    
    for i in range(DIMENSION):
        xb=gb[i]
        index=random.randint(0,hm_size-1)
        xw=hm[index][0][i]
        if random.random()<0.9:
            x=xw+beta(gb,hm[index][0])*(gb[i]-xw)+0.3*(random.uniform(0,1)-0.5)
            if x<0:
                x = 0
            elif x>vehicle_num:
                x = vehicle_num
        else:
            x=random_choice()
        newh.append(x)
    return newh

def NGHS_update_hm(hm,newh,fitness):
    index = len(hm)-1
    hm[index][0] = newh
    hm[index][1] = fitness



def update_hm(hm,newh,fitness):
    index = len(hm)-1
    if fitness < hm[index][1]:
        hm[index][0] = newh
        hm[index][1] = fitness

# def main():
hm=initial_hm(hm_size)   
for i in hm:
    print (i)  
tic = time.clock() 

q=random.random() 

for i in range(MAXH):
    if i%1000==0:
        print (hm[0][1])
    hm = sorted(hm,key = itemgetter(1))       
    gb = hm[0][0]     
# restart HM        
#     if hm[0][1]==hm[hm_size-15][1] :
#         new_hm=c_initial_hm(hm_size)
#         new_hm[0]=hm[0]
#         print (new_hm[0])
#         print (i)
#         hm=new_hm

#     new_harmony = improvisation(hm,gb,i)
    new_harmony = EFGHS_improvisation(hm,gb,i)
    new_path=vehicle_path(new_harmony)
    opt_path=local_search_p(new_path)
    new_harmony = p_to_sol(opt_path,new_harmony)       
    score = vrp_sol.fitness(new_harmony)
    NGHS_update_hm(hm,new_harmony,score)

            
        
        
toc = time.clock()
print (toc - tic)
print ('-----------------------------------' )      
for i in hm:
    print (i)    
print (vehicle_path(hm[0][0]))

for i in hm:
    print (vehicle_path(i[0]))


# if __name__ == "__main__":
#     import cProfile
#     cProfile.run("main()" )
 
# memory=[vehicle_path(i[0]) for i in hm]
# for i in memory:
#     print i