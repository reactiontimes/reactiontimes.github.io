from browser import document,timer,alert,html
import time
from random import random
start=time.time()
last=start
state='intro'
count=0
interval=None
gaps=[]

doc=document
def echo(ev):
    alert(document["zone"].value)
def encode(gaps):
    return ['{:.3f}'.format(gap) for gap in gaps]
def doOrange():
    global interval
    timer.clear_timeout(interval)
    showHide('red',0)
    showHide('orange',1)
    showHide('green',0)
    interval=timer.set_interval(doGreen,2000 + random()*5000)
def doGreen():
    global green,last,interval
    timer.clear_timeout(interval)
    showHide('orange',0)
    showHide('green',1)
    green= True
    last= time.time()

def clicker(ev):
    global state,count,timer,interval,green,gaps
    if state== 'intro':
        state = 'test'
        green =False
        doc['zone'].value = 'test'
        count = 3
        interval=timer.set_interval(doOrange,2000)
    elif state in ('test','main'):
        if green:
            green = False
            gap=time.time()-last
            gaps.append(gap)
            doc["zone"].value += '\n{}'.format(gap)
            count -= 1
            if count ==0:
                if state== 'test':
                    green =False
                    gaps=[]
                    doc['zone'].value = state = 'main'
                    count = 5
                    interval=timer.set_interval(doOrange,2000)
                else:
                    state = 'done'
                    doc['result'].value = '{},{},{},{}'.format('nm','gn','yr'
                    ,','.join(encode(gaps)))
                    doc['zone'].value = 'please email results to '
            else: #do another test
                interval=timer.set_interval(doOrange,2000)
        else:  # pused to early so restart timer
            timer.clear_timeout(interval)
            interval=timer.set_interval(doGreen,2000 + random()*5000)
    else: # state 'done'
          pass
def calc():
 global last
 now=time.time()
 gap=now - last
 last=now
 doc["zone"].value= '{}'.format(gap)
def showHide(elt,mode=None):
 inv=doc[elt].style.visibility
 print('v',elt,inv)
 if mode == None:
   mode = inv == 'hidden'
 doc[elt].style.visibility = '' if mode else 'hidden'

def ready(ev):
 #flip('mybutton')
 print('--{}--'.format(doc["name"].value))
 if doc['name'].value.strip() == '':
   doc['error'].value = 'name please'
   return
 for elt in ('ready','lights','notetab'):
   showHide(elt)
 doc['zone'].value ='There will be 3 test runs\n press click to start'
showHide('green')
showHide('orange')
showHide('lights')
doc['mybutton'].bind('click',clicker)
doc['readybutton'].bind('click',ready)

print("hi")