import time

class ConsoleStream():
    

    __author__ = "jay_"
    __version__ = "0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        self.file_path = '/home/jhildz737/~/redenv/data/core/logs/latest.log'

    def stream(self):
        end_str = ""
        with open(self.file_path) as f:
            for console in f.readlines():
                end_str += console + '\n'
        f.close()
        print(end_str)
        time.sleep(100)
