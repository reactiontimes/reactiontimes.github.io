from browser import document,window,timer,alert,html
import time
#from urllib import parse
#from random import random as random1
doc=document

def random():
  return .5
def echo(ev):
  alert(doc["zone"].value)

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
    doc['zone'].value = '3 test runs\n Click as soon as light goes green'
    doc['result'].value = "Orange is the warning, then 2 to 5 seconds to green\n 'Click!' as soon as green appears"
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
        doc['zone'].value = 'now 5 main runs'
        self.state = 'main'
        self.count = 5
      else:
        self.state = 'done'
        self.subjects[-1].setgaps(self.gaps)
        showHide('resultButtons',1)
        doc['result'].value = ("'Click!' to record another person or if all finished, press an email button to send results")
        if len(self.subjects) > 1:
          self.compare()
        else:
          doc['zone'].value += '\nNow next person to get a comparison!'
    if self.count > 0: #do another test
      showHide('green',0)
      showHide('red',1)
      self.interval=timer.set_interval(self.doOrange,2000)    
  def falsePress(self):
    timer.clear_timeout(self.interval)
    self.interval=timer.set_interval(self.doGreen,2000 + random()*5000)
  def compare(self):
    family = [ (sum(subject.gaps)/len(subject.gaps),subject.name) for subject in self.subjects]
    print(family)
    texts =  [ '{0[1]} score is {0[0]:.3f}'.format(person) for person in sorted(family)]
    doc['zone'].value = '\n'.join(texts)
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
      showHide('green',0)
      showHide('red',1)
      s=Subject()
      self.subjects.append(s)
      s.clear()
      doc['readybutton'].unbind('click')
      doc['readybutton'].bind('click',s.ready)
      showHide('ready',1)
      showHide('notetab',1)
      self.state = 'intro'


class Subject:  
  def ready(self,ev):
    def getGender(self):
      for gender in {'genderF','genderM'}:
        if doc[gender].checked:
          return doc[gender].value
      return None
     
    #window.open('mailto: fred@blogs?subject=stat&body=thebody','title')
    if doc['name'].value.strip() == '':
      doc['error'].value = 'Name Please'
      return
    if getGender() not in ['male','female']:
      doc['error'].value = 'Gender needs to be Male or Female'
      return
    if doc['year'].value.strip() == '':
      doc['error'].value = 'Birth Year Please'
      return
    for elt in ('ready','lights','notetab'):
      showHide(elt)
    doc['zone'].value ='There will be 3 test runs.\nPress click to start'
    self.name = doc['name'].value
    
    self.gender = getGender()
    self.year= doc['year'].value
  def clear(self):
    doc['name'].value = ''
    doc['genderF'].checked = False
    doc['genderM'].checked = False
    doc['year'].value = ''
  def setgaps(self,gaps):
    self.gaps=[gap for gap in gaps]
  @staticmethod
  def encode(values):
    def check(v):
      res='{:.5f}'.format(v)
      digits = [(ord(r)-ord('0'))*(count+1)
        for count,r in enumerate(res) if r != '.']
      res += chr(sum(digits)%10+ord('a'))
      #print(digits,res)
      return res
    return [check(v) for v in values]
  def result(self):
    return '{},{},{},{}'.format(self.name,self.gender,self.year
          , ','.join(self.encode(self.gaps)))
class Results(object):
  def __init__(self,subjects):
    self.subjects = subjects
  def results(self):
    return '\n'.join(
          [subject.result() for subject in self.subjects if hasattr(subject,'gaps')])
  @staticmethod
  def uenc(strng):
    def change(c):
      ordc=ord(c)
      hex='0123456789abcdef'
      if c <= '0':
        return '%' + hex[ordc // 16] + hex[ordc % 16]
      return c
    res=[change(c) for c in strng]
    return ''.join(res)
  def web_email(self,email):
    doc['result'].value = ('If the email button didn\'t work you can cut, paste, email the results to '+email
                           +'\nHere are your results '+self.subjects[0].name+':\n'+self.results()
                          )
  def email_kaya(self,ev):
    stringk = self.uenc('Hi Kaya,\nHere are the results from '+self.subjects[0].name+':\n')
    stringk += self.uenc(self.results())
    #print('sk',stringk)
    window.open('mailto:kaya.dahlke@gmail.com?subject=Results&body='+stringk,'Sending to Kaya')
    self.web_email('Kaya: kaya.dahlke@gmail.com')
    
  def email_sophie(self,ev):
    strings = self.uenc('Hi Sophie,\nHere are the results from '+self.subjects[0].name+':\n')
    strings += self.uenc(self.results())
    #print('ss',stringk)
    window.open('mailto:swackyweb@gmail.com?subject=Results&body='+strings,'Sending to Sophie')
    self.web_email('Sophie: swackyweb@gmail.com')

showHide('green')
showHide('orange')
showHide('lights')
showHide('resultButtons',0)
subjects=[Subject()]
start=time.time()
stops=StopLights(subjects,start)
results=Results(subjects)
""" test of mail
subjects[0].name='fred'
subjects[0].gender='Male'
subjects[0].year='2014'
subjects[0].setgaps([.2,.3])
results.email_kaya("")
"""
doc['mybutton'].bind('click',stops.clicker)
doc['readybutton'].bind('click',subjects[-1].ready)
doc['email-kaya'].bind('click',results.email_kaya)
doc['email-sophie'].bind('click',results.email_sophie)

print("hi")
