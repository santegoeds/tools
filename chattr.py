import os
import Tkinter as tk
import ttk
import win32api
import win32con

from os import path
from tkFileDialog import askdirectory


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.title("Chattr - voor Erwin")        
        self._tree = ttk.Treeview(self)
        self._tree.grid(column=0, row=0, sticky=tk.NSEW)
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, 
                                  command=self._tree.yview)
        vscrollbar.grid(column=1, row=0, sticky=tk.NS)
        self._tree.config(yscrollcommand=vscrollbar.set)
        self._button = ttk.Button(self, command=self.populate, 
                                  text="Selecteer een Folder")
        self._button.grid(column=2, row=0, sticky=tk.N)
        self._button.grid_configure(padx=5, pady=5)

    def populate(self):
        dirname = askdirectory(title ="Selecteer een Folder")
        if not dirname:
                return
        self.config(cursor="clock")
        self.update_idletasks()
        self._tree.insert('', 'end', dirname, text=dirname)
        for dpath, _, fnames in os.walk(dirname, topdown=True):
            for fname in fnames:
                fname = path.join(dpath, fname)
                if not self.has_normal_attributes(fname):
                    self.insert(fname)
        self.config(cursor="")
        self._button.configure(text="Normaliseer Bestanden",
                               command=self.normalise)

    def insert(self, fname):
        stack = []
        while not self._tree.exists(fname):
            stack.insert(0, fname)
            fname = path.dirname(fname)
        for fname in stack:
            self._tree.insert(path.dirname(fname), 'end', fname,
                              text=path.basename(fname))

    @staticmethod
    def has_normal_attributes(fname):
        return win32api.GetFileAttributes(fname) != win32con.FILE_ATTRIBUTE_NORMAL

    @staticmethod
    def normalise_attributes(fname):
        win32api.SetFileAttributes(fname, win32con.FILE_ATTRIBUTE_NORMAL)

    def normalise(self, fpath=None):
        if fpath is None:
            fpath = ''
        children = self._tree.get_children(fpath)
        if not children and path.isfile(fpath):
            self.normalise_attributes(fpath)
        else:
            for child in children:
                self.normalise(child)


if __name__ == '__main__':
    app = App()
    app.mainloop()    