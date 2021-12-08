import logging
import datetime

class tiny_timer():
    def __init__(self,tot,timer_step=300,max_time_stuck=900,log_level=logging.DEBUG):
        self.tot=tot
        self.cnt=0
        self.step=1
        self.timer_step=timer_step
        self.max_time_stuck=max_time_stuck
        self.stuck_start=datetime.datetime.now()
        self.global_start=datetime.datetime.now()
        self.logger=logging.getLogger('timer')
        self.logger.setLevel(log_level)
    def check_timer(self,cnt):
        very_stuck=False
        if self.tot>cnt:
            if self.cnt<cnt:
                self.stuck_start=datetime.datetime.now()
            else:
                stuck_time=datetime.datetime.now()-self.stuck_start
                if stuck_time.total_seconds()>=self.max_time_stuck:
                    very_stuck=True
            elapsed_time=datetime.datetime.now()-self.global_start
            if cnt>0:
                time_left=elapsed_time/cnt*(self.tot-cnt)
            else:
                time_left=elapsed_time*self.tot
            if elapsed_time.total_seconds()>=self.step*self.timer_step:
                self.logger.info('{} items processed [{}]. '.format(cnt,str(elapsed_time).split('.')[0]) + \
                                 '{} items left [{}]'.format(self.tot-cnt,str(time_left).split('.')[0]))
                self.step=int(elapsed_time.total_seconds()/self.timer_step)+1
            seconds_left=time_left.total_seconds()
        else:
            seconds_left=0
        self.cnt=cnt
        return seconds_left,very_stuck