from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import customtkinter
import subprocess
import threading

def py_input():
    py_path = filedialog.askopenfilename(
        title='.py file',
        filetypes=[('python file', '*.py')]
    )

    if py_path:
        py_file.set(py_path)

def folder_output():
    folderOpen = filedialog.askdirectory(
        title='folder output', 
        initialdir=".", 
        mustexist=True 
    )
    
    if folderOpen:
        selectedFolder.set(folderOpen)

def ico_input():
    ico_path = filedialog.askopenfilename(
        title='.ico file',
        filetypes=[('icon file', '*.ico')]
    )

    if ico_path:
        ico_file.set(ico_path)
        icon_input.configure(state='normal')
        icon_input.delete(0, 'end')
        icon_input.insert(0, ico_path)
        icon_input.configure(state='disabled')

def compile():
    if not py_file.get():
        output_box.configure(state='normal')
        output_box.insert('end', 'Error: No .py file selected\n')
        output_box.configure(state='disabled')
        return

    flags = {
        '--standalone': standalone_var,
        '--onefile': onefile_var,
        '--module': module_var,
        '--python-debug': pydebug_var,
        '--full-compat': fullcompat_var,
        '--low-memory': lowmemory_var,
        '--pgo': pgo_var,
        '--windows-uac-admin': uac_var,
        '--windows-uac-uiaccess': uiaccess_var,
        '--mingw64': mingw64_var,
    }

    cmd = 'python -m nuitka'

    for flag, var in flags.items():
        if var.get() == 'on':
            cmd += f' {flag}'

    if ico_exe_var.get() == 'on' and ico_file.get():
        cmd += f' --windows-icon-from-ico={ico_file.get()}'

    if selectedFolder.get():
        cmd += f' --output-dir={selectedFolder.get()}'

    cmd += f' {py_file.get()}'

    output_box.configure(state='normal')
    output_box.delete('1.0', 'end')
    output_box.insert('end', f'Running: {cmd}\n\n')
    output_box.configure(state='disabled')

    def run():
        process = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in process.stdout:
            output_box.configure(state='normal')
            output_box.insert('end', line)
            output_box.see('end')
            output_box.configure(state='disabled')
            app.update_idletasks()

        output_box.configure(state='normal')
        output_box.insert('end', '\nDone!\n')
        output_box.configure(state='disabled')

    threading.Thread(target=run, daemon=True).start()

def areyousure():
    ready = CTkMessagebox(title='Ready?', message="You're about to compile which can take take long depending on how long your code is", icon="question", option_1="No", option_2="Yes")
    r = ready.get()

    if r == 'Yes':
        compile()
    else:
        pass

def toggle_standalone(*args):
    if standalone_var.get() == 'on':
        compile_button.configure(state='normal')

customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.geometry("600x750")
app.title('Nuitka GUI')
app.grid_columnconfigure(0, weight=1)

py_file = customtkinter.StringVar()
selectedFolder = customtkinter.StringVar()
ico_file = customtkinter.StringVar()

input_label = customtkinter.CTkLabel(app, text='Input .py Directory', justify='left')
input_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
script_location = customtkinter.CTkEntry(app, textvariable=py_file)
script_location.grid(row=2, column=0, padx=5, pady=1, sticky='nsew')
browse_button = customtkinter.CTkButton(app, text='Browse', command=py_input)
browse_button.grid(row=2, column=1, padx=5, pady=1, sticky='nsew')
output_label = customtkinter.CTkLabel(app, text='Output Folder Directory', justify='left')
output_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
output_location = customtkinter.CTkEntry(app, textvariable=selectedFolder)
output_location.grid(row=4, column=0, padx=5, pady=1, sticky='nsew')
browse_button = customtkinter.CTkButton(app, text='Browse', command=folder_output)
browse_button.grid(row=4, column=1, padx=5, pady=1, sticky='nsew')
icon_label = customtkinter.CTkLabel(app, text='Icon File (Optional)', justify='left')
icon_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
icon_input = customtkinter.CTkEntry(app, placeholder_text='.ico File Directory', state='disabled')
icon_input.grid(row=6, column=0, padx=5, pady=1, sticky='nsew')
icon_browse = customtkinter.CTkButton(app, text='Browse', command=ico_input)
icon_browse.grid(row=6, column=1, padx=5, pady=1, sticky='nsew')

