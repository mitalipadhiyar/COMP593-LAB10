from tkinter import *
from tkinter import ttk
import os
import ctypes
import poke_api
import image_lib

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)  

# Create image cache directory
image_cache_dir = os.path.join(script_dir, 'images')
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

# Create the main window
root = Tk()
root.title("Pokemon illustration")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(500, 600)

# Set the window icon
icon_path = os.path.join(script_dir, 'jigglypuff')
app_id = 'COMP593.PokeImageViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
root.iconbitmap('jigglypuff.ico')

# Put a frame for gui 
frame = ttk.Frame(root, relief= 'ridge')
frame.grid(row=0, column=0, sticky=NSEW)
frame.columnconfigure(0, weight=100)
frame.rowconfigure(0, weight=100)

#put image into frame
img_path = os.path.join(script_dir, 'Pokemonn-Logo.png')
img_poke = PhotoImage(file=img_path)
lbl_image = ttk.Label(frame, image=img_poke)
lbl_image.grid(padx=10, pady=10)

#put the pull-down of pokemon names into the 

pokemon_name_list = sorted(poke_api.get_pokemon_names())
cbox_pokemon_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_pokemon_names.set("Select a Pokemon")
cbox_pokemon_names.grid(padx=10, pady=10)



def handle_pokemon_sel(event):

    sel_pokemon= cbox_pokemon_names.get()
    global img_path
    img_path = poke_api.download_pokemon_artwork(sel_pokemon,image_cache_dir)
    img_poke['file'] = img_path
    btn_set_desktop.state(['!disabled'])
    return

cbox_pokemon_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)


    
#put "set desktop" button into frame
def handle_set_desktop():
    image_lib.set_desktop_background_image(img_path)
    
    


btn_set_desktop = ttk.Button(frame, text='Set as Desktop image',command=handle_set_desktop)
btn_set_desktop.grid(padx=10, pady=10)
btn_set_desktop.state(['disabled'])




root.mainloop()