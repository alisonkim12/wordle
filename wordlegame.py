
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
    font = pygame.font.Font('freesansbold.ttf', 25)
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

        self.box_grid = []
        for i in range(6): # n of rows
            box_list = []
            for j in range(5): # n of columns
                box = Box(self.display_screen, i, j)
                box.draw_box() # draw box on display
                box_list.append(box)
            self.box_grid.append(box_list)
        
        # set where the words will be typed
        self.curr_row = 0 # based on how many words have been guessed
        self.curr_col = 0 # based on how many ch have been typed/deleted
        self.curr_box = self.box_grid[self.curr_row][self.curr_col]

    def start():
        return
    
    def update_curr_box(self, p, q): # args are by what you want to incr/decr the indexes by
        self.curr_row = self.curr_row + p
        self.curr_col = self.curr_col + q
        self.curr_box = self.box_grid[self.curr_row][self.curr_col]
    
    ########### letters are printing on the screen now!!! but not working perfectly
    def key_pressed(self, event):
        if event.key == pygame.K_BACKSPACE: 
            # delete letter and set curr box to previous one
            self.curr_box.draw_box()
            if self.curr_col != 0:
                self.update_curr_box(0, -1)  
            # todo: fix this so it works in more situations
        elif event.key == pygame.K_RETURN:
            # check if there are 5 letters + word in list, then enter + update colors etc
            # todo: all of this
            pass
        else: 
            # try and catch bc not all other chars will be alphabetic
            try: 
                ch = chr(event.key).lower()
                self.curr_box.add_text(ch, self.font, self.display_screen)
                if self.curr_col != 4:
                    self.update_curr_box(0, 1)
            except:
                print("aaaah error")
    
    ########### this function is not working at all atm
    def pressed_enter(self):
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

    def add_text(self, text, font, display_screen):
        text = font.render(text, True, (0,0,0))
        display_screen.blit(text, (50 + (self.j*100), 50 + (self.i*100)))
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


# Part 2: Function (param: user's word guess)(returns a dictionary of what letters of the game board should change)

def every_input(user_word): 
    color_change_Dict = {"green": [], "yellow": []}
    og_list = []
    char_list = list(user_word) #putting the word into a list of individual char
    for i in range(len(char_list)): 
        for j in range(len(word_answer_char)): 
            if char_list[i] == word_answer_char[j]:
                if i == j: 
                    print("Char: ", char_list[i])
                    color_change_Dict["green"].append(char_list[i])
                    print("APPEND: ", color_change_Dict["green"])

                else: 
                    og_list = color_change_Dict["yellow"]
                    color_change_Dict["yellow"].append(char_list[i])

    return color_change_Dict

"""
Letter_class_list = []
Letter_class_list_input = []


#For every round 
user_text = ""
user_answer = ""  

not_done = True
enter_button_active = False
letter1_input_active = False
letter2_input_active = False
letter3_input_active = False
letter4_input_active = False
letter5_input_active = False
play_counter = 0
"""

"""def update(user_answer): 
    user_answer_char_list = list(user_answer)

    for i in range(5): 
        txt_surface = font.render(user_answer_char_list[i], True, (0,0,0))
      #  Letter_class_list[(play_counter*5)+i].text = user_answer_char_list[i]
        Letter_class_list[(play_counter*5)+i].addText(user_answer_char_list[i])
       # screen.blit(txt_surface, (Letter_class_list[(play_counter*5)+i].left_x,Letter_class_list[(play_counter*5)+i].top_y))

    play_counter = play_counter + 1

    pygame.display.update() """