commands_frame = customtkinter.CTkScrollableFrame(app, height=250) 
commands_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=25, sticky='nsew')

standalone_var = customtkinter.StringVar(value='off')
standalone_var.trace_add('write', toggle_standalone)
onefile_var = customtkinter.StringVar(value='off')
module_var = customtkinter.StringVar(value='off')
pydebug_var = customtkinter.StringVar(value='off')
fullcompat_var = customtkinter.StringVar(value='off')
lowmemory_var = customtkinter.StringVar(value='off')
pgo_var = customtkinter.StringVar(value='off')
ico_exe_var = customtkinter.StringVar(value='off')
uac_var = customtkinter.StringVar(value='off')
uiaccess_var = customtkinter.StringVar(value='off')
mingw64_var = customtkinter.StringVar(value='off')

build_label = customtkinter.CTkLabel(commands_frame, text='Build Mode')
standalone = customtkinter.CTkCheckBox(commands_frame, text='--standalone', onvalue='on', offvalue='off', variable=standalone_var)
onefile = customtkinter.CTkCheckBox(commands_frame, text='--onefile', onvalue='on', offvalue='off', variable=onefile_var)
module = customtkinter.CTkCheckBox(commands_frame, text='--module', onvalue='on', offvalue='off', variable=module_var)
pydebug = customtkinter.CTkCheckBox(commands_frame, text='--python-debug', onvalue='on', offvalue='off', variable=pydebug_var)
fullcompat = customtkinter.CTkCheckBox(commands_frame, text='--full-compat', onvalue='on', offvalue='off', variable=fullcompat_var)
lowmemory = customtkinter.CTkCheckBox(commands_frame, text='--low-memory', onvalue='on', offvalue='off', variable=lowmemory_var)
pgo = customtkinter.CTkCheckBox(commands_frame, text='--pgo', onvalue='on', offvalue='off', variable=pgo_var)

windows_label = customtkinter.CTkLabel(commands_frame, text='Windows')
ico_exe = customtkinter.CTkCheckBox(commands_frame, text='--windows-icon-from-ico=PATH', onvalue='on', offvalue='off', variable=ico_exe_var)
uac = customtkinter.CTkCheckBox(commands_frame, text='--windows-uac-admin', onvalue='on', offvalue='off', variable=uac_var)
uiaccess = customtkinter.CTkCheckBox(commands_frame, text='--windows-uac-uiaccess', onvalue='on', offvalue='off', variable=uiaccess_var)
mingw64 = customtkinter.CTkCheckBox(commands_frame, text='--mingw64', onvalue='on', offvalue='off', variable=mingw64_var)

build_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
standalone.grid(row=1, column=0, padx=5, pady=3, sticky='w')
onefile.grid(row=2, column=0, padx=5, pady=3, sticky='w')
module.grid(row=3, column=0, padx=5, pady=3, sticky='w')
pydebug.grid(row=4, column=0, padx=5, pady=3, sticky='w')
fullcompat.grid(row=5, column=0, padx=5, pady=3, sticky='w')
lowmemory.grid(row=7, column=0, padx=5, pady=3, sticky='w')
pgo.grid(row=8, column=0, padx=5, pady=3, sticky='w')
windows_label.grid(row=9, column=0, padx=5, pady=3, sticky='w')
ico_exe.grid(row=10, column=0, padx=5, pady=3, sticky='w')
uac.grid(row=11, column=0, padx=5, pady=3, sticky='w')
uiaccess.grid(row=12, column=0, padx=5, pady=3, sticky='w')
mingw64.grid(row=13, column=0, padx=5, pady=3, sticky='w')

compile_button = customtkinter.CTkButton(app, text='Compile', state='disabled',command=areyousure)
compile_button.grid(row=8, column=0, columnspan=2, pady=2)

output_box = customtkinter.CTkTextbox(app, height=150, state='disabled')
output_box.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
app.grid_rowconfigure(9, weight=1)

app.mainloop()