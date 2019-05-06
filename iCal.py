from event import event
import datetime
class iCal:

    def __init__(self, data):
        self.plain = data
        # save all the data into a list
        self.plainlist = data.splitlines()

        #split this at first occurance of event start for file information
        endOfInfo = self.plainlist.index('BEGIN:VEVENT')
        self.fileInfo = self.plainlist[:endOfInfo]
        self.splitData(endOfInfo)
        #self.sortByWeeks()
        self.splitByCourse()


    def getInfo(self):
        return '\n'.join(self.fileInfo)
    
    def splitData(self, start):
        # all data after the file info
        allEventData = splitAtEvent(self.plainlist[start:])
        self.events = []
        for i in allEventData:
            self.events.append(event('\n'.join(i)))

    def getEvent(self, index): 
        return event.allInfo(self.events[index])

    def onDay(self, date): # date as DateString
        return [event.all(e) for e in self.events if event.onDay(e, date.date())]

    def splitByCourse(self):
        courses = {}
        for e in self.events:
            course = event.all(e)["SUMMARY"].strip("Deadline: ").split(" ", 1)[0].replace("s1","").replace("s2","")
            if course in courses:
                courses[course].append(event.all(e))
            else:
                courses[course] = [event.all(e)]

        for course,val in courses.items():
            courses[course] = sorted(val, key=lambda x: x["DTSTART"], reverse=False)
        
        
        self.byCourse = courses
       

    def next(self, course, date):
        if course not in self.byCourse:
            return None
        else:
            requested = self.byCourse[course]
            for e in requested:
                if e["DTSTART"] > date:
                    return e["DTSTART"]
            return "No more deadlines"
            
            





def splitAtEvent(toSplit):
    listOfSublists = []
    while True:
        try:
            startOfInfo = toSplit.index('BEGIN:VEVENT') +1
            endOfInfo = toSplit.index('END:VEVENT')
            listOfSublists.append(toSplit[startOfInfo:endOfInfo])
            #print(toSplit[startOfInfo:endOfInfo])
            toSplit = toSplit[endOfInfo + 1:]
        except ValueError:
            #EOF so exit the loop and quit the method call
            break
    return listOfSublists


