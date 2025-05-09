
from map_manage import Map_manage #Import Map_manage class from map_manage.py to access map data
import os #Import os module to interact with operating system (e.g. getting terminal size)
import shutil #used if player changes terminal size
from utils import Direction,ascii_art #Import Direction from utils for rendering directional indicators
import time #Import time module to control the speed of transition animation
class Render:
    ins = None
    
 
    def __init__(self):
        Render.ins = self #Set class instance to allow global access
        self.image : list = [] #Initialize a string variable to hold the render output
        self.middle_result = None #Initialize a temporary variable to store the content to be rendered example: ['[  ]','[  ]','[  ]']
        self.width = os.get_terminal_size().columns #Get terminal width to prepare for render
        self.height = os.get_terminal_size().lines -1 #Get terminal height to prepare for render
        self.cnt = 0
        ascii_art.processed_images= ascii_art.process_images(ascii_art.images, self.width, self.height)
        #self.min_width = 600   
        #self.min_height = 600  

    def fresh_board(self):
        print('\n' * (self.height+1),end='') #Clears the screen by printing empty lines, +1 to print sufficient empty lines
        
    def update_map(self,layer):
        self.map_layer = layer #Current Map Layer Index
        self.cur_map_layer = Map_manage.ins.map[layer] #Retrieve Current Map Layout
        self.cur_game_objects = Map_manage.ins.game_objects[layer] #Retrieve Current Game Objects in the current Map Layer
        self.map_height = len( self.cur_map_layer) #Get Map Height
        self.map_width = len( self.cur_map_layer[0]) #Get Map Width
        
        #Create a format list with empty strings for formatting 
        Max_length = max([len(x) for x in self.cur_map_layer]) #Find the longest row
        Empty_lines = ' '*4*Max_length #Create empty strings with the appropriate length
        self.update_meta([Empty_lines] * self.map_height) #Update formatting metadata

    def update_meta(self,format):
        self.post_process = [None for i in range(self.height)] #Initialize a list for extra content
        self.empty_post_process = self.post_process.copy()
        #max to prevent negative value
        self.top_gap = max((self.height - len(format)) // 2, 0) #Calculate top padding
        self.left_gap = max((self.width - len(format[0])) // 2, 0) #Calculate left padding
        self.bottom_gap = max(self.height - len(format) - self.top_gap, 0) #Calculate bottom padding
        self.right_gap = max(self.width - len(format[0]) - self.left_gap-2, 0) #Calculate right padding

    def Update_terminal_size(self): #to prevent wrong calculation in top_gap or left_gap when player changes the terminal size
        size = shutil.get_terminal_size()
        self.width = size.columns
        self.height = size.lines - 1
    
    def Render_top_padding(self):
        # if self.top_gap>0:
        #     self.image += str(self.cnt) #Add counter value at the top if there is a / are gap(s) 
        # self.cnt += 1 #Increment counter value
        #Add top padding lines
        for i in range(self.top_gap):
            # if i < len(self.post_process) and self.post_process[i]: #I added an extra condition i < len(self.post_process) to prevent index out of range error - Chi Yin 
            if self.post_process[i]: #I added an extra condition i < len(self.post_process) to prevent index out of range error - Chi Yin 
                str_len = len(self.post_process[i]) #Get the length of the additional content
                self.image.append(list(self.post_process) + [' ' for i in range(self.width - str_len - 1)]) #Add any additional content
            else:
                self.image.append([' ' for i in range(self.width)]) #Go to next line if no additional content (from tmp_content)
        # self.image += '\n' * (self.top_gap)

    def Render_content(self):
        #Add the map and game objects with left paddings
        for line in self.middle_result:
            construct = []
            if self.left_gap > 0:
                construct += [' ' * self.left_gap] 
            for block in line:
                construct += list(block)    #rasterisation
            if self.right_gap > 0:
                construct += [' ' * self.right_gap]
            self.image.append(construct)
        #     self.image+= ' ' * self.left_gap
        #     self.image += ''.join(line)
        #     self.image += '\n'
        # self.image+= ' ' * self.left_gap
        # self.image += self.middle_result[-1]

    def Render_bottom_padding(self):
        #Add bottom paddings
        for i in range(self.height - self.bottom_gap, self.height):
            # print(i)
            if self.post_process[i]:
                str_len = len(self.post_process[i])
                self.image.append(list(self.post_process[i]) + [' ' for _ in range(self.width - str_len-1)])
            else:
                self.image.append([' ' for _ in range(self.width)])

    def draw(self):
        self.Update_terminal_size()
        #if size.width < self.min_width or self.height < self.min_height:    As mentioned above, I aint sure about the min size of terminal required so i kept it as comment first - Chi Yin
            #os.system('clear')
            #print('Resize the terminal to continue.')
            #return

        self.image = [] #Reset image string
        # if self.top_gap>0:
        #     self.image += str(self.cnt) #Add counter value at the top if there is a / are gap(s) 
        # self.cnt += 1 #Increment counter value

        self.Render_top_padding()
        self.Render_content()
        self.Render_bottom_padding()
        self.post_process = self.empty_post_process.copy()


         
         #Clear terminal screen
        self.print_image()

    def print_image(self):
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Linux/Mac
            os.system('clear')
        for line in self.image:
            print(''.join(line))
            # print()
        # print(self.image,end = '') #Print the complete image of the map

    def Render_game_object(self, Game_Object):
        dirs = ''.join([Direction.render_map[dir] for dir in Game_Object.dir]) #String to hold directional indicators of game objects (e.g. pawns)
        dirs = (dirs*2)[:2] #Ensure 2 symbols representing direction
        return f'{dirs[0]}{Game_Object.image}{dirs[1]}'

    def Render_map_cell(self, cell):
        match cell:
            case '#':
                return '[  ]' 
            case '':
                return '    ' 
            case _:
                return '    '

    def Render_cell(self, r, c):
        Game_Object = self.cur_game_objects[r][c]
        if Game_Object:
            return self.Render_game_object(Game_Object)
        else:
            return self.Render_map_cell(self.cur_map_layer[r][c])

    def Generate_line(self, row):
        return [self.Render_cell(row, column) for column in range(self.map_width)]

    def generate_map(self):
        map_str = [self.Generate_line(i) for i in range(self.map_height)] #A list to hold each line of a map as a string
        return map_str  #Return completed map as a list of string

    def Draw_call(self,content):
        self.middle_result = content #Set the content to be drawn in the next frame

    def Butoom_add(self,add_list:list[str]):
        tmp = []
        for x in add_list:
            while True:
                tmp.append(x[:self.width]) #Ensure each line does not exceed terminal width
                if len(x) < self.width:
                    break
                x = x[self.width:] #Move the next segment if the line is too long
        add_list = tmp  
        if self.bottom_gap >= len(add_list):
            for i in range(len(add_list)):
                self.post_process[-(len(add_list) - i)] = add_list[i] #Add content to the bottom lines
    def Transition_anim(self, target_image, transition_time, transition_type = 'vertical_split'):
        prev_image = self.image
        cur_image = []
        min_delay = 0.05  # 设置最小delay值
        match transition_type:
            case 'vertical_split':
                steps = self.width // 2
                delay = transition_time / steps
                if delay < min_delay:
                    steps_per_iteration = max(1, int(steps * min_delay / transition_time))
                else:
                    steps_per_iteration = 1

                step = 0
                while step <= steps:
                    cur_image = []
                    for i in range(len(prev_image)):
                        left_part = prev_image[i][:steps - step]
                        middle_part = target_image[i][steps - step:steps + step]
                        right_part = prev_image[i][steps + step:]
                        cur_image.append(left_part + middle_part + right_part)
                    self.image = cur_image
                    self.print_image()
                    time.sleep(max(delay, min_delay))
                    step += steps_per_iteration
                self.image = target_image
                self.print_image()
                time.sleep(max(delay, min_delay))
            case 'horizontal_split':
                steps = self.height // 2
                delay = transition_time / steps
                if delay < min_delay:
                    steps_per_iteration = max(1, int(steps * min_delay / transition_time))
                else:
                    steps_per_iteration = 1

                step = 0
                while step <= steps:
                    top_part = prev_image[:steps - step]
                    middle_part = target_image[steps - step:steps + step]
                    bottom_part = prev_image[steps + step:]
                    cur_image = top_part + middle_part + bottom_part
                    self.image = cur_image
                    self.print_image()
                    time.sleep(max(delay, min_delay))
                    step += steps_per_iteration
                self.image = target_image
                self.print_image()
                time.sleep(max(delay, min_delay))
            case 'slide_left2right':
                steps = self.width
                delay = transition_time / steps
                if delay < min_delay:
                    steps_per_iteration = max(1, int(steps * min_delay / transition_time))
                else:
                    steps_per_iteration = 1

                step = 0
                while step < steps:
                    cur_image = []
                    for i in range(len(prev_image)):
                        line = target_image[i][:step] + prev_image[i][step+1:]
                        cur_image.append(line)
                    self.image = cur_image
                    self.print_image()
                    time.sleep(max(delay, min_delay))
                    step += steps_per_iteration
                self.image = target_image
                self.print_image()
                time.sleep(max(delay, min_delay))
            case 'slide_right2left':
                steps = self.width
                delay = transition_time / steps
                if delay < min_delay:
                    steps_per_iteration = max(1, int(steps * min_delay / transition_time))
                else:
                    steps_per_iteration = 1

                step = 0
                while step < steps:
                    cur_image = []
                    for i in range(len(prev_image)):
                        line = prev_image[i][:self.width - step - 1] + target_image[i][self.width - step:]
                        cur_image.append(line)
                    self.image = cur_image
                    self.print_image()
                    time.sleep(max(delay, min_delay))
                    step += steps_per_iteration
                self.image = target_image
                self.print_image()
                time.sleep(max(delay, min_delay))
            case 'none':
                self.middle_result = target_image
                time.sleep(transition_time)
        
    
        
    

    # argurment: (x, ababa)
    # return : (a:int, ababa)
    def ababa(self,x):

        return 0






