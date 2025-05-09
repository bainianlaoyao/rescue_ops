
from utils import Direction, ascii_art ## Import Direction class from utils.py 
from game_main import Game_main ## Import game_main from Game_main.py
import pickle ## Import pickle to save file for each status
import os     ## Import os to operate system-dependent functionality, including file, process management, etc
import time   ## Import time module to control the speed of transition animation
import sys    ## Import sys to access system-specific parameters and functions
from inputer import Inputer ## Import Inputer from inputer.py

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
    