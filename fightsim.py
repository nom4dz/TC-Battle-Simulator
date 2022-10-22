import numpy as np
import math
import time
start = time.time()
#Bonuses to include: puncture, assassinate, focus, deadeye, weaken, cupid, achilles
#RW armor: Dune, Assault, EOD
N = 10000 #Number of simulations
idmg1 = 0 # %Damage increase 
idmg2 = 0 
ap1 = 0 # %Armor penetration of P1
ap2 = 0 
cr1 = 25 # %Critical hit
cr2 = 25
wdmg1 = 70 #Weapon damage
wdmg2 = 70
acc1 = 60 #Weapon accuracy
acc2 = 60
hp1 = 7500
hp2 = 7500
str1 = 10**9
def1 = 10**9
spd1 = 10**9
dex1 = 10**9
str2 = 10**9
def2 = 10**9
spd2 = 10**9
dex2 = 10**9
def dmg(STR): #dmg dealt to arms/legs
    return (7 * (math.log10(STR/10))**2 + 27 * math.log10(STR/10) + 30)/3.5

def defm(STR1, DEF2): #mitigation% from defence
    ratio = DEF2/STR1
    if ratio < 1/32:
        return 0
    elif 1/32 <= ratio and ratio < 1:
        return math.log(ratio)*50/math.log(32) + 50
    elif 1 <= ratio and ratio < 14:
        return math.log(ratio)*50/math.log(14) + 50
    else:
        return 100

def hit_chance(SPD1, DEX2): #base hit chance
    ratio = SPD1/DEX2
    if ratio < 1/64:
        return 0
    elif 1/64 <= ratio and ratio < 1:
        return 50/7*(8*math.sqrt(ratio) - 1)
    elif 1 <= ratio and ratio < 64:
        return 100 - 50/7*(8*math.sqrt(1/ratio) - 1)
    else:
        return 100

def fHC(bHC, acc): #final hit chance
    if bHC >= 50:
        return bHC + ((acc-50)/50)*(100 - bHC)
    else:
        return bHC + ((acc-50)/50)*bHC

dmg1 = (1 + idmg1/100)*dmg(str1)*wdmg1/10*(1 - defm(str1,def2)/100) #Damage dealt by P1 to P2 on arms/legs
dmg2 = (1 + idmg2/100)*dmg(str2)*wdmg2/10*(1 - defm(str2,def1)/100)
hit1 = fHC(hit_chance(spd1, dex2), acc1) #Hit chance of P1 after weapon acc modifier
hit2 = fHC(hit_chance(spd2, dex1), acc2)

#(Head, Throat, Heart, Chest, Stomach, Groin, Arm, Hand, Leg, Foot)
fba = [0, 0, 100, 95.73, 96.57, 11.88, 36.16, 0, 0.51, 0]
combat_pants = [0, 0, 0, 0, 7.62, 100, 0, 0, 100, 16.28]
combat_gloves = [0, 0, 0, 0, 0, 0, 0.32, 100, 0, 0]
combat_boots = [0, 0, 0, 0, 0, 0, 0, 0, 7.92, 100]
moto_helm = [85.35, 23.19, 0, 0, 0, 0, 0, 0, 0, 0]
welding_helm = [100, 49.53, 0, 0, 0, 0, 0, 0, 0, 0]
delta_mask = [27.13, 0, 0, 0, 0, 0, 0, 0, 0, 0]
delta_body = [0, 88.81, 100, 100, 100, 13.4, 100, 30.7, 0.64, 0]
delta_pants = [0, 0, 0, 0, 8.59, 100, 0, 0, 100, 29.06]
delta_gloves = [0, 0, 0, 0, 0, 0, 0.5, 100, 0, 0]
delta_boots = [0, 0, 0, 0, 0, 0, 0, 0, 10.25, 100]
riot_helm = [99.61, 0, 0, 0, 0, 0, 0, 0, 0, 0]
riot_body = [0, 79.06, 100, 100, 100, 99.9, 100, 21.6, 3.01, 0]
riot_pants = [0, 0, 0, 0, 2.12, 100, 0, 0, 100, 39.96]
riot_gloves = [0, 0, 0, 0, 0, 0, 0.78, 100, 0, 0]
riot_boots = [0, 0, 0, 0, 0, 0, 0, 0, 11.62, 100]

