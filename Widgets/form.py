
import Brick
class text_field():
    text:str
    next:text_field
    prev:text_field
class form(Brick.Brick):
    first_text:text_field

    pass


def form_numbers():
   i= input()
   
   x=i.isnumeric()
   if (x==False):
       return 1

   #i do bazy danych
   return 0

def form_else():
     i= input()
     #i do bazy danych
     return 0

