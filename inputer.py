

import threading # import threading to implement multi-threading in programs, allowing for running
                 # multiple threads concurrently

import time      # import time module to control the speed of transition animation
import sys       # import sys to access system-specific parameters and functions

class Inputer:
    ins : 'Inputer' = None
    def __init__(self):
        Inputer.ins = self
        self.getch = _Getch()
        self.cur_inp = None
        self.flag = False
    def Get_input(self):
        return self.cur_inp
    def Update(self):
        if not self.flag:
            self.flag = True
            self.cur_inp = ''
            return
        inp = self.getch()
        self.cur_inp = inp #.decode('utf-8')
        # if self.cur_inp == '0':
        #     sys.exit(0)
        #     return
    def Get_long_input(self):
        if not self.flag:
            self.flag = True
            return ''
        return input()
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
 
    def __call__(self): return self.impl()
 
 
class _GetchUnix:
    def __init__(self):
        import tty, sys
 
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
 
 
class _GetchWindows:
    def __init__(self):
        import msvcrt
 
    def __call__(self):
        import msvcrt
        return msvcrt.getwch()
if __name__ == '__main__':
    getch = _Getch()
    while True:
        print('12')
        a = getch()
        print(a)
        if a == '0':
            break

