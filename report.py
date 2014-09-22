class Person:
    def __init__(self,line):
        hold = line.split(',')
        self.name,self.gender,self.year = hold[:3]
        self.goes =[float(go) for go in hold[3:]]
        #print(self.goes)
        if len(self.goes) !=5:
            raise ValueError('naughty '+self.name)
        self.average = sum(self.goes)/len(self.goes)
    def __str__(self):
        return self.name
    def __repr__(self):
        return '(Person:{} {})'.format(self.name,self.average)

class Report:
    def __init__(self,line):
        hold = line.split(',')
        self.name=hold[0]
        self.age_start = int(hold[1])
        self.age_end = int(hold[2])
        self.gender = hold[3].lower()
        if self.gender not in ['male','female','all']:
            raise ValueError('Gender error '+self.gender)
    def check(self,person):
        if self.gender != 'all':
            if person.gender.lower() != self.gender:
                return False
        age = 2014 - int(person.year)
        return self.age_start <= age <= self.age_end
        
with open("playtext.txt") as f:
    people = [Person(line.strip()) for line in f if not line.startswith('#')]

with open("reports.txt") as f:
    reports = [Report(line.strip()) for line in f if not line.startswith('#')]
    
#print(people)

for report in reports:
    keeps = [person for person in people if report.check(person)]
    avgs = [person.average for person in keeps]
    try:
        average = sum(avgs)/len(avgs)
    except ZeroDivisionError:
        average = 0
    #print(keeps)
    print('Group Name: {} Average Score: {:.3f}'.format(report.name,average))
