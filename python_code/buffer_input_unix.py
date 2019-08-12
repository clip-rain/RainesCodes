import sys


class _Getch:
    '''
    compatible system input component.
    '''

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    '''
    unix system
    '''

    def __init__(self):
        import tty

    def __call__(self):
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    '''
    windows system
    '''

    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getwch()


class _MyInput():

    def __call__(self):
        self.getch = _Getch()
        return self.input()

    def __init__(self, buf=[], prefix=""):
        self.prefix = prefix
        self.buffer = buf

    # must be invoked after invoking get_input 
    def get_input_buffer(self):
        return ''.join(self.buffer)

    def get_last_line(self):
        return self.prefix + self.get_input_buffer()

    def input(self):
        '''
        get the input from console.
        :return:
        '''
        while True:
            # clear the rest of the line.
            print("\r" + self.prefix + ''.join(self.buffer), end='', flush=True)
            sys.stdout.write('\033[K')
            # l is the input.
            l = self.getch()
            # return
            if l == '\r':
                input_content = ''.join(self.buffer)
                print("\r" + self.prefix + ''.join(self.buffer), end='\033[K\n')
                self.buffer = []
                return input_content
            # delete
            if l == '\x7f' and len(self.buffer) > 0:
                self.buffer.pop()
            # ctrl + z
            else:
                if l == '\x1a':
                    sys.exit()
                # append all others.
                else:
                    self.buffer.append(l)


if __name__ == '__main__':
    inp = _MyInput(prefix="lei >>")
    inp()
