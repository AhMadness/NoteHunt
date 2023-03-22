import tkinter as tk
from tkinter import scrolledtext

class NoteApp:
    def __init__(self, master):
        self.master = master
        master.title("NoteHunt")
        
        # set size of the window
        master.geometry("600x600")
        master.config(bg='#1e1e1e')

        # create a frame for the toolbar
        toolbar_frame = tk.Frame(master, bg="#0F0F0F")
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # create text area for notes
        self.notes_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10, font=("Montserrat", 12), borderwidth=0)
        self.notes_text.pack(expand=True, fill='both', padx=(10, 0), pady=(5, 5))
        
        # Set border color of notepad widget
        self.notes_text.configure(background='#1E1E1E')
        
        # set the foreground color (i.e., text colorr) of the notes_text widget to green
        self.notes_text.config(fg="#E1E1E1")
    
        # define "highlight" tag for highlighting search term
        self.notes_text.tag_configure("highlight", background="#19afaf")
        
        # cursor color
        self.notes_text.config(insertbackground="#E1E1E1")
        
        # set highlight colors
        self.notes_text.configure(selectbackground="#19afaf", selectforeground="#E1E1E1")
        
        # load any previously saved notes
        self.load_notes()
        
        # bind modified event to auto-save notes
        self.notes_text.bind("<KeyRelease>", self.auto_save_notes)
        
        # create search bar and button
        self.search_var = tk.StringVar()
        self.search_var.set("Search...")
        self.search_var.trace("w", self.search_notes)
        self.search_entry = tk.Entry(toolbar_frame, textvariable=self.search_var, width=16, font=('Montserrat', 12), fg='grey')
        self.search_entry.pack(side=tk.TOP, padx=10, pady=10)


        self.search_entry.bind("<FocusIn>", self.clear_searchbox)
        self.search_entry.bind("<FocusOut>", self.on_search_entry_focus_out)
        
        # bind key event to check search input before allowing user to type in text area
        self.notes_text.bind("<Key>", self.check_search_input)
        
        self.notes_text.bind("<Control-c>", lambda e: self.notes_text.event_generate("<<Copy>>"))
        
        self.notes_text.bind("<Control-z>", self.undo)




# FUNCTIONS

    def load_notes(self, search_term=None):
        try:
            with open("notes.txt", "r") as f:
                notes = f.read()
                if search_term:
                    filtered_notes = ""
                    for line in notes.splitlines():
                        if search_term.lower() in line.lower():
                            filtered_notes += line + "\n\n"
                    self.notes_text.delete("1.0", tk.END)
                    self.notes_text.insert(tk.END, filtered_notes)
                else:
                    self.notes_text.delete("1.0", tk.END)
                    self.notes_text.insert(tk.END, notes)
        except FileNotFoundError:
            pass
    
    def save_notes(self):
        with open("notes.txt", "w") as f:
            notes = self.notes_text.get("1.0", tk.END)
            f.write(notes)
            
    
    # def auto_save_notes(self, event=None):
    #     # if self.search_var.get() != "Search...":
    #     #     return
    #     self.save_notes()
        
    def auto_save_notes(self, event=None):
        search_term = self.search_var.get()
        if not search_term or search_term == "Search...":
            self.save_notes()
        
    def search_notes(self, *args):
        search_term = self.search_var.get()
        if search_term and search_term != "Search...":
            self.load_notes(search_term.lower())
            # remove previous search term highlighting
            self.notes_text.tag_remove("highlight", "1.0", tk.END)
            # highlight current search term
            start = "1.0"
            while True:
                start = self.notes_text.search(search_term, start, tk.END, nocase=1)
                if not start:
                    break
                end = f"{start}+{len(search_term)}c"
                self.notes_text.tag_add("highlight", start, end)
                start = end
        else:
            self.load_notes()
            # remove search term highlighting when search box is empty
            self.notes_text.tag_remove("highlight", "1.0", tk.END)
            
    def clear_searchbox(self, event):
        if self.search_var.get() == "Search...":
            self.search_var.set("")

            
    def on_search_entry_focus_out(self, event):
        if not self.search_var.get():
            self.search_var.set("Search...")

        
    def check_search_input(self, event):
        search_term = self.search_var.get()
        if search_term and search_term != "Search...":
            self.notes_text.config(insertbackground="#1E1E1E")
            return "break"
        else:
            self.notes_text.config(insertbackground="#E1E1E1")
            
            
    def undo(self, event=None):
        if self.search_var.get() != "Search...":
            self.notes_text.edit_undo()
 

root = tk.Tk()
app = NoteApp(root)
root.mainloop()