#armor coverage and mitigation of each body part
def armor(helmet: tuple, h: int , 
          body: tuple, by: int , 
          gloves: tuple, g: int , 
          pants: tuple, p: int , 
          boots: tuple, bs: int, AP2 ): 
    a = np.array([helmet, body, gloves, pants, boots]) #coverage of each body part
    a_value = [h, by, g, p, bs] #armor mitigation
    a_value = np.array(a_value)*(1 - AP2/100) #Armor mitigation after penetration
    a_value = a_value.tolist()
    x = []
    for i in range(10):        
        if np.nonzero(a[:,i])[0].size == 1: #when body part is covered by 1 piece of armor
            c1 = a[np.nonzero(a[:,i]),i][0][0]
            a1 = a_value[np.nonzero(a[:,i])[0][0]]
            if c1 == 100:
                x.append([[c1,], [a1,]])
            else:
                x.append([[c1, 100 - c1], [a1, 0]])
        elif np.nonzero(a[:,i])[0].size == 2: #when body part is covered by 2 pieces of armor
            c1 = a[np.nonzero(a[:,i]),i][0][0]
            c2 = a[np.nonzero(a[:,i]),i][0][1]
            a1 = a_value[np.nonzero(a[:,i])[0][0]]
            a2 = a_value[np.nonzero(a[:,i])[0][1]]
            c3 = [c1, c2]
            a3 = [a1, a2]
            maxarg = np.argmax(a3)
            minarg = 1 - maxarg
            if c3[maxarg] + c3[minarg] < 100:
                x.append([[c3[maxarg], c3[minarg], 100 - c3[maxarg] - c3[minarg]],[a3[maxarg], a3[minarg], 0]])
            elif c3[maxarg] < 100:
                x.append([[c3[maxarg], 100 - c3[maxarg]],[a3[maxarg], a3[minarg]]])
            else:
                x.append([[c3[maxarg],],[a3[maxarg],]])
        elif np.nonzero(a[:,i])[0].size == 3: #when body part is covered by 3 pieces of armor
            c1 = a[np.nonzero(a[:,i]),i][0][0]
            c2 = a[np.nonzero(a[:,i]),i][0][1]
            c3 = a[np.nonzero(a[:,i]),i][0][2]
            a1 = a_value[np.nonzero(a[:,i])[0][0]]
            a2 = a_value[np.nonzero(a[:,i])[0][1]]
            a3 = a_value[np.nonzero(a[:,i])[0][2]]
            if a_value[3] >= a_value[4] and a_value[3] >= a_value[1]:
                x.append([[c2,], [a2,]])
            elif a_value[3] < a_value[4] and a_value[3] >= a_value[1]:
                x.append([[c3,c2 - c3], [a3,a2]])
            elif a_value[3] >= a_value[4] and a_value[3] < a_value[1]:
                x.append([[c1,c2 - c1], [a1,a2]])
            else:
                x.append([[c3, c1, c2 - c1 - c3], [a3, a1, a2]])                
        else:
            x.append([[100, 0]])
    return x

#Armor coverage of P1
a1 = armor(moto_helm, 31, fba, 44,  combat_gloves, 40, combat_pants, 40, combat_boots, 40, ap2) 
#Armor coverage of P2
a2 = armor(moto_helm, 31, fba, 44,  combat_gloves, 40, combat_pants, 40, combat_boots, 40, ap1) 

