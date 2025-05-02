import tkinter as tk
from tkinter import messagebox
import time

class dangerous_write:
    def __init__(self, root):
        self.root = root
        self.root.title("Dangerous Write")
        self.root.geometry("600x400")
        self.root.configure(bg="black")
        self.create_start_button()
        self.inactivity_timer = None
        self.start_time = None
    
    def create_start_button(self):
        center_frame = tk.Frame(self.root, bg="black")
        center_frame.pack(expand=True)

        self.instruction_label = tk.Label(center_frame, text="Don’t stop writing, or all progress will be lost.", bg="black", fg="white")
        self.instruction_label.pack(pady=20)
        self.instruction_label.config(font=("Arial", 14))

        self.start_button = tk.Button(center_frame, text="Start", command=self.start_typing, bg="green", fg="white")
        self.start_button.pack(pady=20)
        self.start_button.config(font=("Arial", 20))
        
    def start_typing(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.word_count_label = tk.Label(self.root, text="Words: 0", bg="black", fg="white")
        self.word_count_label.pack(pady=10)

        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg="black", fg="white", font=("Arial", 16), height=10)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.text_area.bind("<KeyPress>", self.reset_inactivity_timer)
        self.text_area.bind("<KeyRelease>", self.update_word_count)

        self.text_area.focus_set()

        self.start_time = time.time()
        self.check_time_limit()
        self.reset_inactivity_timer()
        
    def reset_inactivity_timer(self, event=None):
        if self.inactivity_timer:
            self.root.after_cancel(self.inactivity_timer)
        self.inactivity_timer = self.root.after(5000, self.clear_text_area)

    def clear_text_area(self):
        self.text_area.delete(1.0, tk.END)
        messagebox.showwarning("Inactivity", "You stopped typing! All progress is lost!")

    def update_word_count(self, event=None):
        text = self.text_area.get(1.0, tk.END).strip()
        word_count = len(text.split()) if text else 0
        self.word_count_label.config(text=f"Words: {word_count}")

    def check_time_limit(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 300:  # 5 minutes
            self.end_writing_session()  
        else:
            self.root.after(1000, self.check_time_limit)

    def end_writing_session(self):
        if self.inactivity_timer:
            self.root.after_cancel(self.inactivity_timer)
        self.text_area.config(state=tk.DISABLED)
        messagebox.showinfo("Session Ended", "You’ve done a great job!\n\nYour writing session has ended. You can now save your work.")
        self.create_end_buttons()

    def create_end_buttons(self):
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=10, side=tk.BOTTOM)

        copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=self.copy_text, bg="green", fg="white")
        copy_button.pack(side=tk.LEFT, pady=10)

        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_session, bg="blue", fg="white")
        restart_button.pack(side=tk.LEFT, pady=10)

    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.get(1.0, tk.END))
        self.root.update()
        messagebox.showinfo("Copied", "Your text has been copied to the clipboard!")

    def restart_session(self):
        self.root.destroy()
        main()

def main():
    root = tk.Tk()
    app = dangerous_write(root)
    root.mainloop()

if __name__ == "__main__":
    main()
        

    
        
        
    
