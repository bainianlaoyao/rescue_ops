## Annotation by Zhang Siyun

from inputer import Inputer ## import Inputer class from inputer.py
from utils import Direction,ascii_art ## import Direction & ascii_art class, from utils.py
from map_manage import Map_manage ## import Map_manage class from map_manage.py
from game_main import Game_main ## import Game_main class from game_main.py
import time ## import time module to control the speed of transition animation

# shi boyuan
class Game_object:
    def __init__(self):
        # every class defined like xxx(Game_object) could use these variable by self.pos, also yyy(xxx) can still use
        self.is_show = True # Flag to determine if the object should be shown
        self.killable=False # Flag to determine if the object can be killed
        self.pos = [0, 0, 0]# Initial position of the object
        self.dir = [Direction.none]# Initial direction of the object
        # Game_main.ins.Add_game_object(self)


    # it will be called at every iteration of game, so write logic like check player in attack zone in it
    def Update(self):
        pass
    def Find_game_object(self,pos):
        return Map_manage.ins.game_objects[pos[0]][pos[1]][pos[2]] # Find a game object at a specific position
    def Is_ground(self,pos):
        return Map_manage.ins.map[pos[0]][pos[1]][pos[2]] == '#' # Check if the position is ground
    def sum_vector(self, a, b):
        return [x[0] + x[1] for x in zip(a, b)] # Sum two vectors element-wise
    def valid_pos(self, pos):
        return (0 <=pos[0] < len(Map_manage.ins.map) and 0 <= pos[1] < len(Map_manage.ins.map[0]) and 0 <= pos[2] < len(Map_manage.ins.map[0][0])) and self.Is_ground(pos)
        # Check if the position is valid and on ground
    def update_image(self):
        pass
# Tangziqi
class Player(Game_object):
    def __init__(self):
        super().__init__() # Initialize the parent class
        self.image = '🕺' # Image representation of the player
        self.is_dead = False # Flag to determine if the player is dead
        self.killable = True # Flag to determine if the player can be killed
        Map_manage.ins.player = self # Set the player instance in Map_manage

    def Update(self):
        inp = Inputer.ins.Get_input() # Get input from the player
        if inp:
            if inp == '0':
                Game_main.ins.exit()
            if inp in 'wasd': # Check if the input is a movement key
                dir_vec = Direction.Move_dispatch(inp) # Get the direction vector from the input
                looked_pos = self.sum_vector(self.pos, dir_vec)# Calculate the new position
                if 0 <=looked_pos[0] < len(Map_manage.ins.game_objects) and 0 <= looked_pos[1] < len(Map_manage.ins.game_objects[0]) and 0 <= looked_pos[2] < len(Map_manage.ins.game_objects[0][0]) and isinstance(self.Find_game_object(looked_pos),Goal): # Check if the new position is a goal
                    Game_main.ins.win() # Call the win method if it is a goal
                    return 1
                else:
                    if not(self.valid_pos(looked_pos)):
                        return
                        # Return if the new position is out of bounds
                    obj = self.Find_game_object(looked_pos) # Find the object at the new position
                    if obj:
                        return
                        # Return if there is an object at the new position
                    if not self.Is_ground(looked_pos):
                        return
                        # Return if the new position is not ground
                    self.Move_to(looked_pos) # Move the player to the new position
    def Move_to(self, pos):
        try:
            Map_manage.ins.Move(self.pos, pos) # Move the player to the new position
        except:
            pass # Handle any exceptions
    def update_image(self):
        self.image = Player().image

# Li yunhe (change the variable name 'Qizi' into 'Chess')
# shi boyuan
class Chess(Game_object):
    def __init__(self, direction: list[Direction], image):
        super().__init__() # Initialize the parent class
        self.image = image # Image representation of the chess piece
        self.dir = direction # Direction of the chess piece


