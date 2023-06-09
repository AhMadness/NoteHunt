import tkinter as tk
from tkinter import scrolledtext, filedialog

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
        self.notes_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10, font=("Montserrat", 12), borderwidth=0, undo=True, autoseparators=True, maxundo=1)
        self.notes_text.pack(expand=True, fill='both', padx=(10, 0), pady=(5, 5))
        
        # Set border color of notepad widget
        self.notes_text.configure(background='#1E1E1E')
        # set the foreground color (i.e., text colorr) of the notes_text widget to green
        self.notes_text.config(fg="#E1E1E1")
    
        # define "highlight" tag for highlighting search term
        self.notes_text.tag_configure("highlight", background="#19afaf")
        self.notes_text.tag_configure("highlight_current", background="#0f6969")
        
        # cursor color
        self.notes_text.config(insertbackground="#E1E1E1")
        
        # set highlight colors
        self.notes_text.configure(selectbackground="#19afaf", selectforeground="#E1E1E1")
        
        # set the default file path to "notes.txt"
        self.file_path = "notes.txt"
        
        # load any previously saved notes
        self.load_notes()
        
        # bind modified event to auto-save notes
        self.notes_text.bind("<KeyRelease>", self.auto_save_notes)
        
        # open
        open_button = tk.Button(toolbar_frame, text="Open", font=('Montserrat', 12), command=self.open_file)
        open_button.grid(row=0, column=0, padx=(0, 300), pady=(0, 0))
        
        # create search bar
        self.search_var = tk.StringVar()
        self.search_var.set("Search...")
        self.search_var.trace("w", self.search_notes)
        self.search_entry = tk.Entry(toolbar_frame, textvariable=self.search_var, width=16, font=('Montserrat', 12), fg='grey')
        self.search_entry.grid(row=0, column=0, padx=(200, 20), pady=10)
        
        # search function to focus in and out of search bar
        self.search_entry.bind("<FocusIn>", self.clear_searchbox)
        self.search_entry.bind("<FocusOut>", self.on_search_entry_focus_out)
        
        # create another search bar
        self.search_var2 = tk.StringVar()
        self.search_var2.set("Highlight")
        self.search_var2.trace("w", self.search_notes)
        self.search_entry2 = tk.Entry(toolbar_frame, textvariable=self.search_var2, width=16, font=('Montserrat', 12), fg='grey')
        self.search_entry2.grid(row=0, column=1, padx=0, pady=10)
  
        # search function to focus in and out of search bar 2
        self.search_entry2.bind("<FocusIn>", self.clear_searchbox2)
        self.search_entry2.bind("<FocusOut>", self.on_search_entry_focus_out2)
        self.search_entry2.bind("<Return>", self.next_occurrence)
        self.search_entry2.bind("<Down>", self.next_occurrence)
        self.search_entry2.bind("<Up>", self.previous_occurrence)
        
        # jump button
        self.occurrences = []
        # tk.Button(toolbar_frame, text="v", command=self.find_next_occurrence).grid(row=0, column=2, padx=0, pady=(6, 4))
        self.jump_button = tk.Button(toolbar_frame, text="0 | 0", state="disabled", command=self.find_next_occurrence)
        
        
        self.jump_button.place_forget()
        # function to check if search_var2 is populated
        def check_search_var2(*args):
            if self.jump_button['text'] != "0 | 0":
                self.jump_button.grid(row=0, column=2, padx=0, pady=(6, 4))  # change the coordinates to where you want to show the button
            else:
                self.jump_button.grid_forget()  # hide the button      
        self.search_var2.trace("w", check_search_var2)
        
        def check_search_var2_width(*args):
            if self.search_var2.get() == "Highlight":
                self.search_entry2.config(width=16)
            else:
                self.search_entry2.config(width=13)
        self.search_var2.trace("w", check_search_var2_width)
        
        # bind key event to check search input before allowing user to type in text area
        self.notes_text.bind("<Key>", self.check_search_input)
        
        # enable copying in filtered mode
        self.notes_text.bind("<Control-c>", lambda e: self.notes_text.event_generate("<<Copy>>"))

