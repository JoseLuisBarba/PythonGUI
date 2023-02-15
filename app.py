from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk


class InputLabel(tk.Frame):
    '''A widget containing a label and input together'''

    def __init__(
            self, parent,
            label='',
            inputClass=tk.Entry,
            inputVar=None,
            inputArgs=None,
            labelArgs=None,
            **kwargs
        ):
        super().__init__(parent, **kwargs)
        inputArgs = inputArgs or {}
        labelArgs = labelArgs or {}
        self.variable = inputVar
        if inputClass in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            inputArgs['text'] = label
            inputArgs['variable'] = inputVar
        else:
            self.label = ttk.Label(self, text=label, **labelArgs)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            inputArgs['textvariable'] = inputVar
        self.input = inputClass(self, **inputArgs)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.W + tk.E), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self,):
        if self.variable:
            return self.variable.get()
        elif type(self.input) == tk.Text:
            return self.input.get('1.0', tk.END)
        else:
            return self.input.get()

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input).__name__.endswith('button'):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)


class DataRecordForm(tk.Frame):
    '''input form for  our widgets'''

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # a dict to keep track of input widgets
        self.input = {}
        

        # build the form
        # recordinfo section
        recordInfo = tk.LabelFrame(text='Record Information')

        # line 1
        self.input['Date'] = InputLabel(
            recordInfo,
            'Date',
            inputVar=tk.StringVar()
        )
        self.input['Date'].grid(row=0, column=0)
        self.input['Time'] = InputLabel(
            recordInfo,
            'Time',
            inputClass=ttk.Combobox,
            inputVar=tk.StringVar(),
            inputArgs={'values':['8:00', '12:00', '16:00', '20:00']}
        )
        self.input['Time'].grid(row=0,column=1)
        self.input['Technician'] = InputLabel(
            recordInfo,
            'Technician',
            inputVar= tk.StringVar()
        )
        self.input['Technician'].grid(row=0, column=2)

        #line 2
        self.input['Lab'] = InputLabel(
            recordInfo,
            'Lab',
            inputClass=ttk.Combobox,
            inputVar=tk.StringVar(),
            inputArgs={'values':['A','B','C','D','E']}
        )
        self.input['Lab'].grid(row=1, column=0)
        self.input['Plot'] = InputLabel(
            recordInfo, 'Plot',
            inputClass=ttk.Combobox,
            inputVar=tk.IntVar(),
            inputArgs={'values': list(range(1, 21))}
        )
        self.input['Plot'].grid(row=1, column=1)
        self.input['Seed sample'] = InputLabel(
            recordInfo, "Seed sample",
            inputVar=tk.StringVar()
        )
        self.input['Seed sample'].grid(row=1, column=2)
        recordInfo.grid(row=0, column=0, sticky=(tk.W + tk.E))

        # Environment Data
        environmentinfo = tk.LabelFrame(self, text="Environment Data")
        self.input['Humidity'] = InputLabel(
            environmentinfo, "Humidity (g/m³)",
            inputClass=tk.Spinbox,
            inputVar=tk.DoubleVar(),
            inputArgs={"from_": 0.5, "to": 52.0, "increment": .01}
        )
        self.input['Humidity'].grid(row=0, column=0)
        self.input['Light'] = InputLabel(
            environmentinfo, "Light (klx)",
            inputClass=tk.Spinbox,
            inputVar=tk.DoubleVar(),
            inputArgs={"from_": 0, "to": 100, "increment": .01}
        )
        self.input['Light'].grid(row=0, column=1)
        self.input['Temperature'] = InputLabel(
            environmentinfo, "Tenmperature (°C)",
            inputClass=tk.Spinbox,
            inputVar=tk.DoubleVar(),
            inputArgs={"from_": 4, "to": 40, "increment": .01}
        )
        self.input['Temperature'].grid(row=0, column=2)
        self.input['Equipment Fault'] = InputLabel(
            environmentinfo, "Equipment Fault",
            inputClass=ttk.Checkbutton,
            inputVar=tk.BooleanVar()
        )
        self.input['Equipment Fault'].grid(row=1, column=0, columnspan=3)
        environmentinfo.grid(row=1, column=0, sticky=(tk.W + tk.E))

        # Plant Data section
        plantinfo = tk.LabelFrame(self, text="Plant Data")

        self.input['Plants'] = InputLabel(
            plantinfo, "Plants",
            inputClass=tk.Spinbox,
            inputVar=tk.IntVar(),
            inputArgs={"from_": 0, "to": 20}
        )
        self.input['Plants'].grid(row=0, column=0)
        self.input['Blossoms'] = InputLabel(
            plantinfo, "Blossoms",
            inputClass=tk.Spinbox,
            inputVar=tk.IntVar(),
            inputArgs={"from_": 0, "to": 1000}
        )
        self.input['Blossoms'].grid(row=0, column=1)
        self.input['Fruit'] = InputLabel(
            plantinfo, "Fruit",
            inputClass=tk.Spinbox,
            inputVar=tk.IntVar(),
            inputArgs={"from_": 0, "to": 1000}
        )
        self.input['Fruit'].grid(row=0, column=2)

        # Height data
        self.input['Min Height'] = InputLabel(
            plantinfo, "Min Height (cm)",
            inputClass=tk.Spinbox,
            inputVar=tk.DoubleVar(),
            inputArgs={"from_": 0, "to": 1000, "increment": .01}
        )
        self.input['Min Height'].grid(row=1, column=0)
        self.input['Max Height'] = InputLabel(
            plantinfo, "Max Height (cm)",
            inputClass=tk.Spinbox,
            inputVar=tk.DoubleVar(),
            inputArgs={"from_": 0, "to": 1000, "increment": .01}
        )
        self.input['Max Height'].grid(row=1, column=1)
        self.input['Median Height'] = InputLabel(
            plantinfo, "Median Height (cm)",
            inputClass=tk.Spinbox,
            inputVar=tk.DoubleVar(),
            inputArgs={"from_": 0, "to": 1000, "increment": .01}
        )
        self.input['Median Height'].grid(row=1, column=2)

        plantinfo.grid(row=2, column=0, sticky=(tk.W + tk.E))

        # Notes section
        self.input['Notes'] = InputLabel(
            self, "Notes",
            inputClass=tk.Text,
            inputArgs={"width": 75, "height": 10}
        )
        self.input['Notes'].grid(sticky=tk.W, row=3, column=0)
        # default the form
        self.reset()

    def get(self,):
        '''Retrieve data from form as a dict.'''
        # We need to retrieve the data from Tkinter variables
        # and place it in regular Python objects
        data = {}
        for key, widget in self.input.items():
            data[key] = widget.get()
        return data
    def reset(self,):
        '''Reste the form entries'''
        #clear all values
        for widget in self.input.values():
            widget.set('')