# SHI BOYUAN
class Editor(Chess):
    def __init__(self):
        super().__init__([Direction.none], '✏️') # Initialize the parent class with no direction and an editor image
        self.restore_obj = None # Object to restore after moving
        self.name = 'editor' # Name of the editor
    def Update(self):
        from render import Render # Import Render class

        Render.ins.Butoom_add([ "ag: add ground, dg: delete ground, ao {gameobject class} {wd} : add gameobject {gameobject clas} with up and right direction, save: save map, text abc: always dispaly abc on buttom"])
        # Display editor commands
        inp = Inputer.ins.Get_long_input() # Get long input from the editor
        if inp:
            if len(inp) == 1 and inp in 'wasd': # Check if the input is a movement key
                dir = Direction.Move_dispatch(inp) # Get the direction vector from the input
                desire = [x[0] + x[1] for x in zip(dir, self.pos)] # Calculate the new position
                # if all([x>= 0 for x in desire]) and desire[0] < len(Map_manage.ins.map) and desire[1] < len(Map_manage.ins.map[0]) and desire[2] < len(Map_manage.ins.map[0][0]):
                self.Move_to(desire) # Move the editor to the new position
            else:
                match (inp): # Match the input to specific commands
                    case 'ag':
                        Map_manage.ins.Add_ground(self.pos) 
                    case 'g':
                        Map_manage.ins.Add_ground(self.pos) # Add ground at the current position
                    case 'dg':
                        Map_manage.ins.remove_ground(self.pos) # Remove ground at the current position
                    case 'save':
                        name = input('Map Name:') # Get the map name from the user
                        Map_manage.ins.Save_map(filename = name)
                        # Map_manage.ins.Save_map2(filename = name)
                    case 'anim':
                        Render.ins.Transition_anim(ascii_art.processed_images['ninja']['word'], 2, 'slide_left2right')
                        # Display a transition animation
                        time.sleep(2)
                        # Pause for 2 seconds
                        Render.ins.Transition_anim(ascii_art.processed_images['ninja']['head'], 2, 'vertical_split')
                        # Display another transition animation
                        time.sleep(4)
                        # Pause for 4 seconds
                if inp[:8] == 'showanim': # Check if the input is to show an animation
                    args = inp[8:].strip().split(' ') # Split the input into arguments
                    if len(args) == 3:
                        Render.ins.Transition_anim(ascii_art.processed_images[args[0]][args[1]], 1, args[2])
                        # Display a transition animation with arguments
                    elif len(args) == 2:
                        Render.ins.Transition_anim(ascii_art.processed_images[args[0]][args[1]], 1)
                        # Display a transition animation with arguments
                    time.sleep(2)
                    # Pause for 2 seconds to control the game speed
                if inp[:4] == 'read':
                    args = inp[4:].strip().split(' ')
                    Map_manage.ins.Read_map(args[0])
                    
                    Map_manage.ins.game_objects[0][-1][-1] = self
                    Render.ins.update_map(0) # Update the map in the render
                    Render.ins.fresh_board() # Refresh the game board
                    Map_manage.ins.update_meta() # Update the metadata for the map
                    Inputer.ins.flag = False # Reset the input flag
                    Game_main.ins.player = Map_manage.ins.player # Set the player instance
                 
                if inp[:4] == 'text':
                    args = inp[4:].strip()
                    Map_manage.ins.level_text = args
                if inp[:2] == 'ao': # Check if the input is to add a game object
                    args = inp[2:].strip().split(' ') # Split the input into arguments
                    try:
                        if len(args) == 1:
                            obj = Map_manage.ins.Init_game_object(args[0])
                            # Initialize a game object with the given class
                        else:
                            obj = Map_manage.ins.Init_game_object(args[0], [Direction.Move_dispatch(x) for x in args[1]])
                        # Initialize a game object with the given class and direction
                        self.restore_obj = obj
                        # Set the restore object
                    except:
                        print("command not valid")
                        # Print an error message if the command is not valid
                if inp == 'do':# Check if the input is to delete a game object
                    self.restore_obj =None
                    Map_manage.ins.update_meta()
                    #Map_manage.ins.Remove_game_object(self.pos) # Remove the game object at the current position
                    # self.Move_to(self.pos) # Move the editor to the current position

    def Move_to(self, pos):
        try:
            tmp = self.restore_obj # Store the current restore object
            tmp_pos = self.pos.copy() # Store the current position
            self.restore_obj = Map_manage.ins.game_objects[pos[0]][pos[1]][pos[2]] # Set the restore object to the object at the new position
            Map_manage.ins.Move(self.pos, pos) # Move the editor to the new position
            if tmp != None:
                Map_manage.ins.game_objects[tmp_pos[0]][tmp_pos[1]][tmp_pos[2]] = tmp  # Restore the object at the old position
        except:
            pass # Handle any exceptions

#shi boyuan
class Sword(Chess):
    def __init__(self, direction):
        super().__init__(direction, '🤺')

    def Update(self):
        if self.dir[0] == Direction.all_dir:
            dirs = 'wasd'
            dir_vecs = [Direction.Move_dispatch(i) for i in dirs]
            self.try_dirs(dir_vecs)
        else:
            self.try_dirs(self.dir)
    def try_dirs(self,dirs):
        for dir in dirs:
            looked_pos = self.sum_vector(self.pos, dir)
            if not(self.valid_pos(looked_pos)):
                continue
            obj = self.Find_game_object(looked_pos)
            if obj:
                if obj.killable:
                    Game_main.ins.Kill(self,obj)

