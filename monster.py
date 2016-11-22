# Monster.py
# Thorin Schmidt
# 11/16/2016

''' Monster Package '''
from character import *
from random import randint, choice

class Monster(Character):
    ''' generic monster class '''
    def __init__(self,
                 name = "Generic Foe",
                 maxHealth = 10,
                 speed = 25,
                 stamina = 25,
                 strength = 8,
                 dexterity = 8,
                 constitution = 10,
                 intelligence = 8,
                 wisdom = 10,
                 charisma = 10,
                 numberOfPotions = 2,
                 inventory = [],
                 aggression = 50,
                 awareness = 50,
                 fear = 50):
        super(Monster, self).__init__(name, maxHealth, speed, stamina,
                                      strength, dexterity, constitution,
                                      intelligence, wisdom, charisma,
                                      numberOfPotions, inventory)
        self.aggression = aggression
        self.awareness = awareness
        self.fear = fear  #indicates cowardice level

    def combat_choice(self):
        ''' combat AI

            returns a, h, or f.  Based on aggression, awareness, morale
            
            '''
        attackValue = randint(1,100) + self.aggression
        healValue = randint(1,100) + self.awareness
        fleeValue = randint(1,100) + self.fear

        if attackValue >= healValue and attackValue >= fleeValue:
            return "a"
        elif healValue >= attackValue and healValue >= fleeValue:
            return "h"
        elif fleeValue >= attackValue and fleeValue >= healValue:
            return "f"
        else:
            return "AI_error"

class Orc(Monster):
    ''' generic Orc class

        this class '''
    def __init__(self, name = "Dorque da Orc"):
        orcName = name
        maxHealth = randint(1,8)
        speed = 25
        stamina = 25
        strength = randint(8,10)
        dexterity = randint(10,12)
        constitution = 10
        intelligence = 8
        wisdom = 10
        charisma = 10
        numberOfPotions = 2
        inventory = []
        aggression = 80
        awareness = 30
        fear = 20
        super(Orc, self).__init__(orcName, maxHealth, speed, stamina, strength,
                                  dexterity, constitution, intelligence,
                                  wisdom, charisma, numberOfPotions,
                                  inventory, aggression, awareness, fear)
class WrathMan(Monster):
    '''generic wrath class

       converts half of damage taken into strength
       takes other half of damage'''
    def __init__(self,name = 'Wrath'):
        maxHealth = randint(20,50)
        speed = randint(20,30)
        stamina = randint(20,30)
        strength = randint(8,15)
        dexterity = randint(6,10)
        constitution = randint(6,10)
        intelligence = randint(6,10)
        wisdom = randint(6,10)
        charisma = randint(4,14)
        numberOfPotions = randint(0,8)
        inventory = []
        aggression = randint(20,70)
        awareness = randint(0,30)
        fear = 0
        super(WrathMan,self).__init__(name,maxHealth,speed,stamina,
                                      strength,dexterity,constitution,
                                      intelligence,wisdom,charisma,
                                      numberOfPotions,inventory,
                                      aggression,awareness,fear)
    def get_damaged(self,damage):
        '''gets stronger and more aggressive with every hit
           takes half damage'''
        self.strength += damage//2
        self.health -= damage//2
        self.aggression += damage
   

def random_monster():
    '''generate a monster at random

    create an instance of each monster here, then add that instance to
    the listOfMonsters.  The function will pick a random instance out of
    the list, then return it to the caller.'''
    
    monster = Monster()
    orc = Orc()
    wrath = WrathMan()# DAS
    
    listOfMonsters = [monster, orc, wrath]
    return choice(listOfMonsters)


if __name__ == "__main__":

    Grr = Orc(name = "Freddy")
    #Randy = random_monster()
    #print(Randy.name)


    
