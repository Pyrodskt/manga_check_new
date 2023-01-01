from tkinter import Tk, Frame, Button, Entry, Label, ttk, END, Toplevel
from processing import Processing
from mangas import Mangas, Manga
import json
class Window:
    def __init__(self):
        # main window containing 2 frames
        # Mangas = list of manga obj initiated with the data in the json
        
        
        self.window = Tk()

        # Contain the table with the mangas and their values
        # also a button to save the values of the manga objs
        # as well as the button to lauch the process of update
        self.mangas = Mangas(self)
        self.left_frame = Leftframe(Frame(self.window), self)
        
        # Contain the inputs to update the data
        self.right_frame = Rightframe(Frame(self.window), self)

        
        # use pack for the frames for them to be "responsive"
        self.left_frame.frame.pack(side="left", expand=True, fill='both')
        self.right_frame.frame.pack(side='right', expand=True)


        

        self.window.mainloop()

class InputWindow:
    def __init__(self, parent):
        # Create the top level window
        self.parent = parent
        self.window = Toplevel(self.parent.window)

        # Create a frame to hold the widgets
        frame = Frame(self.window)
        frame.pack()

        # Create the entry widgets
        self.label_entry_name = Label(frame, text="Title")
        self.entry1 = Entry(frame)
        self.label_entry_url = Label(frame, text="URL")
        self.entry2 = Entry(frame)
        self.btnSave = Button(frame, text="Add", command=self.save)
        self.label_entry_name.pack(side='left')
        self.entry1.pack(side='left')
        self.label_entry_url.pack(side='left')
        self.entry2.pack(side='left')
        self.btnSave.pack(side='left')


    def save(self):
        title = self.entry1.get()
        url = self.entry2.get()
        print(title, url)
        self.parent.mangas.mangas.append(Manga( title, url, [], ""))
        self.window.destroy()
        self.parent.mangas.write_file()
        self.parent.left_frame.updateTable()
        
class Leftframe:
    def __init__(self, frame, window):
        # window contains the top window in order 
        # to access its properties and functions
        self.window = window
        self.frame = frame

        # treeview.table of the mangas in data.json  
        self.table = ttk.Treeview(self.frame, columns=('Title', 'Current', 'Last'), selectmode='browse')
        
        # Btn to launch the update process in mangas obj
        self.btnFrame = Frame(self.frame)
        self.btnUpdate = Button(self.btnFrame, text="Update", command=self.updateTable)
        self.btnSave = Button(self.btnFrame, text="Save", command=lambda : self.window.mangas.write_file())
        self.btnAdd = Button(self.btnFrame, text="Add", command=self.addManga)
        # column config for the treeview.table
        self.table.heading("Title", text='Title')
        self.table.heading("Current", text="Current")
        self.table.heading('Last', text="Last")
        self.table['show'] = "headings"

        # packing all buttons

        self.btnFrame.pack()
        self.btnUpdate.pack(side='left', padx=10, pady=10)
        self.btnSave.pack(side='left', padx=10, pady=10)
        self.btnAdd.pack(side='left', padx=10, pady=10)
        self.table.pack(fill='both', expand=True)
        # bind on click select item -> update input of Rightframe
        self.table.bind('<<TreeviewSelect>>', self.select_item)
        

    def addManga(self):
        InputWindow(self.window)



    def updateTable(self):
        # function to update data by scraping webpages
        if not self.window.mangas.updated:
            self.window.mangas.updateMangas()
            for i in self.window.mangas.mangas:
                # insert the updated values in the table
                self.table.insert('', END, values=(i.title, i.current, i.last))
        else:
            for item in self.table.get_children():
                self.table.delete(item)
            for i in self.window.mangas.mangas:
                self.table.insert('', END, values=(i.title, i.current, i.last))

    def select_item(self, e):
        # update inputs in rightframe when row in table selected
        selected = self.table.selection()
        print(selected)
        for i in self.window.mangas.mangas:
            if len(selected) != 0:
                if i.title == self.table.item(selected[0])['values'][0]:
                    # set the default value to be 
                    # the imported value from the json
                    self.window.right_frame.combobox['values'] = i.results
                    self.window.right_frame.label_title.config(text=i.title)
                    if i.current != '':
                        self.window.right_frame.combobox.set(i.current)
                    else:
                        self.window.right_frame.combobox.set(i.results[-1])
            
class Rightframe:
    def __init__(self, frame, window):
        self.frame = frame
        self.window = window
        self.label_title = Label(self.frame, text='Title')
        self.label_combo=  Label(self.frame, text='List')
        self.combobox = ttk.Combobox(self.frame, width=30)
        self.btnSave = Button(self.frame, text="Save", command=self.save)
        self.label_title.pack(fill='x', padx=10, pady=10)
        self.label_combo.pack(fill='x', padx=10, pady=10)
        self.combobox.pack(padx=10, pady=10)
        self.btnSave.pack(padx=10, pady=10)
    
    def save(self):
        for i in self.window.mangas.mangas:
            if i.title == self.label_title.cget("text"):
                i.current = self.combobox.get()
                print(i.current)
        for i in self.window.left_frame.table.selection():
            self.window.left_frame.table.selection_remove(i)
        self.window.left_frame.updateTable()
window = Window()

