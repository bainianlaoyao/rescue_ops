# from render import Render
from inputer import Inputer # import Inputer class from inputer.py
import time                 # import time module to control the speed of transition animation
import pickle
from utils import ascii_art
import os
from time import sleep
class Game_main:
    ins = None
    def __init__(self):
        self.game_objects = [] # List to store all game objects
        self.global_vars = {} # Dictionary to store global variables
        self.render = None # Instance of the Render class for rendering the game
        self.inputer = None # Instance of the Inputer class for handling user input
        self.player = None # Instance of the Player class
        self.levels = ['Start of Odyssey','Precise and deadly','Les Trois Sword','2 guards','A one-man army','Horse','Strong Horse',"Ninja is Ninja","Do not go gentle into the ninja's array","Yollow Ghost",'Winding and twisting route','Chasing all the way','Blocked Route','Furthest Path','arduous challenge','gelea\'s champions','outflanking tactics','Endgame: Break the siege'] # List of available levels
        self.level_index = 0
        file_path = "Game_data/game_progress.pkl"

        if not os.path.exists(file_path):
            with open(file_path, 'wb') as file:
                pickle.dump([], file) 
        with open("Game_data/game_progress.pkl",'rb') as file:
            self.locks = pickle.load(file)
            if not self.locks:
                self.locks = [False] + [True for i in range(len(self.levels) - 1)] # List of level locks (True if locked, False if unlocked)
        # self.locks = [False for i in range(len(self.levels))] # very temp
        self.cur_level = '' # Current level being played
        self.is_win = False # Flag to indicate if the player has won the game
        self.is_lose = False
        Game_main.ins = self # Set the singleton instance of Game_main
        ## Line 8~17: Initialize the game status
        ## Annotated by Zhangsiyun: end
    def Update(self):
        if self.mode == 'game': # Check if the game mode is 'game'
            self.inputer.Update() # Update the input handler
            if self.player:
                r =  self.player.Update() # Update the player object if it exists
        if r != 1:
            for obj in self.game_objects: # Update all game objects
                obj.Update()
    def Add_game_object(self,obj):
        if obj not in self.game_objects: # Meaning that the object is not already in the list
            self.game_objects.append(obj) # Add the object to the list of game objects
            
    def Kill(self, killer,killed):  
        from map_manage import Map_manage
        from time import sleep
        import game_object
        char_name = ''
        slide_func1 = ''
        slide_func2 = ''
        match killer:
            case game_object.Sword():
                char_name = 'sword'
                slide_func1 = 'slide_left2right'
                slide_func2 = 'horizontal_split'
            case game_object.Horse():
                char_name = 'horse'
                slide_func1 = 'horizontal_split'
                slide_func2 = 'slide_left2right' 
            case game_object.Cannon():
                char_name = 'ninja'
                slide_func1 = 'slide_left2right'
                slide_func2 = 'vertical_split'
            case game_object.Ghost():
                char_name = 'ghost'
                slide_func1 = 'horizontal_split'
                slide_func2 = 'horizontal_split'            
        Map_manage.ins.game_objects[killed.pos[0]][killed.pos[1]][killed.pos[2]] = killer
        Map_manage.ins.game_objects[killer.pos[0]][killer.pos[1]][killer.pos[2]] = None

        self.render.Draw_call(self.render.generate_map())
        self.render.draw()
        sleep(1.2)
        
        self.render.ins.Transition_anim(ascii_art.processed_images[char_name]['word'], 1, slide_func1)
        time.sleep(0.8)
        self.render.ins.Transition_anim(ascii_art.processed_images[char_name]['head'], 2, slide_func2)
        time.sleep(0.5)
        # self.render.ins.Transition_anim(ascii_art.processed_images['game_over']['head'], 1, 'vertical_split')
        # time.sleep(0.4)
        # self.render.ins.Transition_anim(ascii_art.processed_images['game_over']['word'], 2, 'slide_left2right')
        self.render.ins.Transition_anim(ascii_art.processed_images['game_over']['word2'], 1.5, 'slide_left2right')
        time.sleep(0.4)

        self.is_lose = True
    def exit(self):
        with open("Game_data/game_progress.pkl",'wb') as file:
            pickle.dump(self.locks,file)
        import os
        os.sys.exit(0)
    def win(self):
        self.is_win = True # Set the win flag to True
        # self.render.Butoom_add([f"win"]) # Add a win message to the render

        self.render.ins.Transition_anim(ascii_art.processed_images['game_over']['head'], 1.5, 'slide_left2right')
        self.render.ins.Transition_anim(ascii_art.processed_images['win']['head'], 0.65, 'slide_right2left')
        time.sleep(1)
        self.render.ins.Transition_anim(ascii_art.processed_images['win']['word'], 1.5, 'slide_left2right')
        time.sleep(1)

    def game(self):
        from map_manage import Map_manage
        ## import Map_manage from the file map_manage.py
        while True:
            print("before select")
            name = Game_main.select_level(self.levels,self.locks,self.render.height,self.render.width // 2,self.render)
            self.cur_level = name # Set the current level to the selected level
            # Map_ame = Game_main.select_level(manage.ins.MainInter()
            Map_manage.ins.Read_map(name) # Read the map for the selected level
            self.render.update_map(0) # Update the map in the render
            self.render.fresh_board() # Refresh the game board
            Map_manage.ins.update_meta() # Update the metadata for the map
            self.inputer.flag = False # Reset the input flag
            Game_main.ins.player = Map_manage.ins.player # Set the player instance
            while True:
                self.Update() # Update the game state
                if(self.is_lose):
                    self.is_lose = False
                    break
                if(self.is_win): # Check if the player has won
                    try:
                        self.locks[self.levels.index(self.cur_level) + 1] = False # Unlock the next level
                    except IndexError:
                        pass
                    self.is_win = False # Reset the win flag

                    if not any(self.locks):
                        self.render.ins.Transition_anim(ascii_art.processed_images['win']['end'], 3, 'slide_left2right')
                        sleep(2)
                    print('Break')
                    break

                self.render.Draw_call(self.render.generate_map()) # Generate and draw the map
                if(Map_manage.ins.level_text):
                    self.render.Butoom_add([Map_manage.ins.level_text])
                self.render.draw() # Draw the game board
                
                
                
                time.sleep(0.2) # Pause for 0.2 seconds to control the game speed
            
    @staticmethod
    def display_width(s):
        width = 0
        for char in s:
            if char == "🔒": ## Use this character to design the locked level.
                width += 2
            elif ord(char) > 127:
                width += 2  # 非ASCII字符算作双宽度 # Non-ASCII characters are considered double width
            else:
                width += 1
        return width

    
    def select_level(levels, locks, max_height, max_width,render):
        # Game_main.ins.level_index = 0  # Game_main.ins.level_index: the index of the game levels. Setting zero to put the arrow at the first level.
        max_height -= 2
        max_width -= 10             
        max_width -= max_width%2
        flag = True
        while True:
            # Game_main.ins.render.Butoom_add("'ws' for move select level, 'y' for enter level")
            border_top = "┌" + "─" * (max_width + 2) + "┐   "    ## Designing the top border of the level option
            border_bottom = "└" + "─" * (max_width + 2) + "┘   " ## Designing the bottom border of the level option
            result = []
            for idx, (level, locked) in enumerate(zip(levels, locks), 1):
                arrow = " 🕺" if idx - 1 == Game_main.ins.level_index else "    " ## If selecting the level, put the arrow "<--" right next to the game level option
                if locked:
                    lock_line = "❎" * ((max_width) // 2)     
                    result.append(border_top)
                    result.append(f"│ {lock_line} │{arrow}")
                    result.append(border_bottom)
                    ## line 84~88: Designing the locked level, using the symbol "❎".
                else:
                    level_str = f"{idx}. {level}" ## Giving the format of the level name, with "idx" the level position, "level" the name of level.
                    level_width = Game_main.display_width(level_str) ## Setting up the width of the level
                    total_padding = max_width - level_width # total_padding: the number of characters not occupied by the level name.
                    ## line 94 & 95: calculate the empty spaces for left and right paddings
                    left_padding = total_padding // 2    
                    right_padding = total_padding - left_padding
                    ## use the left_padding and right_padding to fill with space character ' '
                    result.append(border_top)
                    ## save the top border of level option into the result
                    if idx - 1 == Game_main.ins.level_index:
                        result.append(f"│ {' ' * left_padding}{level_str}{' ' * right_padding} │{arrow}") 
                        # If selecting the level, there will be an arrow in the option
                    else:
                        result.append(f"│ {' ' * left_padding}{level_str}{' ' * right_padding} │{arrow}") 
                        # If not selecting the level, there won't be an arrow in the option
                    result.append(border_bottom)
                    ## save the bottom border of level option into the result
            if len(result) > max_height:
                start_index = max(0, Game_main.ins.level_index * 3 - max_height // 2)
                end_index = min(len(result), start_index + max_height)
                result = result[start_index:end_index]
            result = [[x for x in line] for line in result]
            render.Draw_call(result)
            
            if flag:
                render.update_meta(result)
                flag = False
            render.Butoom_add(['"ws" for move select, press "y" to enter level'])
            render.draw()
            ## From line 110 to line 116, print out the interface of the game.

            # print("\n".join([''.join(line) for line in  result]))
            # print("\n".join(result))
            Inputer.ins.Update()
            key = Inputer.ins.Get_input()
            ## Read a character on keyboard to opt for a game level:
            ## 1. "w": scrolling up
            ## 2. "s": scrolling down
            ## 3. "y": enter and load the chosen game to print out the game graphics
            if key == None:
                continue
            if key == '0':
                Game_main.ins.exit()
            if key.lower() == 'w' and Game_main.ins.level_index > 0:
                Game_main.ins.level_index -= 1 ## The arrow moves to the previous level if pressing 'w' (upwards).

                # while locks[Game_main.ins.level_index]:
                #     if Game_main.ins.level_index > 0:
                #         Game_main.ins.level_index -= 1
                #     else:
                        # break

            elif key.lower() == 's' and Game_main.ins.level_index < len(levels) - 1:
                Game_main.ins.level_index += 1 ## The arrow moves to the next level if pressing 's' (downwards).

                # while locks[Game_main.ins.level_index]:
                #     if Game_main.ins.level_index < len(levels) - 1:
                #         Game_main.ins.level_index += 1
                #     else:
                #         break

            elif key.lower() == 'y': ## selecting the game to play
                if not locks[Game_main.ins.level_index]:
                    return levels[Game_main.ins.level_index]
                    ## return the unlocked level, then start the game
                else:
                    print("locked level")
                    ## for locked level, we can not choose hence this level can't be started
                    
            ## Choosing a level of game
        
    


