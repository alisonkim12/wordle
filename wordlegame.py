
""" 
Wordle game 

Sept 2023 

Alison and Danielle 

""" 

import pandas as pd 
import csv
import random 
import pygame, sys
from pygame.locals import*

#Setting up the display
clock = pygame.time.Clock()
screen_width=1000
screen_height=1000
background_color = (255, 255, 255) #white
box_color = (211, 211, 211) #light gray
yellow = (255, 191, 0)
green = (60, 179, 113)
dark_gray = (105,105,105)
border_width = 3
border_color = (0,0,0)
user_input_color = (135, 206, 235) #light blue
button_color = (34,139,34) #green 


# Functional component

# Part 1: Random five letter word (import online database)
def pick_word():
    # open pandas dataframe with the words
    df = pd.read_csv('https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt')

    # choose number at random in the range of # of rows in dataframe 
    chosen_idx = random.choice(df.index)

    chosen_word = str(df.iloc[chosen_idx][0])
    print("The answer to this wordle is: ", chosen_word)

    # putting the word into a list of individual char
    return list(chosen_word)


# called within the init of game class
def display_setup():
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 40)
    display_screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("WORDLE")

    display_screen.fill(background_color)

    return display_screen, font   


# class the contains the highest level of the game / includes most of everything else 
# picking the answer, setting up the display, and creating all game objs start here 
class Game:
    def __init__(self):
        self.answer_list = pick_word()

        self.display_screen, self.font = display_setup()
        self.enter = Button(self.display_screen, self.font)
        self.user_text = ""
        self.user_answer = ""
        self.enter_button_active = False 
        self.letter1_input_active = False
        self.letter2_input_active = False
        self.letter3_input_active = False
        self.letter4_input_active = False
        self.letter5_input_active = False
        self.play_counter = 0

        #self.answer_space_1 = pygame.Rect(50, 550, 100, 100)
       # print(type(self.answer_space_1))
       # self.answer_space_2 = pygame.Rect(150, 550, 100, 100)
       # self.answer_space_3 = pygame.Rect(250, 550, 100, 100)
       # self.answer_space_4 = pygame.Rect(350, 550, 100, 100)
        #self.answer_space_5 = pygame.Rect(450, 550, 100, 100)

        self.box_grid = []
        for i in range(6): # n of rows
            box_list = []
            for j in range(5): # n of columns
                box = Box(self.display_screen, i, j)
                if i == 5: 
                    box.draw_box(user_input_color) 
                    box_list.append(box)
                else: 
                    box.draw_box() 
                    box_list.append(box)
            self.box_grid.append(box_list)

        """ 
        # set where the words will be typed
        self.curr_row = 0 # based on how many words have been guessed
        self.curr_col = 0 # based on how many ch have been typed/deleted
        self.curr_box = self.box_grid[self.curr_row][self.curr_col]

        """

    def start():
        return
    
    """
    def update_curr_box(self, p, q): # args are by what you want to incr/decr the indexes by
        self.curr_row = self.curr_row + p
        self.curr_col = self.curr_col + q
        self.curr_box = self.box_grid[self.curr_row][self.curr_col]

    """

    def calculate_input(self, user_word): 
        color_change_Dict = {"green": [], "yellow": []}
        og_list = []
        char_list = list(user_word) #putting the word into a list of individual char
        for i in range(len(char_list)): 
            for j in range(len(self.answer_list)): 
                if char_list[i] == self.answer_list[j]:
                    if i == j: 
                        print("Char: ", char_list[i])
                        color_change_Dict["green"].append(char_list[i])
                        print("APPEND green: ", color_change_Dict["green"])
                        break
                    else: 
                        #duplicate checkon the answer (eg.g never) 
                        og_list = color_change_Dict["yellow"]
                        color_change_Dict["yellow"].append(char_list[i])
                        print("APPEND yellow: ", color_change_Dict["yellow"])

        return color_change_Dict


    # only does something if first box has been clicked
    def key_pressed(self, event):
        if self.letter1_input_active or self.letter2_input_active or self.letter3_input_active or self.letter4_input_active or self.letter5_input_active: 
                if event.key == pygame.K_BACKSPACE:

                    """
                    # delete letter and set curr box to previous one
                    #self.curr_box.draw_box()
                    #if self.curr_col != 0:
                    #    self.update_curr_box(0, -1)  
                    # todo: fix this so it works in more situations

                    """
                    # get text input from 0 to -1 i.e. end.
                    self.user_text = self.user_text[:-1]
                    self.user_answer = self.user_answer[:-1]
                    # todo need box

                    if self.letter1_input_active == True: 
                        self.box_grid[5][0].draw_box()

                    if self.letter1_input_active == True: 
                        self.box_grid[5][1].draw_box()


                    if self.letter1_input_active == True: 
                        self.box_grid[5][2].draw_box()


                    if self.letter1_input_active == True:
                        self.box_grid[5][3].draw_box()
 

                    if self.letter1_input_active == True: 
                        self.box_grid[5][4].draw_box()


                    #self.add_text("", self.font) #delete the char from the screen
                    pygame.display.update()

                    if pygame.Rect(50, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                        self.letter1_input_active = False
                    if pygame.Rect(150, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                        self.letter2_input_active = False
                    if pygame.Rect(250, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                        self.letter3_input_active = False
                    if pygame.Rect(350, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                        self.letter4_input_active = False
                    if pygame.Rect(450, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                        self.letter5_input_active = False
                else:
                    ch = chr(event.key)
                    self.user_text = event.unicode
                    
                    if self.letter1_input_active == True: 
                        if pygame.Rect(50, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                            self.letter1_input_active = True
                            self.box_grid[5][0].add_text(self.user_text, self.font)
                            self.user_answer = self.user_answer + self.user_text
                            print("User text: ", self.user_text)
                            print("User answer: ", self.user_answer)


                        elif self.letter2_input_active == True: 
                            if pygame.Rect(150, 550, 100, 100).collidepoint(pygame.mouse.get_pos()):
                                self.letter2_input_active = True
                                self.box_grid[5][1].add_text(self.user_text, self.font)
                                self.user_answer = self.user_answer + self.user_text
                                print("User text: ", self.user_text)
                                print("User answer: ", self.user_answer)

                            elif self.letter3_input_active == True: 
                                if pygame.Rect(250, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                                    self.letter3_input_active = True
                                    self.box_grid[5][2].add_text(self.user_text, self.font)
                                    self.user_answer = self.user_answer + self.user_text
                                    print("User text: ", self.user_text)
                                    print("User answer: ", self.user_answer)
                                
                                elif self.letter4_input_active == True: 
                                    if pygame.Rect(350, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                                        self.letter4_input_active = True
                                        self.box_grid[5][3].add_text(self.user_text, self.font)
                                        self.user_answer = self.user_answer + self.user_text
                                        print("User text: ", self.user_text)
                                        print("User answer: ", self.user_answer)

                                    elif self.letter5_input_active == True: 
                                        if pygame.Rect(450, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): 
                                            self.letter5_input_active = True
                                            self.box_grid[5][4].add_text(self.user_text, self.font)
                                            self.user_answer = self.user_answer + self.user_text
                                            print("User text: ", self.user_text)
                                            print("User answer: ", self.user_answer)
                    

    def mouse_down_enter(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.enter.location.collidepoint(event.pos): 
                #error: "letter1_input_active" referenced before assignment 
                if self.letter1_input_active and self.letter2_input_active and self.letter3_input_active and self.letter4_input_active and self.letter5_input_active: 
                    
                    print("User answer is: ", self.user_answer)
                    user_answer_char_list = list(self.user_answer)
                    answer_duplicate_letters = []
                    for every_char in user_answer_char_list: 
                        if user_answer_char_list.count(every_char) > 1: 
                            if answer_duplicate_letters.count(every_char) == 0: 
                                answer_duplicate_letters.append(every_char)
                    
                    answer_Dict = self.calculate_input(self.user_answer)                    
                    
                    print("Play counter: ", self.play_counter)
                    print("Answer Dictionary", answer_Dict)

                    answer_box = Box(self.display_screen, self.play_counter, 0)
                    answer_box.draw_box(dark_gray) 
                    answer_box.add_text(user_answer_char_list[0], self.font)  
                    
                    if (len(answer_Dict["green"]) > 0): 
                        for i in range(len(answer_Dict["green"])):
                            if answer_Dict.get("green")[i] == user_answer_char_list[0]: 
                                if user_answer_char_list[0] in answer_duplicate_letters: 
                                    if user_answer_char_list[0] == self.answer_list[0]: 
                                        answer_box = Box(self.display_screen,self.play_counter, 0)
                                        answer_box.draw_box(green) 
                                        answer_box.add_text(user_answer_char_list[0], self.font)    
                                        print("green 1")
                                        break
                                else: 
                                    answer_box = Box(self.display_screen,self.play_counter, 0)
                                    answer_box.draw_box(green) 
                                    answer_box.add_text(user_answer_char_list[0], self.font)    
                                    print("green 1")
                                    break
                        
                    if (len(answer_Dict["yellow"]) > 0): 
                        for j in range(len(answer_Dict["yellow"])):
                            if answer_Dict.get("yellow")[j] == user_answer_char_list[0]: 
                                answer_box = Box(self.display_screen,self.play_counter, 0)
                                answer_box.draw_box(yellow) 
                                answer_box.add_text(user_answer_char_list[0], self.font)    
                                print("yellow 1")
                                break
               
                    pygame.display.update() 
                    pygame.time.wait(2000)

                    answer_box = Box(self.display_screen, self.play_counter, 1)
                    answer_box.draw_box(dark_gray) 
                    answer_box.add_text(user_answer_char_list[1], self.font)  

                    if (len(answer_Dict["green"]) > 0): 
                        for i in range(len(answer_Dict["green"])):
                            if answer_Dict.get("green")[i] == user_answer_char_list[1]: 
                                if user_answer_char_list[1] in answer_duplicate_letters: 
                                    if user_answer_char_list[1] == self.answer_list[1]: 
                                        answer_box = Box(self.display_screen,self.play_counter, 1)
                                        answer_box.draw_box(green) 
                                        answer_box.add_text(user_answer_char_list[1], self.font)    
                                        print("green 2")
                                        break
                                else: 
                                    answer_box = Box(self.display_screen,self.play_counter, 1)
                                    answer_box.draw_box(green) 
                                    answer_box.add_text(user_answer_char_list[1], self.font)    
                                    print("green 2")
                                    break


                    if (len(answer_Dict["yellow"]) > 0):    
                        for j in range(len(answer_Dict["yellow"])):
                            if answer_Dict.get("yellow")[j] == user_answer_char_list[1]: 
                                answer_box = Box(self.display_screen,self.play_counter, 1)
                                answer_box.draw_box(yellow) 
                                answer_box.add_text(user_answer_char_list[1], self.font)    
                                print("yellow 2")
                                break
                    
                    pygame.display.update() 
                    pygame.time.wait(2000)

                    answer_box = Box(self.display_screen, self.play_counter, 2)
                    answer_box.draw_box(dark_gray) 
                    answer_box.add_text(user_answer_char_list[2], self.font)  

                    if (len(answer_Dict["green"]) > 0): 
                        for i in range(len(answer_Dict["green"])):
                            if answer_Dict.get("green")[i] == user_answer_char_list[2]: 
                                if user_answer_char_list[2] in answer_duplicate_letters: 
                                    if user_answer_char_list[2] == self.answer_list[2]: 
                                        answer_box = Box(self.display_screen,self.play_counter, 2)
                                        answer_box.draw_box(green) 
                                        answer_box.add_text(user_answer_char_list[2], self.font)    
                                        print("green 3")
                                        break
                                else: 
                                    answer_box = Box(self.display_screen,self.play_counter, 2)
                                    answer_box.draw_box(green) 
                                    answer_box.add_text(user_answer_char_list[2], self.font)    
                                    print("green 3")
                                    break
                    if (len(answer_Dict["yellow"]) > 0):  
                        for j in range(len(answer_Dict["yellow"])):
                            if answer_Dict.get("yellow")[j] == user_answer_char_list[2]: 
                                answer_box = Box(self.display_screen,self.play_counter, 2)
                                answer_box.draw_box(yellow) 
                                answer_box.add_text(user_answer_char_list[2], self.font)    
                                print("yellow 3")
                                break    

                    pygame.display.update() 
                    pygame.time.wait(2000)

                    answer_box = Box(self.display_screen, self.play_counter, 3)
                    answer_box.draw_box(dark_gray) 
                    answer_box.add_text(user_answer_char_list[3], self.font) 
                    
                    if (len(answer_Dict["green"]) > 0): 
                        for i in range(len(answer_Dict["green"])):
                            if answer_Dict.get("green")[i] == user_answer_char_list[3]: 
                                if user_answer_char_list[3] in answer_duplicate_letters: 
                                    if user_answer_char_list[3] == self.answer_list[3]: 
                                        answer_box = Box(self.display_screen,self.play_counter, 3)
                                        answer_box.draw_box(green) 
                                        answer_box.add_text(user_answer_char_list[3], self.font)    
                                        print("green 4")
                                        break
                                else: 
                                    answer_box = Box(self.display_screen,self.play_counter, 3)
                                    answer_box.draw_box(green) 
                                    answer_box.add_text(user_answer_char_list[3], self.font)    
                                    print("green 4")
                                    break
                    
                    if (len(answer_Dict["yellow"]) > 0):  
                        for j in range(len(answer_Dict["yellow"])):
                            if answer_Dict.get("yellow")[j] == user_answer_char_list[3]: 
                                answer_box = Box(self.display_screen,self.play_counter, 3)
                                answer_box.draw_box(yellow) 
                                answer_box.add_text(user_answer_char_list[3], self.font)    
                                print("yellow 4")
                                break
                     
                 
                    pygame.display.update() 
                    pygame.time.wait(2000)

                    answer_box = Box(self.display_screen, self.play_counter, 4)
                    answer_box.draw_box(dark_gray) 
                    answer_box.add_text(user_answer_char_list[4], self.font) 
                    
                    
                    if (len(answer_Dict["green"]) > 0): 
                        for i in range(len(answer_Dict["green"])):
                            if answer_Dict.get("green")[i] == user_answer_char_list[4]: 
                                if user_answer_char_list[4] in answer_duplicate_letters: 
                                    if user_answer_char_list[4] == self.answer_list[4]: 
                                        answer_box = Box(self.display_screen,self.play_counter, 4)
                                        answer_box.draw_box(green) 
                                        answer_box.add_text(user_answer_char_list[4], self.font)    
                                        print("green 5")
                                        break
                                else: 
                                    answer_box = Box(self.display_screen,self.play_counter, 4)
                                    answer_box.draw_box(green) 
                                    answer_box.add_text(user_answer_char_list[4], self.font)    
                                    print("green 5")
                                    break
                                
                    if (len(answer_Dict["yellow"]) > 0):  
                        for j in range(len(answer_Dict["yellow"])):
                            if answer_Dict.get("yellow")[j] == user_answer_char_list[4]: 
                                answer_box = Box(self.display_screen,self.play_counter, 4)
                                answer_box.draw_box(green) 
                                answer_box.add_text(user_answer_char_list[4], self.font)    
                                print("yellow 5")
                                break

                    self.play_counter = self.play_counter + 1
                    self.letter1_input_active = False
                    self.letter2_input_active = False
                    self.letter3_input_active = False
                    self.letter4_input_active = False
                    self.letter5_input_active = False
                    self.enter_button_active = False
                    self.box_grid[5][0].draw_box(user_input_color)
                    self.box_grid[5][1].draw_box(user_input_color)
                    self.box_grid[5][2].draw_box(user_input_color)
                    self.box_grid[5][3].draw_box(user_input_color)
                    self.box_grid[5][4].draw_box(user_input_color)
                    pygame.display.update() 
                    self.user_answer = ""


    
    # if not pressed in enter button, it goes here
    def mouse_down_letter(self,event): 
        if pygame.Rect(50, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): # aka answer space 1
            text = self.font.render("__", True, (0,0,0))
            self.display_screen.blit(text, (75, 575))
            self.letter1_input_active = True
        elif pygame.Rect(150, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): # aka answer space 2
            text = self.font.render("__", True, (0,0,0))
            self.display_screen.blit(text, (175,575))
            self.letter2_input_active = True
        elif pygame.Rect(250, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): # aka answer space 3
            text = self.font.render("__", True, (0,0,0))
            self.display_screen.blit(text, (275,575))
            self.letter3_input_active = True
        elif pygame.Rect(350, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): # aka answer space 4
            text = self.font.render("__", True, (0,0,0))
            self.display_screen.blit(text, (375,575))
            self.letter4_input_active = True
        elif pygame.Rect(450, 550, 100, 100).collidepoint(pygame.mouse.get_pos()): # aka answer space 5
            text = self.font.render("__", True, (0,0,0))
            self.display_screen.blit(text, (475,575))
            self.letter5_input_active = True


    """
    ########### this function is not working at all atm
    def pressed_enter(self, event):
        #change the letters that need to be changed
        for box in self.curr_row:
            print(box.letter, answer_list[box.j])
            if box.letter == answer_list[box.j]:
                box.draw_box(green)
                box.add_text(box.letter, self.font, self.display_screen)
            elif box.letter in answer_list:
                box.draw_box(yellow)
                box.add_text(box.letter, self.font, self.display_screen)

        # update curr row down
        self.update_curr_box(1, -4) # -4 so it'll go back to 0? idk if it works


"""

# class for each of the boxes on the display
class Box:
    def __init__(self, display_screen, i, j):
        self.display_screen = display_screen
                
        # box's location in the grid
        self.i = i
        self.j = j
        self.box_color = box_color
        self.letter = None

    def draw_box(self, color=box_color):
        pygame.draw.rect(self.display_screen, color, (50 + (self.j*100), 50 + (self.i*100),100,100))
        pygame.draw.rect(self.display_screen, border_color, (50 + (self.j*100), 50 + (self.i*100),100,100), width = border_width)

    def add_text(self, text, font):
        text = font.render(text, True, (0,0,0))
        self.display_screen.blit(text, (75 + (self.j*100), 75 + (self.i*100))) #so its centered in the middle of the box
        self.letter = text
        

# class for the enter button
class Button:
    def __init__(self, display_screen, font):
        self.display_screen = display_screen

        # box's location in the grid
        
        # enter button font
        text = font.render('ENTER', True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (300, 737.5)

        #ENTER button draw
        pygame.draw.rect(display_screen, button_color, (200, 700,200,75))
        pygame.draw.rect(display_screen, button_color, (200, 700,200,75), width = border_width)
        display_screen.blit(text, textRect)
        
        self.location = pygame.Rect(200, 700,200,75)


# for errors after
class Banner:
    def __init__(self, display_screen, font):
        self.display_screen = display_screen
        self.font = font

    # todo: create errors if word not in list or if word not 5 letters 


def main():

    game = Game()
    
    not_done = True

  
    while not_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_done = False

            # calls for the enter button 
            if event.type == pygame.MOUSEBUTTONDOWN and game.enter.location.collidepoint(event.pos):
                game.mouse_down_enter(event)
            
            # pressed on anywhere else
            if event.type == pygame.MOUSEBUTTONDOWN: 
                game.mouse_down_letter(event)

            if event.type == pygame.KEYDOWN:
                game.key_pressed(event)

        pygame.display.update()
        #pygame.display.flip()

if __name__ == "__main__":
    main()