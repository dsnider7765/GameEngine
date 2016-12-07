# character_creator.py
# Thorin Schmidt
# 11/29/2016

''' GUI-based character generator'''

import tkinter as tk
import character as ch
import monster as mon
from random import randint

BUTTON_COLOR = '#9494B8'
TITLE_FONT = ("Helvetica", 18, "bold")
CHAR_HELP_STR_TITLE = 'generate a character based on user input'
CHAR_HELP_STR_SIMPLE='The user is asked which stat(str, dex, con, int, wis, cha) is most important, and which is least.  most important gets a value of 17, least gets a 9, and the rest get 12. This method is suitable for a 20-point character build using Pathfinder d20 rules.  This method has only a few choices, and results in moderate satisfaction for the user.'
CHAR_HELP_STR_HARDCORE = 'hardcore - results are generated randomly using the 3d6 method, in standard stat block sequence: (str, dex, con, int, wis, cha). if none of the stats are over 12, then the entire set is re-rolled until it does. The user has no control over ability scores. This method is the easiest, but usually has the least satisfaction for the user.'
CHAR_HELP_STR_FOURD6 = '4d6, keep best three, arrange to suit - 6 sets of 4d6 are rolled, in each set, the top three dice are kept and added together. Then these scores are assigned by the user. This method usually has the highest satisfaction for the player, but is also the most complicated, due to the many choices required.'

class RootApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        ''' Custom Window class for Game

        Data Model - Character object
        referenced in frames by using:
            self.controller.player'''

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        self.cheat = 0
        self.cheatsDescription = {0:'No Cheats Activated',
                                  1:'All 1\'s are rerolled',
                                  2:'All 1\'s are converted to 6\'s',
                                  3:'Reroll all 1\'s and 2\'s',
                                  4:'All 1\'s are converted to 6\'s and ' + \
                                   'all 2\'s are converted to 5\'s'}
        
        container = tk.Frame(self)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.grid(sticky=tk.N + tk.E + tk.W + tk.S)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.player = ch.Character()

        self.frames = {}
        for F in (Menu, Hardcore, Simple, FourD6, Help, Travel):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Menu")
        
    def cheat_handler(self):
        '''handle cheat binding'''
        self.cheat = (self.cheat + 1) % 5
        if self.cheat:
            print('Cheat {0} enabled! {1}'.format(self.cheat,
                                                  self.cheatsDescription[self.cheat]))
        else:
            print(self.cheatsDescription[self.cheat])

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Menu(tk.Frame):
    """ Opening Menu for Character Creator """
    def __init__(self, parent, controller):
        """ Initialize the frame. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Create button, text, and entry widgets. """
        # create instruction label
        self.instLbl = tk.Label(self, text =
                              "Choose a Character Creation Method:")
        self.instLbl.grid()

        # create whitespace
        self.blankLbl = tk.Label(self, text ="")
        self.blankLbl.grid()

        # create hardcore button
        self.hcBttn = tk.Button(self, text = "Hardcore",
                                command = lambda: self.controller.show_frame("Hardcore"))
        self.hcBttn.grid()

        # create simple button
        self.simpleBttn = tk.Button(self, text = "Simple",
                             command = lambda: self.controller.show_frame("Simple"))
        self.simpleBttn.grid()

        # create 4d6 button
        self.fourD6Bttn = tk.Button(self, text = "4d6",
                             command = lambda: self.controller.show_frame("FourD6"))
        self.fourD6Bttn.grid()

        # create Help button
        self.helpBttn = tk.Button(self, text = "Help",
                             command = lambda: self.controller.show_frame("Help"))
        self.helpBttn.grid()

