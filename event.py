import re
from datetime import datetime, timedelta

class event:
    def __init__(self, data):
        #print("1: {}\n2: {}\n3: {}\n4: {}\n5: {}".format(data[1],data[2],data[3],data[4],data[5]))     
        self.plain = data
        keys = ["DTSTAMP","SUMMARY","LOCATION","DESCRIPTION","TZID","DTSTART","DTEND","RRULE","EXDATE","UID"]
        self.info = {key: None for key in keys}

        for key in keys:
            if key in data:
                start = data.index(key) + len(key) + 1 # +1 is for starting colon :
                matches = re.search(r"(?=("+'|'.join(keys)+r"))", data[start:])
                if matches is not None:
                    end = start + matches.start()
                    value = data[start:end].replace('\n ' ,'').strip(' \n')
                else:
                    value = data[start:].replace('\n ','').strip(' \n')

                if value is '':
                    value = None
                
                if "DT" in key and value is not None:
                    value = datetime.strptime(value.strip('Z'),"%Y%m%dT%H%M%S") 

                self.info[key] = value

        
        if self.info["EXDATE"] is not None:
            self.info["EXDATE"] = [datetime.strptime(date,"%Y%m%dT%H%M%S") for date in self.info["EXDATE"].split(',')] 

        if self.info["RRULE"] is not None:
            rule = self.info["RRULE"]
            if "FREQ" in rule:
                start = rule.index("FREQ") + 5
                freq = rule[start: rule[start:].index(';') + start].strip('\n ')
            if "UNTIL" in rule:
                start = rule.index("UNTIL") + 6
                try:
                    until = rule[start: rule[start:].index(';') + start].strip('\n ')
                except ValueError:
                    until = rule[start:].strip('\n ')
                until = datetime.strptime(until.strip('Z'),"%Y%m%dT%H%M%S")
            self.info["RRULE"] = {"FREQ": freq, "UNTIL": until}



#keys = ["DTSTAMP","SUMMARY","LOCATION","DESCRIPTION","TZID","DTSTART","DTEND","RRULE","EXDATE","UID"]
    def all(self):
        return self.info

    def __str__(self):
        return "{}\n{}\n{} to {}".format(self.info["SUMMARY"], self.info["DESCRIPTION"], self.info["DTSTART"].time(), self.info["DTEND"].time()) 

    def __repr__(self):
        return str(self)

    def allInfo(self):
        return self.info

    def onDay(self, date): # date is a datetime
        if date == self.info["DTSTART"].date():
            return True
        if date < self.info["DTSTART"].date():
            return False
        if self.info["EXDATE"] is not None:
            if date in [d.date() for d in self.info["EXDATE"]]:
                return False
        if self.info["RRULE"] is not None:
            if "FREQ" in self.info["RRULE"]:
                freq = self.info["RRULE"]["FREQ"]
                if "UNTIL" in self.info["RRULE"]:
                    until = self.info["RRULE"]["UNTIL"].date()
                    if date > until:
                        return False
                    current = self.info["DTSTART"].date() + timedelta(weeks = 1)
                    if freq == "WEEKLY":
                        while current <= until:
                            if current == date:
                                return True
                            elif current > date:
                                return False
                            current += timedelta(weeks=1)
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