#shi  boyuan
class Cannon(Chess):
    def __init__(self, direction):
        super().__init__(direction, '🥷') # Initialize the parent class with a cannon image
        self.meet_obj = False # Flag to determine if the cannon has met an object
    def Update(self):
        if self.dir[0] == Direction.all_dir: # Check if the direction is all directions
            dirs = 'wasd' # Define all possible directions
            dir_vecs = [Direction.Move_dispatch(i) for i in dirs] # Get direction vectors for all directions
            self.try_dirs(dir_vecs) # Try all directions
        else:
            self.try_dirs(self.dir) # Try the specified direction
    def try_dirs(self,dirs):
        for dir in dirs:
            looked_pos = self.pos.copy() # Copy the current position
            self.meet_obj = False   # Reset the meet_obj flag               

            while True:
                looked_pos = self.sum_vector(looked_pos, dir) # Calculate the new position
                if not((0 <=looked_pos[0] < len(Map_manage.ins.game_objects) and 0 <= looked_pos[1] < len(Map_manage.ins.game_objects[0]) and 0 <= looked_pos[2] < len(Map_manage.ins.game_objects[0][0]))): # Check if the new position is valid
                    self.meet_obj = False
                    break
                obj = self.Find_game_object(looked_pos) # Find the object at the new position
                if obj:
                    if not self.meet_obj: # Check if the cannon has met an object
                        self.meet_obj = True
                    else:
                        if obj.killable: # Check if the object is killable
                            Game_main.ins.Kill(self,obj) # Kill the object
                        else:
                            self.meet_obj = False
                            break  # Break if the object is not killable
                        
                
# shi boyuan
class Ghost(Chess):
    def __init__(self, direction):
        super().__init__(direction, '👹') # Initialize the parent class with a ghost image

    def Update(self):
        if self.dir[0] == Direction.all_dir: # Check if the direction is all directions
            dirs = 'wasd' # Define all possible directions, "w", "a", "s", "d"
            dir_vecs = [Direction.Move_dispatch(i) for i in dirs] # Get direction vectors for all directions
            self.try_dirs(dir_vecs) # Try all directions
        else:
            self.try_dirs(self.dir) # Try the specified direction
        
    def try_dirs(self,dir_list):
        for dir in dir_list:
            dir_vec = Direction.Move_dispatch2(dir)  # Get the direction vector
            looked_pos = self.pos.copy() # Copy the current position
            while True:
                looked_pos = self.sum_vector(looked_pos, dir_vec) # Calculate the new position
                if not(self.valid_pos(looked_pos)): # Check if the new position is valid
                    break
                obj = self.Find_game_object(looked_pos) # Find the object at the new position
                if obj:
                    if obj.killable: # Check if the object is killable
                        Game_main.ins.Kill(self,obj) # Kill the object
                    break # Break if the object is not killable
#shi boyuan
class Horse(Chess):
    def __init__(self, direction):
        super().__init__(direction, '🐎')
        self.flag = False

    def Update(self):
        # if self.flag:
        #     from render import Render
        #     Render.ins.Buttom_add(['flag'])
        if self.dir[0] == Direction.all_dir:
            dirs = 'wasd'
            dir_vecs = [Direction.Move_dispatch(i) for i in dirs]
            self.try_dirs(dir_vecs)
        else:
            self.try_dirs(self.dir)
        for d in [Direction.Move_dispatch(i) for i in 'wasd']:
            safe = self.sum_vector(self.pos,d)
            if not(self.valid_pos(safe)):
                continue
            obj = self.Find_game_object(safe)
            if obj and obj.killable:
                self.flag = True
                break
            else:
                self.flag = False
    def try_dirs(self,dirs):
        for dir in dirs:
            
            vec = Direction.Move_dispatch2(dir)
            looked_pos = self.sum_vector(self.pos, vec)
            if not(self.valid_pos(looked_pos)):
                continue
            obj = self.Find_game_object(looked_pos)
            if obj and obj.killable:
                if not self.flag:
                    Game_main.ins.Kill(self,obj) 
# Tang ziqi
# class Horse(Chess):
#     def __init__(self, direction):
#         super().__init__(direction, '🐎') # Initialize the parent class with a horse image
#         self.flag = 0 # Flag to determine if the horse has met the player


#     def Update(self):
#         player_pos = map_manage.ins.player.pos # Get the player's position
#         all_dir = 'wasd' # Define all possible directions
#         for i in all_dir:
#             if player_pos == self.pos + Direction.Move_dispatch(i): # Check if the player is in the same position
#                 self.flag = 1 # Set the flag to 1
#         for i in all_dir:
#             if player_pos == self.pos + Direction.Move_dispatch2(i) and flag == 0: # Check if the player is in the same position
#                 self.is_dead = True # Set the horse to dead
#             if flag == 1:
#                 flag = 0 # Reset the flag

class Goal(Game_object):
    def __init__(self):
        super().__init__() # Initialize the parent class
        self.image = '☢️' # Image representation of the goal
    