class Hardcore(tk.Frame):
    '''frame for hardcore character creation'''
    def __init__(self, parent, controller):
        '''hardcore initializer'''
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(3):
            self.columnconfigure(i, weight=1)

        self.statblock = self.roll_stats()

        self.create_widgets()
        self.populate_statblock()

    def create_widgets(self):
        '''method for widget placement'''
        #row 0 - Heading
        self.label = tk.Label(self, text="Hardcore", font=TITLE_FONT)
        self.label.grid(row=0, column=0, columnspan=3)

        #row 1 - table headings
        attLbl = tk.Label(self, text="Attribute")
        abrLbl = tk.Label(self, text="Abbreviation")
        scoreLbl = tk.Label(self, text="Score")
        attLbl.grid(row=1, column=0)
        abrLbl.grid(row=1, column=1)
        scoreLbl.grid(row=1, column=2)

        #row 2 - Strength
        self.strengthLbl = tk.Label(self, text="Strength", background="#FF1111",
                                    width=20)
        self.strLbl = tk.Label(self, text="(STR)", background="#FF1111",
                               width=20)
        self.strStatLbl = tk.Label(self, text="", background="#FF1111",
                                   width=20)
        self.strengthLbl.grid(row = 2, column=0)
        self.strLbl.grid(row = 2, column=1)
        self.strStatLbl.grid(row = 2, column=2)

        #row 3 - Dexterity
        self.dexterityLbl = tk.Label(self, text="Dexterity", background="#FF6633",
                                    width=20)
        self.dexLbl = tk.Label(self, text="(DEX)", background="#FF6633",
                               width=20)
        self.dexStatLbl = tk.Label(self, text="", background="#FF6633",
                                   width=20)
        self.dexterityLbl.grid(row = 3, column=0)
        self.dexLbl.grid(row = 3, column=1)
        self.dexStatLbl.grid(row = 3, column=2)

        #row 4 - Constitution
        self.constitutionLbl = tk.Label(self, text="Constitution",
                                        background="yellow",
                                        width=20)
        self.conLbl = tk.Label(self, text="(CON)", background="yellow",
                               width=20)
        self.conStatLbl = tk.Label(self, text="", background="yellow",
                                   width=20)
        self.constitutionLbl.grid(row = 4, column=0)
        self.conLbl.grid(row = 4, column=1)
        self.conStatLbl.grid(row = 4, column=2)

        #row 5 - Intelligence
        self.intelligenceLbl = tk.Label(self, text="Intelligence",
                                        background="#32CD32",
                                        width=20)
        self.intLbl = tk.Label(self, text="(INT)", background="#32CD32",
                               width=20)
        self.intStatLbl = tk.Label(self, text="", background="#32CD32",
                                   width=20)
        self.intelligenceLbl.grid(row = 5, column=0)
        self.intLbl.grid(row = 5, column=1)
        self.intStatLbl.grid(row = 5, column=2)

        #row 6 - Wisdom
        self.wisdomLbl = tk.Label(self, text="Wisdom", background="skyblue",
                                  width=20)
        self.wisLbl = tk.Label(self, text="(WIS)", background="skyblue",
                               width=20)
        self.wisStatLbl = tk.Label(self, text="", background="skyblue",
                                   width=20)
        self.wisdomLbl.grid(row = 6, column=0)
        self.wisLbl.grid(row = 6, column=1)
        self.wisStatLbl.grid(row = 6, column=2)

        #row 7 - Charisma
        self.charismaLbl = tk.Label(self, text="Charisma", background="violet",
                                    width=20)
        self.chaLbl = tk.Label(self, text="(CHA)", background="violet",
                               width=20)
        self.chaStatLbl = tk.Label(self, text="", background="violet",
                                   width=20)
        self.charismaLbl.grid(row = 7, column=0)
        self.chaLbl.grid(row = 7, column=1)
        self.chaStatLbl.grid(row = 7, column=2)
        
        #row 8 - Instructions
        self.instructionLbl = tk.Label(self, text='Click ReRoll to try '+\
                                       'again, or click Save to accept ' +\
                                       'these scores.')
        self.instructionLbl.grid(row=9, column=0, columnspan=3)

        #row 10 - Navigation Buttons
        self.rrBttn = tk.Button(self, text = "Reroll", width=20,
                                command = self.reroll)
        self.rrBttn.grid(row = 10, column = 0)

        self.backbutton = tk.Button(self, text="Back to Menu", width=20,
                           command=lambda: self.controller.show_frame("Menu"))
        self.backbutton.grid(row=10, column=1)

        self.saveBttn = tk.Button(self, text="Save and\nContinue", width=20,
                                  command=self.save_character,)
        self.saveBttn.grid(row=10, column=2)

    def reroll(self):
        '''reroll stats'''
        self.statblock = self.roll_stats()
        self.populate_statblock()
        
    def roll_stats(self):
        '''roll for stats'''
        return [randint(3,18),
                randint(3,18),
                randint(3,18),
                randint(3,18),
                randint(3,18),
                randint(3,18)]
        

    def populate_statblock(self):
        '''place values in stat labels'''
        self.labelList = (self.strStatLbl,
                          self.dexStatLbl,
                          self.conStatLbl,
                          self.intStatLbl,
                          self.wisStatLbl,
                          self.chaStatLbl)

        for i in range(6):
            self.labelList[i].configure(text = str(self.statblock[i]))

    def save_character(self):
        '''Finalizes the user's character with the attributes from the frame.'''
        self.controller.player.strength = int(self.strStatLbl["text"])
        self.controller.player.dexterity = int(self.dexStatLbl["text"])
        self.controller.player.constitution = int(self.conStatLbl["text"])
        self.controller.player.intelligence = int(self.intStatLbl["text"])
        self.controller.player.wisdom = int(self.wisStatLbl["text"])
        self.controller.player.charisma = int(self.chaStatLbl["text"])
        print(self.controller.player)
        self.controller.show_frame("Travel")
        
