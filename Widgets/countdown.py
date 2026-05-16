import Brick
from datetime import datetime, timedelta
class dialogstyle(Brick.Brick):
    

def _open_dialog(self):
    pass

def input_date(date):
    pass



def target_input():
    i=input("YYYY-mm-dd")
    target=datetime.strptime(i, "%Y-%m-%d")
    return target


def countdown(target):
    
    start=datetime.now()
    timeleft=target-start
    return timeleft
    
