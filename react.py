from browser import document,timer,alert,html
import time
#from random import random as random1
doc=document

def random():
  return .5
def echo(ev):
  alert(doc["zone"].value)
def encode(values):
  return [str(v) for v in values]
def showHide(elt,mode=None):
  inv=doc[elt].style.visibility
  print('v',elt,inv)
  if mode == None:
    mode = inv == 'hidden'
  doc[elt].style.visibility = '' if mode else 'hidden'

class StopLights:
  def __init__(self,subjects,start):
    self.subjects=subjects
    self.interval = None
    self.green = False
    self.last = start
    self.state = 'intro'
    self.count = None
    self.gaps=[]
    
  def doOrange(self):
    timer.clear_timeout(self.interval)
    showHide('red',0)
    showHide('orange',1)
    showHide('green',0)
    self.interval=timer.set_interval(self.doGreen,2000 + random()*5000)
    
  def doGreen(self):
    timer.clear_timeout(self.interval)
    showHide('orange',0)
    showHide('green',1)
    self.green= True
    self.last= time.time()
    
  def intro(self):
    self.state = 'test'
    green =False
    doc['zone'].value = 'test'
    self.count = 3
    self.interval=timer.set_interval(self.doOrange,2000)
    
  def response(self):
    gap=time.time()-self.last
    self.gaps.append(gap)
    doc["zone"].value += '\n{}'.format(gap)
    self.count -= 1
    if self.count ==0:
      if self.state== 'test':
        self.gaps=[]
        doc['zone'].value = self.state = 'main'
        self.count = 5
      else:
        self.state = 'done'
        self.subjects[-1].setgaps(self.gaps)
        doc['result'].value = '\n'.join(
          [subject.result() for subject in self.subjects])
        doc['zone'].value = ("please email results to kaya.dahlke@gmail.com or 'click'"
            "to record another person")
    if self.count > 0: #do another test
      showHide('green',0)
      showHide('red',1)
      self.interval=timer.set_interval(self.doOrange,2000)    
  def falsePress(self):
    timer.clear_timeout(self.interval)
    self.interval=timer.set_interval(self.doGreen,2000 + random()*5000)
       
  def clicker(self,ev):
    if self.state== 'intro':
      self.intro()
    elif self.state in ('test','main'):
      if self.green:
        self.green = False
        self.response()
      else:  # pused to early so restart timer
        self.falsePress()
    else: # state 'done'
      showHide('lights',0)
      s=Subject()
      self.subjects.append(s)
      s.clear()
      showHide('ready',1)
      showHide('notetab',1)


class Subject:  
  def ready(self,ev):
    print('--{}--'.format(doc["name"].value))
    if doc['name'].value.strip() == '':
      doc['error'].value = 'name please'
      return
    for elt in ('ready','lights','notetab'):
      showHide(elt)
    doc['zone'].value ='There will be 3 test runs\n press click to start'
    self.name = doc['name'].value
    self.gender = doc['gender'].value
    self.year= doc['year'].value
  def clear(self):
    doc['name'].value = ''
    doc['gender'].value = ''
    doc['year'].value = ''
  def setgaps(self,gaps):
    self.gaps=[str(gap) for gap in gaps]
  def result(self):
    return '{},{},{},{}'.format(self.name,self.gender,self.year
          , ','.join(encode(self.gaps)))
    
showHide('green')
showHide('orange')
showHide('lights')
subjects=[Subject()]
start=time.time()
stops=StopLights(subjects,start)
doc['mybutton'].bind('click',stops.clicker)
doc['readybutton'].bind('click',subjects[-1].ready)

print("hi")