class Simple(tk.Frame):
    '''framefor simple character creation'''

    def __init__(self, parent, controller):
        '''initializer'''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #phase for choosing the first stat and second stat
        self.phase = 0

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.create_widgets()
        self.reset()

    def char_submit(self):
        '''Finalizes the user's character with the attributes from the frame.'''
        self.controller.player.strength = int(self.statLabels[0]['text'])
        self.controller.player.dexterity = int(self.statLabels[1]['text'])
        self.controller.player.constitution = int(self.statLabels[2]['text'])
        self.controller.player.intelligence = int(self.statLabels[3]['text'])
        self.controller.player.wisdom = int(self.statLabels[4]['text'])
        self.controller.player.charisma = int(self.statLabels[5]['text'])
        print(self.controller.player)
        self.controller.show_frame('Travel')
            
    def create_widgets(self):
        '''method for widget placement'''
        
        self.titleLabel = tk.Label(self, text = "Simple", font = TITLE_FONT)
        self.titleLabel.grid(row = 0, column = 0, columnspan = 3)

        self.statNames = 'Strength,(STR),#FF1111 Dexterity,(DEX),#FF6633 Constitution,(CON),Yellow \
Intelligence,(INT),#32CD32 Wisdom,(WIS),skyblue Charisma,(CHA),Violet'.split(' ')
        for i in range(len(self.statNames)):
            self.statNames[i] = self.statNames[i].split(',')

        for i in range(len(self.statNames)):
            statNameLabel = tk.Label(self, width=10, text=self.statNames[i][0])
            statNameLabel.config(background=self.statNames[i][2], foreground='Black')
            statNameLabel.grid(column=0, row=i+1, sticky=tk.E+tk.W)

            shortNameLabel = tk.Label(self, width=5, text=self.statNames[i][1])
            shortNameLabel.config(background=self.statNames[i][2], foreground='Black')
            shortNameLabel.grid(column=1, row=i+1, sticky=tk.E+tk.W)

        self.scoreLabel = tk.Label(self, text='Available Scores')
        self.scoreLabel.grid(row=7, column=1)
        
        self.hintLabel = tk.Label(self, text='Click a button to pick Strength')
        self.hintLabel.grid(row=8, column=0, columnspan=3)

        self.bttns = []
        self.commands = [lambda: self.bttnClick(0), lambda: self.bttnClick(1),
                         lambda: self.bttnClick(2), lambda: self.bttnClick(3),
                         lambda: self.bttnClick(4), lambda: self.bttnClick(5)]
        for i in range(6):
            statName = self.statNames[i][0][:3].upper()
            ftn = self.commands[i]
            statBtn = tk.Button(self, text=statName,
                                command=ftn)
            self.bttns.append(statBtn)
            self.bttns[-1].grid(row=9 + (i//3), column=i%3)
            
        self.statLabels = []
        for i in range(6):
            statName = self.statNames[i][0][:3].upper()
            self.statLabels.append(tk.Label(self, text='',background=self.statNames[i][2]))
            self.statLabels[-1].grid(row=i + 1, column=2, sticky=tk.E+tk.W)
                            
        self.rrButton = tk.Button(self, text = "Reset",
                               command = self.reset)
        self.rrButton.grid(row=12, column=0)
     
        self.menuButton = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        self.menuButton.grid(row=12, column=1)

        self.contButton = tk.Button(self, text='Save and\nContinue',
                                     command=self.char_submit,
                                     state=tk.DISABLED)
        self.contButton.grid(row=12, column=2, sticky=tk.E + tk.W)

    def reset_labels(self):
        '''reset the labels'''
        for label in self.statLabels:
            label['text'] = '12'
    
    def reset(self):
        '''handler for the reset button'''
        for bttn in self.bttns:
            bttn.configure(state = tk.NORMAL)

        self.reset_labels()
        
        self.phase = 0
        self.hintLabel['text'] = 'Choose what attribute to raise to 17'
        self.contButton.configure(state=tk.DISABLED)
    
    def bttnClick(self, value):
        '''for clicking one of the stat buttons'''
        if self.phase == 0:
            self.statLabels[value]['text'] = '17'
            self.phase += 1
            statName = self.statNames[value][0][:3].upper()
            self.bttns[value].configure(state = tk.DISABLED)

            self.hintLabel['text'] = 'Choose what attribute to lower to 9'
            
        elif self.phase == 1:
            self.statLabels[value]['text'] = '9'
            self.phase += 1
            statName = self.statNames[value][0][:3].upper()
            for bttn in self.bttns:
                bttn.configure(state = tk.DISABLED)

            self.hintLabel['text'] = 'Finished!'
            self.contButton.configure(state=tk.NORMAL)
        

class FourD6(tk.Frame):
    '''4d6 frame'''
    def __init__(self, parent, controller):
        '''class constructor'''
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.statblock = []
        for i in range(6):
            self.statblock.append(self.roll_4d6())

        self.create_widgets()

    def roll_4d6(self):
        '''Generate rolls based off the 4d6 rules'''
        rolls = []
        for i in range(4):
            roll = randint(1, 6)
            if self.controller.cheat:
                if self.controller.cheat == 1:
                    roll = randint(1, 6)
                elif self.controller.cheat == 2:
                    if roll == 1:
                        roll = 6
                elif self.controller.cheat == 3:
                    if roll == 1 or roll == 2:
                        roll = randint(1, 6)
                elif self.controller.cheat == 4:
                    if roll == 1 or roll == 2:
                        roll = 7 - roll
            rolls.append(roll)
        rolls.remove(min(rolls))
        return sum(rolls)
    
    def char_submit(self):
        '''Finalizes the user's character with the attributes from the frame.'''
        self.controller.player.strength = int(self.statLabels[0]['text'])
        self.controller.player.dexterity = int(self.statLabels[1]['text'])
        self.controller.player.constitution = int(self.statLabels[2]['text'])
        self.controller.player.intelligence = int(self.statLabels[3]['text'])
        self.controller.player.wisdom = int(self.statLabels[4]['text'])
        self.controller.player.charisma = int(self.statLabels[5]['text'])
        print(self.controller.player)
        self.controller.show_frame('Travel')
            
    def create_widgets(self):
        '''method for widget placement'''
        
        self.titleLabel = tk.Label(self, text = "4D6", font = TITLE_FONT)
        self.titleLabel.grid(row = 0, column = 0, columnspan = 3)

        # Generates the first two columns of labels based on the string below
        # It is turned into a list that is structed as such
        # [Full Name, Abbrivation, Background Color]
        self.statNames = 'Strength,(STR),#FF1111 Dexterity,(DEX),#FF6633 Constitution,(CON),Yellow \
Intelligence,(INT),#32CD32 Wisdom,(WIS),skyblue Charisma,(CHA),Violet'.split(' ')
        for i in range(len(self.statNames)):
            self.statNames[i] = self.statNames[i].split(',')

        for i in range(len(self.statNames)):
            statNameLabel = tk.Label(self, width=10, text=self.statNames[i][0])
            statNameLabel.config(background=self.statNames[i][2], foreground='Black')
            statNameLabel.grid(column=0, row=i+1, sticky=tk.E+tk.W)

            shortNameLabel = tk.Label(self, width=5, text=self.statNames[i][1])
            shortNameLabel.config(background=self.statNames[i][2], foreground='Black')
            shortNameLabel.grid(column=1, row=i+1, sticky=tk.E+tk.W)

        # Generates the labels that tell the user what to do
        self.scoreLabel = tk.Label(self, text='Available Scores')
        self.scoreLabel.grid(row=7, column=1)
        
        self.hintLabel = tk.Label(self, text='Click a button to pick Strength')
        self.hintLabel.grid(row=8, column=0, columnspan=3)


        # Every button is made in order contain a value in self.statblock
        self.bttn1 = tk.Button(self, text = str(self.statblock[0]),
                               command = lambda:
                               self.bttnClick(1, str(self.statblock[0])),
                               width=10)
        self.bttn1.grid(row=9, column=0)

        self.bttn2 = tk.Button(self, text = str(self.statblock[1]),
                               command=lambda:
                               self.bttnClick(2, str(self.statblock[1])),
                               width=10)
        self.bttn2.grid(row=9, column=1)

        self.bttn3 = tk.Button(self, text = str(self.statblock[2]),
                               command=lambda:
                               self.bttnClick(3, str(self.statblock[2])),
                               width=10)
        self.bttn3.grid(row=9, column=2)

        self.bttn4 = tk.Button(self, text = str(self.statblock[3]),
                               command=lambda:
                               self.bttnClick(4, str(self.statblock[3])),
                               width=10)
        self.bttn4.grid(row=10, column=0)

        self.bttn5 = tk.Button(self, text = str(self.statblock[4]),
                               command=lambda:
                               self.bttnClick(5, str(self.statblock[4])),
                               width=10)
        self.bttn5.grid(row=10, column=1)
                               
        self.bttn6 = tk.Button(self, text = str(self.statblock[5]),
                               command=lambda:
                               self.bttnClick(6, str(self.statblock[5])),
                               width=10)
        self.bttn6.grid(row=10, column=2)

        # Generates the labels that accept the values from the buttons above
        self.activeStatLabelIndex = 0
        self.statLabels = []
        for i in range(6):
            self.statLabels.append(tk.Label(self, text='',background=self.statNames[i][2]))
            self.statLabels[i].grid(row=i + 1, column=2, sticky=tk.E+tk.W)

        # Generates the labels that handle the flow of the program
        self.resetButton = tk.Button(self, text='Reset',
                                      command=lambda: self.reroll(reset=False))
        self.resetButton.grid(row=11, column=1)
                            
        self.rrButton = tk.Button(self, text = "Reroll",
                               command = self.reroll)
        self.rrButton.grid(row=12, column=0)
     
        self.menuButton = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        self.menuButton.grid(row=12, column=1)

        self.contButton = tk.Button(self, text='Save and\nContinue', command=self.char_submit)
        self.contButton.grid(row=12, column=2, sticky=tk.E + tk.W)


    def reroll(self, reset=True):
        ''' re-roll the stat block

            the reset argument is set as True;
            if reset is true, the values inside of statblock are changed
            otherwise, they are left untouched.'''
        if reset:
            print("rerolling!")
        else:
            print('resetting!')
            
        self.activeStatLabelIndex = 0
        
        buttonList = (self.bttn1, self.bttn2, self.bttn3,
                      self.bttn4, self.bttn5, self.bttn6)
        for i in range(len(self.statLabels)):
            self.statLabels[i]['text'] = ''
            
        for i in range(len(self.statblock)):
            if reset:
                self.statblock[i] = self.roll_4d6()
            buttonList[i].configure(text = str(self.statblock[i]),
                                    state = tk.NORMAL)

        self.hintLabel['text'] = 'Click a button to pick {}'.format(
            self.statNames[self.activeStatLabelIndex][0])
            
            
    def bttnClick(self, value, newText):
        '''handles the button clickes on the frame

           Puts the clicked button's value into the proper label and
           continues the program until all labels are filled.'''

        self.statLabels[self.activeStatLabelIndex]['text'] = newText
        self.activeStatLabelIndex += 1
        
        try:
            self.hintLabel['text'] = 'Click a button to pick {}'.format(
                self.statNames[self.activeStatLabelIndex][0])
        except IndexError:
            self.hintLabel['text'] = 'Done!'

        getattr(self, 'bttn' + str(value))['state'] = tk.DISABLED
        

class Help(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)

        # Creates and displays a title for the frame
        titleLabel = tk.Label(self, text=CHAR_HELP_STR_TITLE.title(), font=TITLE_FONT)
        titleLabel.config(font='-size 14')
        titleLabel.grid()

        # Displays info about the Simple character creation
        simpleLabel = tk.Label(self, text='Simple')
        simpleLabel.grid(pady=3)
        simpleText = tk.Text(self, width=71,font='-size 8',height=6,wrap=tk.WORD)
        simpleText.grid(pady=5)
        simpleText.insert(0.0,CHAR_HELP_STR_SIMPLE)
        simpleText.config(state=tk.DISABLED)

        # Displays info about the Hardcore character creation
        hardcoreLabel = tk.Label(self, text='Hardcore')
        hardcoreLabel.grid(pady=3)
        hardcoreText = tk.Text(self, width=71,font='-size 8',height=6,wrap=tk.WORD)
        hardcoreText.grid(pady=5)
        hardcoreText.insert(0.0,CHAR_HELP_STR_HARDCORE)
        hardcoreText.config(state=tk.DISABLED)

        # Displays info about the FourD6 character creation
        fourD6Label = tk.Label(self, text='4d6')
        fourD6Label.grid(pady=3)
        fourD6Text = tk.Text(self, width=71,font='-size 8',height=6,wrap=tk.WORD)
        fourD6Text.grid(pady=5)
        fourD6Text.insert(0.0,CHAR_HELP_STR_FOURD6)
        fourD6Text.config(state=tk.DISABLED)

        button = tk.Button(self, text="Back to Menu",
                           command=lambda: controller.show_frame("Menu"))
        button.grid()

class Travel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(2):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)
        self.create_widgets()
    class Text2(tk.Frame): # created by Miguel Martinez Lopez http://code.activestate.com/recipes/578887-text-widget-width-and-height-in-pixels-tkinter/
        def __init__(self, master, width=0, height=0, **kwargs):
            self.width = width
            self.height = height

            tk.Frame.__init__(self, master, width=self.width, height=self.height)
            self.scrollbar = tk.Scrollbar(self)
            self.scrollbar.grid(row=0,column=2,sticky='nsw')
            self.text_widget = tk.Text(self, **kwargs)
            self.text_widget.configure(yscrollcommand=self.scrollbar.set)
            self.text_widget.grid(row=0,column=0,sticky='nsew')
            self.scrollbar.config(command=self.text_widget.yview)

        def pack(self, *args, **kwargs):
            tk.Frame.pack(self, *args, **kwargs)
            self.pack_propagate(False)

        def grid(self, *args, **kwargs):
            tk.Frame.grid(self, *args, **kwargs)
            self.grid_propagate(True)
    def create_widgets(self):
        #makes view window
        self.viewImage = tk.PhotoImage(file='Development Land.gif')#place holder image
        self.viewLabel = tk.Label(self,image=self.viewImage)
        self.viewLabel.grid(row=0,column=0)
        self.viewLabel.grid(row=0,column=0)
        #makes log
        self.logText = self.Text2(self,width=500,height=500,font='-size 12')
        self.logText.grid(row=0,column=1)
        self.logText.text_widget.insert(0.0,'''hnjfkads hfjaksdf hdkjasf hkjasd fhdkjasl hf asdf dasf
asdfd
asf
asdf
asdf
asdfdas fasd
f adsf asdf asdfndkjasf hasdkjl fasd f
asdf asdfbhjaskdf asdh fkgadkljsf adsf
das
fasd
 fasdf hdjasif hdkjas fhdkjasl fdas f
 asd
 f asd
 f asd fasdlf hasdjkf hjaskf hjaskdf hjdkasl fdas
 f asd fasdfkdas hfjkasdfa
 sd fas dfasdfjasdf
 asdf asdf asd
 ef asd fdasufas dfdas fasd
 ''')

         

# main
root = RootApp()
root.bind('<c>',lambda e: root.cheat_handler())
root.title("Character Creator")
root.geometry("1055x1185+200+0")

root.mainloop()