def simulate(DMG1, HIT1, HP2, CR1, A2, N):    
    x = A2
    CR1 = CR1/100
    NCR = 1 - CR1
    hitc = HIT1/100
    missc = 1 - hitc
    #Chance of hitting each body part
    hit = hitc*np.array([0.8*CR1, 0.1*CR1, 0.1*CR1, 0.25*NCR, 0.2*NCR, 0.05*NCR, 0.1*NCR, 0.1*NCR, 0.2*NCR, 0.1*NCR])
    #Chance of missing each body part
    miss = missc*np.array([0.8*CR1, 0.1*CR1, 0.1*CR1, 0.25*NCR, 0.2*NCR, 0.05*NCR, 0.1*NCR, 0.1*NCR, 0.2*NCR, 0.1*NCR])
    multi = [3.5, 3.5, 3.5, 2, 2, 2, 1, 0.7, 1, 0.7]
    for i in range(10):
        x[i][0] = np.array(x[i][0])*hit[i]/100 #Multiply armor coverage by the chance of hitting the armor
        x[i][0] = np.append(x[i][0],miss[i]) #Multiply armor coverage by the chance of missing the armor
        x[i][1].append(100) #Assume P2 has 100 armor whenever P1 misses
    #Create list of hit chance values i.e. sample space of each turn P1 attacks
    y = x[0][0]
    for i in range(9):
        y = np.append(y, x[i+1][0])
    #Create list of armor values corresponding to each hit chance in y
    armor_value = []
    for i in range(10):
        armor_value.append(x[i][1])
    damage1 = []
    #Convert from armor value to damage after armor mitigation
    for i in range(10):
        z = np.array(armor_value[i])
        z = 1 - z/100 #convert armor value to damage after armor mitigation
        z = z*multi[i] #body part dmg multiplier
        damage1.append(z)
    
    #unroll  list of arrays into 1-D array    
    damage2 = []  
    for sublist in damage1:
        for item in sublist:
            damage2.append(item)
    damage2 = np.array(damage2)
    
    #account for precision error, pvalues of multinomial should sum to 1
    #y = np.append(y, 1 - sum(y))
    #damage2 = np.append(damage2, 0)
    if sum(y) > 1:
        y[-1] = y[-1] - (sum(y) - 1)    
    damage2 = DMG1*damage2 #Multiply by dmg P1 deals to arms/legs
    #Generate a multinomial for each turn
    z = np.transpose(np.nonzero(np.random.multinomial(1,y, (N,22))))
    damage3 = np.take(damage2, tuple(z[:,2]))
    d4 = damage3.reshape((N,22)) #Damage dealt on each turn
    c = np.cumsum(d4, axis = 1) #Cumulative sum of damage dealt 
    d = c >= HP2 
    d1 = np.argmax(d, axis = 1) #Find the turn where sum of damage dealt is greater than hp of P2
    return d1
#create length N array, each element is the turn that P2 dies, or 0 if P2 survives
x = simulate(dmg1, hit1, hp2, cr1, a2, N) 
#create length N array, each element is the turn that P1 dies, or 0 if P1 survives
y = simulate(dmg2, hit2, hp1, cr2, a1, N) 

##count draws
#Find all fights where P2 survives
x0 = x == 0
#Find all fights where P1 survives
y0 = y == 0
#Count number of fights where both survive
z = np.logical_and(x0, y0)
draws = sum(z)
drawp = 100*draws/N


x[np.where(x == 0)[0]] = 30
y[np.where(y == 0)[0]] = 31

#count wins
zw = x <= y #Fights where P2 dies on same turn or earlier than P1
wins = sum(zw) - draws
winp = 100*wins/N
#count losses
losses = N - wins - draws
lossp = 100*losses/N

print("Wins: " + str(wins) + " (" + str(winp) +  "%)\nDraws: "+str(draws) + " (" + str(drawp) + 
                     "%)\nLosses: " + str(losses) + " (" + str(lossp) + "%)" )

end = time.time()
total_time = end - start
print("Time taken:" , str(total_time) , "seconds")










