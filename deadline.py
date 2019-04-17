#!/usr/bin/env python3


def main():
    start = datetime.now()
    if("http" in sys.argv[1]):
        data = requests.get(sys.argv[1]).text# url is http feed
    else:
        with open(sys.argv[1], 'r') as content_file:
            data = content_file.read()

    cal = iCal(data)
    print("time taken:(ms) ",(datetime.now() - start).total_seconds() * 1000)
    
    
    #MyManchester week 0 is 17th Sept 2018
    global today
    today = datetime.today()
    global currentWeekStart
    currentWeekStart = today - timedelta(days=today.weekday())
    global displayWeekStart
    displayWeekStart = currentWeekStart

    global h 
    global w 
    global xb
    global yb
    global td
    global th
    
    h = 60 # height of slot
    w = 150 # width of slot
    xb = 50 # x border
    yb = 20 # y border
    td = 5 # total/max days
    th = 10 # total hours

    days = ['Mon','Tue','Wed','Thur','Fri', '']
    
    
    root = Tk()
    canv = Canvas(root, width=td*w + xb, height=th*h + yb)
    canv.pack()

    canv.create_rectangle(xb,yb, td*w + xb, th*h + yb, outline="#000")
    for day in range (0,td + 1): # mon to fri
        canv.create_line(xb + day*w, 0, xb + day*w, yb + h*th)
        canv.create_text(xb + day*w + 0.5*w, yb*0.5, text=days[day])
    for hour in range(9,9+th + 1):
        canv.create_line(0, yb + (hour - 9)*h, td*w + xb, yb + (hour - 9)*h)
        canv.create_text(0.5*xb, yb + (hour - 9)*h + yb*0.5, text="{:02d}00".format(hour))

    #print(weekToShow)
    
    for day in range(0,5):
        for e in cal.onDay(displayWeekStart + timedelta(days=day)):
            draw(canv, e, day)



    root.mainloop()

main()