"""
while not_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            not_done = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.enter.location.collidepoint(event.pos): 
                if letter1_input_active and letter2_input_active and letter3_input_active and letter4_input_active and letter5_input_active: 
                    
                    print("User answer is: ", user_answer)
                    user_answer_char_list = list(user_answer)
                    answer_Dict = every_input(user_answer)
                    
                    txt_surface = font.render(user_answer_char_list[0], True, (0,0,0))

                    print("break 1")
                    print("Play counter: ", play_counter)

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[0]: 
                            pygame.draw.rect(display_screen, green, (50,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (50,(50+(play_counter*100)),100,100), width = border_width)
                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)].left_x + 25, Letter_class_list_input[(play_counter*5)].top_y + 25))
                            print("green 1")

                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[0]: 
                                    pygame.draw.rect(display_screen, green, (50,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (50,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)].left_x + 25, Letter_class_list_input[(play_counter*5)].top_y + 25))
                                
                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)].left_x + 25, Letter_class_list_input[(play_counter*5)].top_y + 25))
                    
                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[1], True, (0,0,0))

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[1]: 
                            pygame.draw.rect(display_screen, green, (150,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (150,(50+(play_counter*100)),100,100), width = border_width)
                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+1].left_x + 25, Letter_class_list_input[(play_counter*5)+1].top_y + 25))
                            print("green 2")

                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[1]: 
                                    pygame.draw.rect(display_screen, green, (150,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (150,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+1].left_x + 25, Letter_class_list_input[(play_counter*5)+1].top_y + 25))

                                
                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+1].left_x + 25, Letter_class_list_input[(play_counter*5)+1].top_y + 25))
                    
                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[2], True, (0,0,0))

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[2]: 
                            pygame.draw.rect(display_screen, green, (250,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (250,(50+(play_counter*100)),100,100), width = border_width)
                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+2].left_x + 25, Letter_class_list_input[(play_counter*5)+2].top_y + 25))
                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[2]: 
                                    pygame.draw.rect(display_screen, green, (250,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (250,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+2].left_x + 25, Letter_class_list_input[(play_counter*5)+2].top_y + 25))

                                
                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+2].left_x + 25, Letter_class_list_input[(play_counter*5)+2].top_y + 25))
                    
                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[3], True, (0,0,0))

                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[3]: 
                            pygame.draw.rect(display_screen, green, (350,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (350,(50+(play_counter*100)),100,100), width = border_width)

                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+3].left_x + 25, Letter_class_list_input[(play_counter*5)+3].top_y + 25))
                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[3]: 
                                    pygame.draw.rect(display_screen, green, (350,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (350,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+3].left_x + 25, Letter_class_list_input[(play_counter*5)+3].top_y + 25))

                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+3].left_x + 25, Letter_class_list_input[(play_counter*5)+3].top_y + 25))

                    #pygame.display.update() unveil each one at a time slowly like they do in the actual game (use the clock)

                    txt_surface = font.render(user_answer_char_list[4], True, (0,0,0))
                    
                    for i in range(len(answer_Dict["green"])):
                        if answer_Dict.get("green")[i] == user_answer_char_list[4]: 
                            pygame.draw.rect(display_screen, green, (450,(50+(play_counter*100)),100,100))
                            pygame.draw.rect(display_screen, border_color, (450,(50+(play_counter*100)),100,100), width = border_width)

                            display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+4].left_x + 25, Letter_class_list_input[(play_counter*5)+4].top_y + 25))
                        
                        else: 
                            for j in range(len(answer_Dict["yellow"])):
                                if answer_Dict.get("yellow")[j] == user_answer_char_list[4]: 
                                    pygame.draw.rect(display_screen, green, (450,(50+(play_counter*100)),100,100))
                                    pygame.draw.rect(display_screen, border_color, (450,(50+(play_counter*100)),100,100), width = border_width)
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+4].left_x + 25, Letter_class_list_input[(play_counter*5)+4].top_y + 25))

                                else: 
                                    display_screen.blit(txt_surface, (Letter_class_list_input[(play_counter*5)+4].left_x + 25, Letter_class_list_input[(play_counter*5)+4].top_y + 25))

                    play_counter = play_counter + 1
                    letter1_input_active = False
                    letter2_input_active = False
                    letter3_input_active = False
                    letter4_input_active = False
                    letter5_input_active = False
                    enter_button_active = False
            
            elif pygame.Rect(Letter_class_list_input[0].left_x,Letter_class_list_input[0].top_y, 100,100).collidepoint(event.pos): 
                letter1_input_active = True

            elif pygame.Rect(Letter_class_list_input[1].left_x,Letter_class_list_input[1].top_y, 100,100).collidepoint(event.pos): 
                letter2_input_active = True

            elif pygame.Rect(Letter_class_list_input[2].left_x,Letter_class_list_input[2].top_y, 100,100).collidepoint(event.pos): 
                letter3_input_active = True

            elif pygame.Rect(Letter_class_list_input[3].left_x,Letter_class_list_input[3].top_y, 100,100).collidepoint(event.pos): 
                letter4_input_active = True

            elif pygame.Rect(Letter_class_list_input[4].left_x,Letter_class_list_input[4].top_y, 100,100).collidepoint(event.pos): 
                letter5_input_active = True

        if event.type == pygame.KEYDOWN:
            if letter1_input_active or letter2_input_active or letter3_input_active or letter4_input_active or letter5_input_active: 
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                    user_answer = user_answer[:-1]
                    pygame.display.update()

                    #should change letter input active to False here technically 
                else:
                    user_text = event.unicode
                    user_answer = user_answer+user_text
                    
            txt_surface = font.render(user_text, True, (0,0,0))

            if letter1_input_active == True: 

                if letter2_input_active == True: 

                    if letter3_input_active == True: 

                        if letter4_input_active == True: 

                            if letter5_input_active == True: 

                                display_screen.blit(txt_surface, (Letter_class_list_input[4].left_x + 25,Letter_class_list_input[4].top_y + 25))
                            else: 
                                display_screen.blit(txt_surface, (Letter_class_list_input[3].left_x + 25,Letter_class_list_input[3].top_y + 25))
                        else: 
                            display_screen.blit(txt_surface, (Letter_class_list_input[2].left_x + 25,Letter_class_list_input[2].top_y + 25))
                    else: 
                        display_screen.blit(txt_surface, (Letter_class_list_input[1].left_x + 25,Letter_class_list_input[1].top_y + 25))
                else: 
                    display_screen.blit(txt_surface, (Letter_class_list_input[0].left_x + 25,Letter_class_list_input[0].top_y + 25))

    pygame.display.update()
    #pygame.display.flip()
"""

def main():

    game = Game()
    
    not_done = True
    while not_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_done = False

            if event.type == pygame.MOUSEBUTTONDOWN and game.enter.location.collidepoint(event.pos):
                game.pressed_enter(event)

            if event.type == pygame.KEYDOWN:
                game.key_pressed(event)

        pygame.display.update()
        #pygame.display.flip()

if __name__ == "__main__":
    main()