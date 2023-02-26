import tkinter as tk
import os
import json

class NavManager:
    root = None
    windowTitle = ''
    financialData = {}
    flatExpenseInputRow = 0
    pctExpenseInputRow = 0

    def __init__(self):
        self.root = tk.Tk()
        self.root.bind('<Button-1>', self.focusElem)
        self.windowTitle = 'Armok Budgeting'
        self.root.title(self.windowTitle)
        self.displayHome()
        self.root.mainloop()

    # MAIN DISPLAY FUNCTIONS
    def displayHome(self):
        self.changeViews(False)
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
    # TODO: Validate finance data
    # TODO: Fix submission of nested values (expenses)
    # TODO: Fix formatting when performing delete or clear actions
    def populateFinances(self, readData = True):
        label = tk.Label(self.root)
        label.grid(row = 1, column = 0, sticky = '', pady = 2)
        cwd = os.getcwd()
        if readData:
            self.financialData = {}
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
        
        clearBtn = tk.Button(self.root, text='Clear all Expenses')
        clearBtn.bind('<Button-1>', self.focusElem)
        clearBtn.bind('<ButtonRelease-1>', self.clearExpenses)
        clearBtn.grid(row = rowIter, column = 0, sticky = 'W', pady = 2)
        rowIter += 1

        expFlatLabel = tk.Label(self.root, text = 'Flat Expenses')
        expFlatLabel.grid(row = rowIter, column = 0, sticky = 'W', pady = 2)
        flatAddBtn = tk.Button(self.root, text='Add')
        self.flatExpenseInputRow = rowIter
        flatAddBtn.bind('<Button-1>', self.focusElem)
        flatAddBtn.bind('<ButtonRelease-1>', lambda event: self.addItemToDict('expenses_flat', self.flatExpenseInputRow))
        flatAddBtn.grid(row = rowIter, column = 1, sticky = 'W', pady = 2)
        rowIter += 1
        for k, v in self.financialData['expenses_flat'].items():
            self.createExpenseRow(rowIter, k, v, 'expenses_flat')
            rowIter += 1

        expPctLabel = tk.Label(self.root, text = 'Percent-based Expenses')
        expPctLabel.grid(row = rowIter, column = 0, sticky = 'W', pady = 2)
        pctAddBtn = tk.Button(self.root, text='Add')
        self.pctExpenseInputRow = rowIter
        pctAddBtn.bind('<Button-1>', self.focusElem)
        pctAddBtn.bind('<ButtonRelease-1>', lambda event: self.addItemToDict('expenses_pct', self.pctExpenseInputRow))
        pctAddBtn.grid(row = rowIter, column = 1, sticky = 'W', pady = 2)
        rowIter += 1
        for k, v in self.financialData['expenses_pct'].items():
            self.createExpenseRow(rowIter, k, v, 'expenses_pct')
            rowIter += 1
        
        gridSize = self.root.grid_size()
        saveBtn = tk.Button(self.root, text='Save Changes')
        saveBtn.bind('<Button-1>', self.focusElem)
        saveBtn.bind('<ButtonRelease-1>', self.commitFinances)
        saveBtn.grid(row = rowIter + 1, column = gridSize[0], sticky = 'NE', pady = 2)

    def addItemToDict(self, dictName, addRow):
        if dictName == 'expenses_flat':
            self.pctExpenseInputRow += 1
        # Update dictionary only with newest value
        cwd = os.getcwd()
        key = 1
        while f'Name{key}' in self.financialData[dictName]:
            key += 1
        self.financialData[dictName][f'Name{key}'] = {'day': '', 'amount': ''}

        # Update GUI to show new element
        widgetsToMove = []
        for widgetName, widget in self.root.children.items():
            widgetInfo = widget.grid_info()
            if len(widgetInfo) == 0:
                continue
            if widgetInfo['row'] > addRow:
                widgetsToMove.append(widgetName)

        self.createExpenseRow(addRow + 1, f'Name{key}', {'day': '', 'amount': ''}, dictName)

        for widgetName, widget in self.root.children.items():
            widgetInfo = widget.grid_info()
            if widgetName in widgetsToMove:
                widget.grid_forget()
                widget.grid(row=widgetInfo['row'] + 1, column=widgetInfo['column'], sticky=widgetInfo['sticky'], pady=widgetInfo['pady'])

    def commitFinances(self, event):
        cwd = os.getcwd()
        json.dump(self.financialData, open(f'{cwd}/data/financial_data.json', 'w'))
    
    def updateFinancialDict(self, event):
        k = event.widget.tag
        v = event.widget.get()
        self.financialData[k] = v

    def updateNestedFinancialDict(self, event):
        pass

    def clearExpenses(self, event):
        self.financialData['expenses_flat'] = {}
        self.financialData['expenses_pct'] = {}
        self.changeViews(True)
        self.populateFinances(False)

    # GENERIC GUI HELPERS
    def focusElem(self, event):
        event.widget.focus_force()

    def createLabelFieldPair(self, labelText, rowIter, fieldText, callbackConfig):
            label = tk.Label(self.root, text = labelText)
            label.grid(row = rowIter, column = 0, sticky = 'W', pady = 2)
            
            field = tk.Entry(self.root)
            field.tag = labelText
            field.insert(tk.END, fieldText)
            if callbackConfig == 'financial':
                field.bind('<FocusOut>', self.updateFinancialDict)
            field.grid(row = rowIter, column = 1, sticky = 'E', pady = 2)

    def deletePlaceholder(self, event, text):
        if event.widget.get() != text:
            return
        event.widget.delete(0, 'end')
    
    def putPlaceholder(self, event, text):
        if len(event.widget.get()) != 0:
            return
        event.widget.delete(0, 'end')
        event.widget.insert(0, text)

    def deleteFinanceRow(self, event, curRow, inputDict):
        relevantWidgets = []

        for widget in self.root.winfo_children():
            widgetInfo = widget.grid_info()
            if widgetInfo['row'] == curRow:
                try:
                    widget.get()
                    relevantWidgets.append(widget.get())
                except AttributeError:
                    pass
        
        deleteKey = relevantWidgets[0]
        newDict = {}
        for key in self.financialData[inputDict]:
            if key != deleteKey:
                newDict[key] = self.financialData[inputDict][key]
        self.financialData[inputDict] = newDict
        self.changeViews(True)
        self.populateFinances(False)

    def handleExpenseUnfocus(self, event, placeholder):
        if len(event.widget.get()) != 0:
            self.updateNestedFinancialDict(event)
        else:
            event.widget.delete(0, 'end')
            event.widget.insert(0, placeholder)

    def createExpenseRow(self, rowIter, rowName, rowVals, inputDict):
        nameField = tk.Entry(self.root)
        dayField = tk.Entry(self.root)
        amtField = tk.Entry(self.root)
        deleteBtn = tk.Button(self.root, text='Delete')

        nameField.insert(0, rowName)
        dayField.insert(0, rowVals['day'] if len(rowVals['day']) != 0 else 'Day of the Month')
        amtField.insert(0, rowVals['amount'] if len(rowVals['amount']) != 0 else 'Amount')

        nameField.bind("<Button-1>", lambda event: self.deletePlaceholder(event, 'Name'))
        nameField.bind("<FocusOut>", lambda event: self.handleExpenseUnfocus(event, 'Name'))
        dayField.bind("<Button-1>", lambda event: self.deletePlaceholder(event, 'Day of the Month'))
        dayField.bind("<FocusOut>", lambda event: self.handleExpenseUnfocus(event, 'Day of the Month'))
        amtField.bind("<Button-1>", lambda event: self.deletePlaceholder(event, 'Amount'))
        amtField.bind("<FocusOut>", lambda event: self.handleExpenseUnfocus(event, 'Amount'))
        
        deleteBtn.bind('<Button-1>', self.focusElem)
        deleteBtn.bind('<ButtonRelease-1>', lambda event: self.deleteFinanceRow(event, rowIter, inputDict))

        nameField.grid(row = rowIter, column = 0, sticky = '', pady = 2)
        dayField.grid(row = rowIter, column = 1, sticky = '', pady = 2)
        amtField.grid(row = rowIter, column = 2, sticky = '', pady = 2)
        deleteBtn.grid(row = rowIter, column = 3, sticky = '', pady = 2)


    def changeViews(self, homeOpt = False):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        if homeOpt:
            gridSize = self.root.grid_size()
            returnBtn = tk.Button(self.root, text='Return Home', command=self.displayHome)
            returnBtn.grid(row = 0, column = gridSize[0], sticky = 'NE', pady = 2)