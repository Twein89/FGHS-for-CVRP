
import math

f=open(r'C:\Documents and Settings\Administrator\My Documents\test\instances\A-VRP\A-n33-k5.vrp')
        
lines=f.readlines()
customers=[]
DIMENSION = 33
vehicle_num=5

for i in range (0,DIMENSION):
    line = lines[7+i].split()
    customer = {'NUM' : int(line[0])-1,
                'XCOORD' : int(line[1]),
                'YCOORD' : int(line[2])
                }
    customers.append(customer)
    line = lines[DIMENSION+8+i].split()
    customers[i]['Demand'] = int(line[1])

rows=DIMENSION
cols=DIMENSION

def distance(x1,y1,x2,y2):
    return (int(round(math.sqrt((x1-x2)**2+(y1-y2)**2)))) 


matrix = [[distance(customers[row]['XCOORD'],customers[row]['YCOORD'],customers[col]['XCOORD'],customers[col]['YCOORD']) 
           for col in range(cols)] for row in range(rows)]

# DIMENSION = 9
# matrix = [[0,4,6,7.5,9,20,10,16,8],[4,0,6.5,4,10,5,7.5,11,10],[6,6.5,0,7.5,10,10,7.5,7.5,7.5],[7.5,4,7.5,0,10,5,9,9,15],[9,10,10,10,0,10,7.5,7.5,10],[20,5,10,5,10,0,7,9,7.5],[10,7.5,7.5,9,7.5,7,0,7,10],[16,11,7.5,6,7.5,9,7,0,10],[8,10,7.5,15,10,7.5,10,10,0]]
# customers = [{'NUM': 0,'Demand': 0},{'NUM': 1,'Demand': 1},{'NUM': 2,'Demand': 2},{'NUM': 3,'Demand': 1},{'NUM': 4,'Demand': 2},{'NUM': 5,'Demand': 1},{'NUM': 6,'Demand': 4},{'NUM': 7,'Demand': 2},{'NUM': 8,'Demand': 2}]
#    
 
# print matrix[8][0]
