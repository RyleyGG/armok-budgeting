from tkinter import *

class NavManager:
    root = None
    windowTitle = ""

    def __init__(self):
        self.root = Tk()
        self.windowTitle = "Armok Budgeting"
        self.root.title(self.windowTitle)
        self.displayHome()
        self.root.mainloop()


    # MAIN DISPLAY FUNCTIONS
    def displayHome(self):
        self.changeViews()
        label = Label(self.root, text="Please select your option below")
        modFinancesBtn = Button(self.root, text="Modify Financial Data", command=self.modFinances)
        viewCalendarBtn = Button(self.root, text="View Calendar", command=self.viewCalendar)
        quitBtn = Button(self.root, text="Quit", command=self.root.quit)

        label.pack()
        modFinancesBtn.pack()
        viewCalendarBtn.pack()
        quitBtn.pack()

    def viewCalendar(self):
        self.changeViews(True)
        label = Label(self.root, text="Now viewing the calendar")
        label.pack()

    def modFinances(self):
        self.changeViews(True)
        label = Label(self.root, text="Now modifying finances")
        label.pack()


    # GUI HELPERS
    def changeViews(self, homeOpt = False):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        if homeOpt:
            returnBtn = Button(self.root, text="Return Home", command=self.displayHome)
            returnBtn.pack()


    # BACKEND HELPERS