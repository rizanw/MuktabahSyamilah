from tkinter import *
from tkinter import ttk 
from tkinter.messagebox import showinfo
from ttkthemes import ThemedTk
from maktabah import *
import textwrap, threading, time

class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Menu",underline=0, menu=fileMenu)
        fileMenu.add_command(label="About", underline=1, command=self.about)
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)

    def about(self):
        showinfo("About", "Maktabah Syamila.\nPada Mesin pencarian Kitab Bahasa Arab ini terdiri dari 2 kategori yaitu ( أصول الفقه والقواعد الفقهية مرقم آليا : membahas mengenai Kaedah-kaedah Fiqh dan  الأنساب : membahas mengenai Nasab (garis keturunan orang Arab). Masing-masing kategori terdiri dari banyak kitab, yaitu pada Kategori أصول الفقه والقواعد الفقهية مرقم آليا terdapat 21 Kitab dan Kategori الأنساب terdapat 20 kitab.")

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.menubar = MenuBar(self)
        self.master['menu'] = self.menubar

        self.splash()
        self.splashFrame.after(4000, self.create_widgets)
        self.pack(fill=BOTH, expand=True) 
    
    def splash(self):
        self.splashFrame = ttk.Frame(self, style='new.TFrame')
        self.splashFrame.pack(fill=BOTH, expand=True)  
        self.splashFrame.place(relx=.5, rely=.5, anchor=CENTER)
        self.welcomeTitle = ttk.Label(self.splashFrame, justify=CENTER, anchor=CENTER)
        self.welcomeTitle['text'] = "Welcome to"
        self.welcomeTitle['font'] = ('Helvatica', 20)
        self.welcomeTitle.pack(fill=X, expand=1, anchor=S) 
        self.appTitle = ttk.Label(self.splashFrame, justify=CENTER, anchor=CENTER)
        self.appTitle['text'] = "Maktabah Syamila"
        self.appTitle['font'] = ('Helvatica', 24)
        self.appTitle.pack(fill=X, expand=1, anchor=CENTER)  
        self.appDesc = ttk.Label(self.splashFrame, justify=CENTER, anchor=CENTER)
        self.appDesc['text'] = "Mesin pencari Kitab Bahasa Arab"
        self.appDesc['font'] = ('Helvatica', 12)
        self.appDesc.pack(fill=X, expand=1) 

    def create_widgets(self):  
        self.splashFrame.destroy()

        self.searchFrame = ttk.Frame(self)
        self.searchFrame.pack(fill=X, padx=5)
        self.searchBox = ttk.Entry(self.searchFrame, justify=RIGHT)
        self.searchBox['width'] = 40
        self.searchBox['font'] = ('Helvatica', 14)
        self.searchBox.pack(side=LEFT, fill=X, expand=True)
        self.searchButton = ttk.Button(self.searchFrame)
        self.searchButton['width'] = 5  
        self.searchButton['text'] = 'search'
        self.searchButton['command'] = self.search
        self.searchButton.pack(side=RIGHT, fill=X, expand=True)
 
        self.listBox = ttk.Treeview(self, columns=(1,2), show="headings")
        self.listBox.pack(fill=BOTH, expand=1, anchor=CENTER, pady= 5, padx=5)
        self.listBox.heading(1, text="Kategori")
        self.listBox.heading(2, text="Kitab") 
        self.listBox.column(1, anchor=E)
        self.listBox.column(2, anchor=E)

        self.statusBar = ttk.Frame(self)
        self.statusBar.pack(fill=X)
        self.statusTitle = ttk.Label(self.statusBar)
        self.statusTitle['text'] = "Status: READY!"
        self.statusTitle['width'] = 10 
        self.statusTitle['relief'] = SUNKEN
        self.statusTitle['anchor'] = W
        self.statusTitle.pack(side=LEFT, fill=X, expand=True)
        self.status = ttk.Label(self.statusBar)
        self.status['text'] = ".. input arabic text to search box"
        self.status['width'] = 50 
        self.status['relief'] = SUNKEN
        self.status['anchor'] = E
        self.status.pack(side=RIGHT, fill=X, expand=True)

    def wrap(self, string, length=64):
        return '\n'.join(textwrap.wrap(string, length))

    def search(self):
        query = self.searchBox.get() 
        if ('\u0600' <= query <= '\u06FF' or
            '\u0750' <= query <= '\u077F' or
            '\u08A0' <= query <= '\u08FF' or
            '\uFB50' <= query <= '\uFDFF' or
            '\uFE70' <= query <= '\uFEFF' or
            '\U00010E60' <= query <= '\U00010E7F' or
            '\U0001EE00' <= query <= '\U0001EEFF'):
            self.searchButton["state"] = "disabled"
            self.statusTitle['text'] = "Status: PROCESSING!"
            self.status['text'] = "please wait .. DO NOT CLICK ANYTHING!"
            threading.Thread(target=self.process_data).start()
        else:
            self.arabic_popup()

    def process_data(self):   
        query = self.searchBox.get() 
        start_time = time.time()
        res = getResult(query)
        total_time = (time.time() - start_time)
        results = []
        for result in res:
            if result not in results:
                results.append({'namakitab': result["namakitab"], 'kategori': result["kategori"]})
        for result in results: 
            self.listBox.insert('', 'end', values=(self.wrap(result["kategori"]), self.wrap(result["namakitab"])))
        self.statusTitle['text'] = "Status: READY!"
        self.status['text'] = "Total: " + str(len(res)) +" found | Time: " + str(total_time)
        self.searchButton["state"] = "normal"

    def arabic_popup(self):
        showinfo("WARNING!!", "Please Input Arabic Only!")
    
      
root = ThemedTk(theme="plastik")
root.title("Maktabah Syamila")
root.geometry("640x480")  
menuBar = Menu(root)
app = Application(master=root)
app.mainloop()
