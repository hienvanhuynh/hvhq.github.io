from datetime import datetime

class timer:
    def __init__(self):
        self.sum_time = 0
        self.resume()
    
    def restart(self):
        self.sum_time = 0
        self.start_time = 0

    def pause(self):
        self.sum_time += datetime.now().timestamp() - self.start_time
        self.start_time = 0
    
    def resume(self):
        self.start_time = datetime.now().timestamp()
    
    def decrease_time(self, numseconds = 3):
        self.sum_time -= numseconds

    def get_miliseconds(self):
        if self.start_time != 0:
            cur_time = datetime.now().timestamp()
            return (self.sum_time + cur_time - self.start_time) * 1000
        else:
            return self.sum_time * 1000
    
    def get_seconds(self):
        if self.start_time != 0:
            cur_time = datetime.now().timestamp()
            return self.sum_time + cur_time - self.start_time
        else:
            return self.sum_time

class chess_timer:
    def __init__(self, turn = 1):
        if(turn < 1):
            turn = 1
        if(turn > 2):
            turn =2
        self.turn = turn
        self.timer1 = timer()
        self.timer2 = timer()
        if turn == 1:
            self.timer2.restart()
        else:
            self.timer1.restart()
    
    def change_turn(self, to_turn = 0):
        if self.turn == to_turn:
            return 0

        if self.turn == 1:
            self.timer1.pause()
            self.timer2.resume()
            self.turn = 2
            self.increase_time(1)
            return 2
        else:
            self.timer2.pause()
            self.timer1.resume()
            self.turn = 1
            self.increase_time(2)
            return 1
    
    def get_time1_seconds(self, time_limit=-1):
        if time_limit==-1:
            return self.timer1.get_seconds()
        else:
            return time_limit - self.timer1.get_seconds()
    
    def get_time2_seconds(self, time_limit=-1):
        if time_limit==-1:
            return self.timer2.get_seconds()
        else:
            return time_limit - self.timer2.get_seconds()
        
    def get_sum_time(self):
        return self.timer1.get_seconds() + self.timer2.get_seconds()
    
    def increase_time(self, timerid):
        if timerid == 1:
            self.timer1.decrease_time(numseconds=2)
        else:
            self.timer2.decrease_time(numseconds=2)

    def __delattr__(self):
        del self.timer1
        del self.timer2
