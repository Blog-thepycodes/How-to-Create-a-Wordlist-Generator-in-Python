import os
from itertools import product
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, filedialog, messagebox, Checkbutton, BooleanVar
from tkinter.ttk import Progressbar
import threading




def generate_wordlist(chars, min_len, max_len, output_file, max_words, all_variations, progress):
   total_combinations = sum(len(chars) ** length for length in range(min_len, max_len + 1))
   word_count = 0
   step = 100 / total_combinations if all_variations else 100 / max_words


   with open(output_file, 'w') as file:
       for length in range(min_len, max_len + 1):
           for combo in product(chars, repeat=length):
               if not all_variations and word_count >= max_words:
                   messagebox.showinfo("Info", f"Reached the limit of {max_words} words.")
                   return
               word = ''.join(combo)
               file.write(word + '\n')
               word_count += 1
               progress.step(step)
               progress.update_idletasks()


   messagebox.showinfo("Success", f"Wordlist successfully created and saved to {output_file}")




def browse_output_file():
   filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
   output_file.set(filename)




def generate_wordlist_gui():
   chars = characters.get()
   try:
       min_len = int(min_length.get())
       max_len = int(max_length.get())
       max_words = int(max_words_var.get())
   except ValueError:
       messagebox.showerror("Input Error", "Lengths and max words must be integers.")
       return


   if not chars:
       messagebox.showerror("Input Error", "Characters set cannot be empty.")
       return


   if min_len > max_len:
       messagebox.showerror("Input Error", "Minimum length cannot be bigger than the Maximum length.")
       return


   output_filepath = output_file.get()
   if not output_filepath:
       messagebox.showerror("Input Error", "Output file path cannot be empty.")
       return


   if os.path.exists(output_filepath):
       overwrite = messagebox.askyesno("File Exists", f"File {output_filepath} already exists. Overwrite?")
       if not overwrite:
           return


   progress_bar['value'] = 0
   threading.Thread(target=generate_wordlist, args=(
   chars, min_len, max_len, output_filepath, max_words, all_variations.get(), progress_bar)).start()




# Set up the main window
root = Tk()
root.title("Wordlist Generator - The Pycodes")


# Variables
characters = StringVar(value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
min_length = IntVar(value=4)
max_length = IntVar(value=6)
max_words_var = IntVar(value=1000)
output_file = StringVar()
all_variations = BooleanVar(value=False)


# GUI Layout
Label(root, text="Characters:").grid(row=0, column=0, sticky="e")
Entry(root, textvariable=characters, width=80).grid(row=0, column=1, padx=10, pady=5)


Label(root, text="Min Length:").grid(row=1, column=0, sticky="e")
Entry(root, textvariable=min_length, width=80).grid(row=1, column=1, padx=10, pady=5)


Label(root, text="Max Length:").grid(row=2, column=0, sticky="e")
Entry(root, textvariable=max_length, width=80).grid(row=2, column=1, padx=10, pady=5)


Label(root, text="Max Words:").grid(row=3, column=0, sticky="e")
Entry(root, textvariable=max_words_var, width=80).grid(row=3, column=1, padx=10, pady=5)


Label(root, text="Output File:").grid(row=4, column=0, sticky="e")
Entry(root, textvariable=output_file, width=80).grid(row=4, column=1, padx=10, pady=5)
Button(root, text="Browse", command=browse_output_file).grid(row=4, column=2, padx=10, pady=5)


Checkbutton(root, text="Generate All Variations", variable=all_variations).grid(row=5, column=0, columnspan=2, pady=5)


Button(root, text="Generate Wordlist", command=generate_wordlist_gui).grid(row=6, column=1, pady=10)


progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=7, column=0, columnspan=3, padx=10, pady=20)


# Run the main loop
root.mainloop()
