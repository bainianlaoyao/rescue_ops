## Annotated By Zhang Siyun: start
from utils import Direction, ascii_art ## Import Direction class from utils.py 
from game_main import Game_main ## Import game_main from Game_main.py
import pickle ## Import pickle to save file for each status
import os     ## Import os to operate system-dependent functionality, including file, process management, etc
import time   ## Import time module to control the speed of transition animation
import sys    ## Import sys to access system-specific parameters and functions
from inputer import Inputer ## Import Inputer from inputer.py
## Annotated By Zhang Siyun: end

## From Line 11: Annotations made by Zhangsiyun
class Map_manage:
    ins : 'Map_manage' = None # Singleton instance of Map_manage
    def __init__(self):
        import game_object # Import game_object.py to plug in game_status
        self.is_selecting = False # Flag to determine if the map is being selected
        self.selct_image = '' # Image for selection
        Map_manage.ins = self # Set the singleton instance
        self.layer = 0 # Current layer of the map
        self.player = None  # Player object
        #3d map for overlap of player/pawns and ground
        self.map = None # 3D map structure 
        self.game_objects = None # 3D structure for game objects
        self.level_text = ""
    #shi boyuan
    #Annotated by Zhangsiyun:
    def update_meta(self):
        import game_object 
        Game_main.ins.game_objects =[]
        #Import game_object.py to plug in game_status
        for layer in range(len(self.game_objects)):
            for row in range(len(self.game_objects[layer])):
                for col in range(len(self.game_objects[layer][row])):
                    if self.game_objects[layer][row][col]:
                        obj =self.game_objects[layer][row][col]
                        obj.update_image()
                        self.game_objects[layer][row][col].pos = [layer,row,col]
                        if(isinstance(obj,game_object.Player)):
                            Map_manage.ins.player = obj
                        else:
                            Game_main.ins.Add_game_object(self.game_objects[layer][row][col])
    #shi boyuan                    
    def trim_map(self):
        u_r,b_r = 0,len(self.map[0]) -1
        l_c,r_c = 0,len(self.map[0][0]) -1
        while all([self.map[self.layer][u_r][i] == '' for i in range(len(self.map[0][0]))]) and all([self.game_objects[self.layer][u_r][i] == None for i in range(len(self.map[0][0]))]):
            u_r += 1
        while all([self.map[self.layer][b_r][i] == '' for i in range(len(self.map[0][0]))]) and all([self.game_objects[self.layer][b_r][i] == None for i in range(len(self.map[0][0]))]):
            b_r -= 1
        while all([self.map[self.layer][i][l_c] == '' for i in range(len(self.map[0]))]) and all([self.game_objects[self.layer][i][l_c] == None for i in range(len(self.map[0]))]):
            l_c += 1
        while all([self.map[self.layer][i][r_c] == '' for i in range(len(self.map[0]))]) and all([self.game_objects[self.layer][i][r_c] == None for i in range(len(self.map[0]))]):
            r_c -= 1
        self.map = [[self.map[self.layer][i][l_c:r_c+1] for i in range(u_r,b_r+1)]]
        self.game_objects = [[self.game_objects[self.layer][i][l_c:r_c+1] for i in range(u_r,b_r+1)]]

    #Chi Yin
    def Read_map(self, filename='map_0.pkl'):
        
        filepath = os.path.join('Game_data', filename)
        if os.path.exists(filepath): #Check if requested map file exists
            try:
                with open(filepath, 'rb') as map_file: 
                    mapData = pickle.load(map_file) #Load the data dictionary consisting the information of map
                    self.map = mapData['map'] #Assign self as the loaded map
                    self.game_objects = mapData['game_objects']
                    self.player = mapData.get('player')
                    self.level_text = mapData.get('text')
                    # ascii_art.images = mapData.get('images', ascii_art.images)
                    # ascii_art.processed_images = ascii_art.process_images(ascii_art.images, 80, 20) don't
                    self.is_selecting = False
                    self.selct_image = ''
                    self.layer = 0
                    Map_manage.ins = self
            except Exception as e:
                print(f'Map loading error:{e}')
        else:
            print(f'Map file {filepath} not found') #Prevent error of map doesn't exists
    #Chi Yin
    def Save_map(self, filename ='map_0.pkl'):
        filepath = os.path.join('Game_data', filename)
        os.makedirs('Game_data', exist_ok = True)
        ##add 
        import game_object
        for l in range(len(self.game_objects)):
            for r in range(len(self.game_objects[0])):
                for c in range(len(self.game_objects[0][0])):
                    if isinstance(self.game_objects[l][r][c],game_object.Editor):
                        self.game_objects[l][r][c] = None
        self.trim_map()
        mapData = {'map':self.map,'game_objects':self.game_objects,'player':self.player,'text':self.level_text,'images':ascii_art.images} #Create a dictionary to save map data
        with open(filepath,'wb') as map_file:  #create a binary data file
            pickle.dump(mapData, map_file) #Save mapData into a pickle file

    
    def Move_game_object(self,dir,dis = 1):
        pass
    #start shi boyuan
    def Add_ground(self,pos):
        # self.map[layer][x][y] = "#"
        self.map[pos[0]][pos[1]][pos[2]] = "#"
    def remove_ground(self, pos):
        self.map[pos[0]][pos[1]][pos[2]] = ""
        
    def Init_game_object(self, type: str, *args):
        import game_object
        obj = None
        obj = getattr(game_object, type)(*args)
        # Game_main.ins.game_objects.append(obj)
        return obj
        
    def Remove_game_object(self, pos):
        self.game_objects[pos[0]][pos[1]][pos[2]] = None
    def Move(self,pos1,pos2):
        if self.game_objects[pos1[0]][pos1[1]][pos1[2]] == None:
            return
        
        self.game_objects[pos2[0]][pos2[1]][pos2[2]] = self.game_objects[pos1[0]][pos1[1]][pos1[2]]
        self.game_objects[pos2[0]][pos2[1]][pos2[2]].pos = pos2
        self.game_objects[pos1[0]][pos1[1]][pos1[2]] = None
    # end

    # ## Zhang Siyun
    # ## Using function of clearing the screen
    # def clear_screen(self):
    #     print("\033[H\033[J", end="")

    # ## Designing game levels and the interface of game menu
    # def LevelOpt(self):
    #     self.is_selecting = True
    #     levelLst = []
    #     test_list= ['123','1','345234','678'] 
    #     for test_list in test_list:
    #         forelen = (17-len(test_list))//2
    #         lattlen = 17-(17-len(test_list))//2-len(test_list)
    #         ## Designing game level options: start
    #         leveloption1 = "┎-----------------┐  "
    #         leveloption2 = "|"+forelen*" "+test_list+lattlen*" "+"|  "
    #         leveloption3 = "└-----------------┘  "
    #         ## Designing game level options: end
    #         levelLst.append([leveloption1,leveloption2,leveloption3])
    #         ## Using a list to store all the game levels
    #     return levelLst

    # ## Printing levels stored from the list
    # def GameLevel(self,current_level):
    #     levelLst = self.LevelOpt()
    #     self.clear_screen()
    #     for i, level in enumerate(levelLst):
    #         if i==current_level:
    #             len1 = len(level[1])
    #             lev1 = level[1][0:len1-1]+"<"
    #             print(f"{level[0]}")
    #             print(f"{lev1}")
    #             print(f"{level[2]}")
    #             ## Use a symbol "<" to show that you are choosing the current level
    #         else:
    #             print(f"{level[0]}")
    #             print(f"{level[1]}")
    #             print(f"{level[2]}")
    #             ## The other levels are not selected, so no "<" symbols outputted.
    #     sys.stdout.flush()

    # ## Printing the interface of the game menu
    # def GameMenu(self):
    #     self.clear_screen()
    #     self.is_selecting = True
    #     print("Welcome to the Chess Game!")
    #     #list all file under game data
    #     #read all file and store in list
    #     while True:
    #         inp = Inputer.ins.Get_input()
    #         #render a image for player to select
    #         #After select, load data in where they should be 
    #         #break out to loop

    #         self.Read_map()
    #         self.selct_image = None
    #     self.is_selecting = False
        
    # ## Using the up, down, left, right button to select a level.
    # def MainInter(self):
    #     levelLst=self.LevelOpt() #execute "LevelOpt" function to read in all the levels
    #     current_level=0
    #     render_result = []
    #     test_list=['123','1','345234','678']
    #     level_name = None
    #     while True:
    #         key = sys.stdin.read(1)
    #         ## Python will read a key on the keyboard.
    #         if key == '\x1b': # ESC
    #             key += sys.stdin.read(2)
    #             if key == '\x1b[A':   # Pressing the up button
    #                 if current_level > 0:
    #                     current_level -= 1
    #             elif key == '\x1b[B': # Pressing the down button
    #                 if current_level < len(levels) - 1:
    #                     current_level += 1
    #         elif key == 'q':          # If inputing 'q', then quit the game.
    #             break
    #         print_levels(levels, current_level)
    #         for test_list in test_list:
    #             rowlis = []
    #             for str in test_list:
    #                 rowlis.append(str)
    #             render_result.append(rowlis)
    #             ## Storing characters to the render result
    #     return rowlis
   
    
    #MainInter(self)
#end


