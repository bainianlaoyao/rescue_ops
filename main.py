from render import Render ## import Render class from render.py
from map_manage import Map_manage ## import Map_manage class from map_manage.py
from inputer import Inputer ## import Inputer from inputer.py
from game_main import Game_main ## import Game_main from game_main.py
import time ## import time module to control the speed of transition animation
import sys ## import sys to access system-specific parameters and functions

from utils import Direction,ascii_art ## import Direction class from utils.py
if __name__ == "__main__": ## determine whether the current script is being run as 
                           ## the main program or if it is being imported as a 
                           ## module into another script
    Inputer() # Initialize the Inputer class
    game_main = Game_main() # Initialize the Game_main class
    Map_manage() # Initialize the Map_manage class
    render = Render() # Initialize the Render class
    game_main.render = render # Assign the render instance to game_main
    game_main.inputer = Inputer.ins # Assign the inputer instance to game_main
    game_main.mode = 'game' # Set the game mode to 'game'
    ## Executing the game by importing functions in each class

    if len(sys.argv) > 1 and sys.argv[1] == 'edit': # Check if the script is run with the 'edit' argument
        game_main.mode = 'edit'  # Set the game mode to 'edit'
        Map_manage.ins.map = [[["" for i in range(render.width//4)] for j in range(render.height-3)]]
        # Initialize the map for editing
        Map_manage.ins.game_objects = [[[None for i in range(render.width//4)] for j in range(render.height-3)]]
        # Initialize the game objects for editing
        render.update_map(0)
        # Update the map in the render
        render.fresh_board()
        # Refresh the game board
        edi = Map_manage.ins.Init_game_object('Editor') # Initialize the Editor game object
        Map_manage.ins.game_objects[0][0][0] = edi # Place the Editor at the initial position
        Map_manage.ins.update_meta() # Update the metadata for the map
        Inputer.ins.flag = False # Reset the input flag
        Game_main.ins.player = Map_manage.ins.player # Set the player instance
        while True: # Main loop for the edit mode
            # game_main.Update() # Update the game state
            edi.Update()
            render.Draw_call(render.generate_map())
            # Generate and draw the map
            render.draw() # Draw the game board
            time.sleep(0.2) # Pause for 0.2 seconds to control the game speed
        
    else:
        #teset
        import game_object
        # Import game_object.py to use game objects

        # Map_manage.ins.map =  [
        #     [
        #         ['#','#','#',''],
        #         ['#','#','#','#'],
        #         ['#','','','']
        #     ]
        # ]
        # Map_manage.ins.game_objects =  [
        #         [
        #             [None,game_object.Chess([Direction.up],'tt'),None,None],
        #             [game_object.Player(),None,None,game_object.Chess([Direction.up],'🥷')],
        #             [None,game_object.Diagonal_soldier([Direction.left]),None,None]
        #         ]
        #     ]
        Render.ins.update_meta(ascii_art.processed_images['game_start']['image'][:-3])
        Render.ins.Draw_call(ascii_art.processed_images['game_start']['image'][:-3])
        Render.ins.Butoom_add(['Press "0" to quit during game',"press any key to continue"])
        Render.ins.draw()

        while True:
            Inputer.ins.Update()
            if Inputer.ins.cur_inp:
                break
        test_image = [[f'{chr(ord('a')+i% 26)}' for _ in range(124)] + ['e'] for i in range(42)]
        test_image = test_image[:18] + ['\n'] * 2 + [list('Intelligent alien beings have taken over all nuclear plants and ')] +[list('are about to conquer Earth with their spaceship, the "Devourer." Steal the nuclear ')] + [list('materials from the plants to save our home planet!')]+['\n'] * 2 + test_image[25:-5] +['please make sure this test image are rectangle, and you see "a" line in first row, letter "e" in end of each row.   ','if not, please press "0" twice to quit game, and resize your terminal and enter again']+[' ' * 40 +'\033[91mNever change terminal size during game!\033[0m'] * 3

        Render.ins.update_meta(test_image)
        Render.ins.Draw_call(test_image)
        
        Render.ins.Butoom_add(['press any key to continue'])
        Render.ins.draw()
        while True:
            Inputer.ins.Update()
            if Inputer.ins.cur_inp:
                break
        Game_main.ins.game() # Start the game in normal mode
    


