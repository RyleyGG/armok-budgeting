import tkinter as tk
import os
import json

class NavManager:
    root = None
    windowTitle = ''
    financialData = {}
    rightmostCol = 0

    def __init__(self):
        self.root = tk.Tk()
        self.root.bind('<Button-1>', self.focusElem)
        self.windowTitle = 'Armok Budgeting'
        self.root.title(self.windowTitle)
        self.displayHome()
        self.root.mainloop()

    # MAIN DISPLAY FUNCTIONS
    def displayHome(self):
        self.changeViews()
        label = tk.Label(self.root, text='Please select your option below')
        modFinancesBtn = tk.Button(self.root, text='Modify Financial Data', command=self.modFinances)
        viewCalendarBtn = tk.Button(self.root, text='View Calendar', command=self.viewCalendar)
        quitBtn = tk.Button(self.root, text='Quit', command=self.root.quit)

        label.pack()
        modFinancesBtn.pack()
        viewCalendarBtn.pack()
        quitBtn.pack()

    def viewCalendar(self):
        self.changeViews(True)
        label = tk.Label(self.root, text='Now viewing the calendar')
        label.pack()

    def modFinances(self):
        self.changeViews(True)
        self.populateFinances()


    # SPECIFIC HELPERS
    def populateFinances(self):
        label = tk.Label(self.root)
        label.grid(row = 1, column = 0, sticky = 'W', pady = 2)
        cwd = os.getcwd()
        if not os.path.exists(f'{cwd}/data') or len(os.listdir(f'{cwd}/data')) == 0:
            label.config(text = 'No financial data found')
            self.financialData = {
                'current_liquid': 0,
                'current_saved': 0,
                'income': 0,
                'income_frequency': 'biweekly',
                'expenses_flat': {},
                'expenses_pct': {}
            }

            if not os.path.exists(f'{cwd}/data'): 
                os.makedirs(f'{cwd}/data')
            json.dump(self.financialData, open(f'{cwd}/data/financial_data.json', 'w'))
        else:
            label.config(text = 'Pulling in previous financial data...')
            try:
                self.financialData = json.load(open(f'{cwd}/data/financial_data.json'))
                label.config(text = 'Financial data successfully loaded')
            except json.JSONDecodeError:
                label.config(text = 'Error loading financial data')
        
        rowIter = 3
        for k, v in self.financialData.items():
            if k in ['expenses_flat', 'expenses_pct']:
                continue

            self.createLabelFieldPair(k, rowIter, v, 'financial')
            rowIter += 1
        
        expFlatLabel = tk.Label(self.root, text = 'Flat Expenses')
        expFlatLabel.grid(row = rowIter, column = 0, sticky = 'W', pady = 2)
        rowIter += 1
        for k, v in self.financialData['expenses_flat'].items():
            self.createLabelFieldPair(k, rowIter, v, 'financial')
            rowIter += 1

        expPctLabel = tk.Label(self.root, text = 'Percent-based Expenses')
        expPctLabel.grid(row = rowIter, column = 0, sticky = 'W', pady = 2)
        rowIter += 1
        for k, v in self.financialData['expenses_pct'].items():
            self.createLabelFieldPair(k, rowIter, v, 'financial')
            rowIter += 1
        
        saveBtn = tk.Button(self.root, text='Save Changes')
        saveBtn.bind('<Button-1>', self.focusElem)
        saveBtn.bind('<ButtonRelease-1>', self.commitFinances)
        saveBtn.grid(row = rowIter + 1, column = self.rightmostCol, sticky = 'NE', pady = 2)

    def commitFinances(self, event):
        cwd = os.getcwd()
        json.dump(self.financialData, open(f'{cwd}/data/financial_data.json', 'w'))
    
    def updateFinancialDict(self, event):
        k = event.widget.tag
        v = event.widget.get()
        self.financialData[k] = v


    # GENERIC GUI HELPERS
    def focusElem(self, event):
        event.widget.focus_force()

    def createLabelFieldPair(self, labelText, rowIter, fieldText, callbackConfig):
            label = tk.Label(self.root, text = labelText)
            label.grid(row = rowIter, column = 0, sticky = 'W', pady = 2)
            
            # sv = tk.StringVar()
            field = tk.Entry(self.root)
            field.tag = labelText
            field.insert(tk.END, fieldText)
            if callbackConfig == 'financial':
                field.bind('<FocusOut>', self.updateFinancialDict)
            field.grid(row = rowIter, column = 1, sticky = 'E', pady = 2)

    def changeViews(self, homeOpt = False):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        if homeOpt:
            returnBtn = tk.Button(self.root, text='Return Home', command=self.displayHome)
            returnBtn.grid(row = 0, column = self.rightmostCol, sticky = 'NE', pady = 2)