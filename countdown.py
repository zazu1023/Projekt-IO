
from datetime import datetime, timedelta
class dialogstyle:
    bg:str
    font_size:int
    text_colour:str

    hight:int
    width:int

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
    