# FUNCTIONS

    def open_file(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path = file_path  # update the file_path variable
            with open(file_path, "r", encoding='utf-8') as f:
                notes = f.read()
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert(tk.END, notes)


    def load_notes(self, search_term=None):
        try:
            with open(self.file_path, "r", encoding='latin-1') as f:
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
        notes = self.notes_text.get("1.0", tk.END)
        with open("notes.txt", "w", encoding='utf-8') as f:
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
        search_term2 = self.search_var2.get()
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
        elif search_term2 and search_term2 != "Highlight":
            # remove previous search term highlighting
            self.notes_text.tag_remove("highlight", "1.0", tk.END)
            # clear the occurrences list
            self.occurrences.clear()
            # search for occurrences and highlight them
            start = "1.0"
            while True:
                start = self.notes_text.search(search_term2, start, tk.END, nocase=1)
                if not start:
                    break
                end = f"{start}+{len(search_term2)}c"
                self.notes_text.tag_add("highlight", start, end)
                self.occurrences.append(start)
                start = end
            # update the jump button text to show number of occurrences and current index
            if self.occurrences:
                self.current_occurrence_index = 0
                self.jump_button.configure(text=f"1 | {len(self.occurrences)}")
                self.find_next_occurrence()
            else:
                self.current_occurrence_index = None
                self.jump_button.configure(text="0 | 0")
        else:
            self.load_notes()
            # remove search term highlighting when search box is empty
            self.notes_text.tag_remove("highlight", "1.0", tk.END)
            self.current_occurrence_index = None
            self.jump_button.configure(text="0 | 0")

    def find_next_occurrence(self):
        if not self.occurrences:
            return

        # find index of next occurrence after current cursor position
        self.current_occurrence_index = (self.current_occurrence_index) % len(self.occurrences)

        # move cursor to start of next occurrence
        start = self.occurrences[self.current_occurrence_index]
        self.notes_text.tag_remove("sel", "1.0", tk.END)
        self.notes_text.tag_remove("highlight_current", "1.0", tk.END)
        self.notes_text.tag_add("highlight_current", start, f"{start}+{len(self.search_var2.get())}c")
        self.notes_text.tag_add("sel", start, f"{start}+{len(self.search_var2.get())}c")
        self.notes_text.mark_set(tk.INSERT, start)
        self.notes_text.see(tk.INSERT)

        # update the jump button text to show current index
        self.jump_button.configure(text=f"{self.current_occurrence_index + 1} | {len(self.occurrences)}")
        
    def activate_jump_button(self, event):
        # call the find_next_occurrence method when the Return key is pressed
        self.next_occurrence()
        
    def next_occurrence(self, event):
        if self.occurrences:
            self.current_occurrence_index = (self.current_occurrence_index + 1) % len(self.occurrences)
            self.find_next_occurrence()

    def previous_occurrence(self, event):
        if self.occurrences:
            self.current_occurrence_index = (self.current_occurrence_index - 1) % len(self.occurrences)
            start = self.occurrences[self.current_occurrence_index]
            self.notes_text.tag_remove("sel", "1.0", tk.END)
            self.notes_text.tag_remove("highlight_current", "1.0", tk.END)
            self.notes_text.tag_add("highlight_current", start, f"{start}+{len(self.search_var2.get())}c")
            self.notes_text.tag_add("sel", start, f"{start}+{len(self.search_var2.get())}c")
            self.notes_text.mark_set(tk.INSERT, start)
            self.notes_text.see(tk.INSERT)
            self.jump_button.configure(text=f"{self.current_occurrence_index + 1} | {len(self.occurrences)}")


    def clear_searchbox(self, event):
        if self.search_var.get() == "Search...":
            self.search_var.set("")
            
    def on_search_entry_focus_out(self, event):
        if not self.search_var.get():
            self.search_var.set("Search...")
            
    def clear_searchbox2(self, event):
        if self.search_var2.get() == "Highlight":
            self.search_var2.set("")
            
    def on_search_entry_focus_out2(self, event):
        if not self.search_var2.get():
            self.search_var2.set("Highlight")
        
    def check_search_input(self, event):
        search_term = self.search_var.get()
        if search_term and search_term != "Search...":
            self.notes_text.config(insertbackground="#1E1E1E")
            return "break"
        else:
            self.notes_text.config(insertbackground="#E1E1E1")

root = tk.Tk()
app = NoteApp(root)
root.mainloop()
