import copy
from operator import itemgetter
import time

import hs
from pso import inatial_from_hm, global_best, position_float, MAXP, \
    particle_update
from vrp_sol import fitness


swarm = inatial_from_hm(hs.hm)
global_best = hs.hm[0][0]
pg = position_float(global_best)
best_score = fitness(global_best)
    
start = time.clock()   
for i in range(MAXP):
    for particle in swarm:
        new_particle = particle_update(particle,pg)
        score = new_particle[3]
        if score < best_score:
            best_score = score
            global_best = copy.deepcopy(new_particle[0])
            pg = position_float(global_best)
#         print global_best
#         print best_score  
#         print '---------------------------------------'
end = time.clock()
swarm = sorted(swarm, key=itemgetter(3))
print global_best
print best_score  
print '---------------------------------------'  
for i in swarm:
    print i
print end - start  