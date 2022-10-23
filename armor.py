import numpy as np

#[Head, Throat, Heart, Chest, Stomach, Groin, Arm, Hand, Leg, Foot]

class Armor:
    def __init__(self, coverage, armor_value, bonus = 0, rw = 0):
        self.value = armor_value
        self.coverage = coverage
        self.bonus = bonus
        self.rw = rw
class fba(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 100, 95.73, 96.57, 11.88, 36.16, 0, 0.51, 0], armor_value, bonus = 0)
class combat_pants(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 7.62, 100, 0, 0, 100, 16.28], armor_value, bonus = 0)
class combat_gloves(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 0, 0, 0.32, 100, 0, 0], armor_value, bonus = 0)
class combat_boots(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 0, 0, 0, 0, 7.92, 100], armor_value, bonus = 0)
class moto_helmet(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [85.35, 23.19, 0, 0, 0, 0, 0, 0, 0, 0], armor_value, bonus = 0)
class welding_helmet(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [100, 49.53, 0, 0, 0, 0, 0, 0, 0, 0], armor_value, bonus = 0)
class delta_mask(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [27.13, 0, 0, 0, 0, 0, 0, 0, 0, 0], armor_value, bonus = 0)        
class delta_body(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 88.81, 100, 100, 100, 13.4, 100, 30.7, 0.64, 0], armor_value, bonus = 0) 
class delta_pants(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 8.59, 100, 0, 0, 100, 29.06], armor_value, bonus = 0) 
class delta_gloves(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 0, 0, 0.5, 100, 0, 0], armor_value, bonus = 0) 
class delta_boots(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self,[0, 0, 0, 0, 0, 0, 0, 0, 10.25, 100] , armor_value, bonus = 0)    
        
class riot_helmet(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [99.61, 0, 0, 0, 0, 0, 0, 0, 0, 0], armor_value, bonus = 0)
class riot_body(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 79.06, 100, 100, 100, 99.9, 100, 21.6, 3.01, 0], armor_value, bonus = 0)
class riot_pants(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 2.12, 100, 0, 0, 100, 39.96], armor_value, bonus = 0)
class riot_gloves(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 0, 0, 0.78, 100, 0, 0], armor_value, bonus = 0)
class riot_boots(Armor):
    def __init__(self, armor_value, bonus = 0):
        Armor.__init__(self, [0, 0, 0, 0, 0, 0, 0, 0, 11.62, 100], armor_value, bonus = 0)    
        
class assault_helmet(Armor):
    def __init__(self, armor_value, bonus):
        Armor.__init__(self, [66.53, 3.99, 0, 0, 0, 0, 0, 0, 0, 0], armor_value, bonus, rw = 1)
class assault_body(Armor):
    def __init__(self, armor_value, bonus):
        Armor.__init__(self, [0, 81.16, 100, 100, 100, 14.15, 100, 20.73, 0.56, 0], armor_value, bonus, rw = 1)
class assault_pants(Armor):
    def __init__(self, armor_value, bonus):
        Armor.__init__(self, [0, 0, 0, 0, 3.84, 100, 0, 0, 100, 33.25], armor_value, bonus, rw = 1)
class assault_gloves(Armor):
    def __init__(self, armor_value, bonus):
        Armor.__init__(self, [0, 0, 0, 0, 0, 0, 0.5, 100, 0, 0], armor_value, bonus, rw = 1)
class assault_boots(Armor):
    def __init__(self, armor_value, bonus):
        Armor.__init__(self, [0, 0, 0, 0, 0, 0, 0, 0, 9.07, 100], armor_value, bonus, rw = 1)


#armor coverage and mitigation of each body part
def Coverage(helmet, body, gloves, pants, boots, AP2): 
    a = np.array([helmet.coverage, body.coverage, gloves.coverage, pants.coverage, boots.coverage]) #coverage of each body part
    a_value = [helmet.value, body.value, gloves.value, pants.value, boots.value] #armor mitigation
    a_value = np.array(a_value)*(1 - AP2/100) #Armor mitigation after penetration
    X = [helmet, body, gloves, pants, boots]
    for i in range(5):
        if X[i].rw == 1:
            a_value[i] = 100 - (100 - a_value[i])*(100 - X[i].bonus)/100 #Account for assault bonus
    a_value = a_value.tolist()
    #print(str(a_value))
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

        
#test = assault_body(46, 20)
#print(str(test.rw))