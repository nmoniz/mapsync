from signal import pause

__author__ = 'natercio'

import time

class Stopwatch:

    def __init__(self, paused):
        self.total_time = 0
        self.last_time = int(round(time.time()*1000))
        self.paused = paused

    def reset(self):
        self.total_time = 0;
        self.last_time = int(round(time.time()*1000))

    def time(self):
        if not self.is_paused():
            current = int(round(time.time()*1000))

            self.total_time += current - self.last_time
            self.last_time = current

        return self.total_time

    def pause(self):
        if not self.is_paused():
            paused = True
            self.time()

    def resume(self):
        if self.is_paused():
            self.paused = False
            lastTime = int(round(time.time()*1000))

    def is_paused(self):
        return self.paused


def main():
    pass

if __name__ == "__main__":
    main()