class Application(tk.Tk):
    '''application root windows'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('ABQ Data Entry Application')
        self.resizable(width=False, height=False)
        ttk.Label(self,text='ABQ Data Entry Application',font=("TkDefaultFont", 16)).grid(row=0)

        self.recordForm = DataRecordForm(self)
        self.recordForm.grid(row=1, padx=10)


        self.saveButton = ttk.Button(self, text='Save', command=self.onSave)
        self.saveButton.grid(sticky=tk.E, row=2, padx=10)
        # status bar
        self.status = tk.StringVar()
        self.statusbar = tk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)
        self.recordsSave = 0
    def onSave(self,):
        """Handles save button clicks"""
        # For now, we save to a hardcoded filename with a datestring.
        # If it doesnt' exist, create it,
        # otherwise just append to the existing file
        dateString = datetime.today().strftime('%y-%m-%d')
        fileName = f'abq_data_record_{dateString}.csv'
        newFile = not os.path.exists(fileName)

        data = self.recordForm.get()

        with open(fileName,'a') as fh:
            csvWriter = csv.DictWriter(fh,fieldnames=data.keys())
            if newFile:
                csvWriter.writeheader()
            csvWriter.writerow(data)

        self.recordsSave +=1
        self.status.set(
            f'{self.recordsSave} records saved this session'
        )
        self.recordForm.reset()
        



if __name__ == '__main__':
    app = Application()
    app.mainloop()
