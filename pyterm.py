#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk,messagebox, colorchooser
from math import floor, ceil
import os,subprocess,re,io,sys
import logging
from contextlib import redirect_stdout
from utils import TextBody 
import utils.getutils as getutils

logging.basicConfig(filename=f'{sys.argv[0].rstrip(".py")}.log', filemode='w', format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%d/%m/%y %H:%M:%S")
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

root = tk.Tk()
root.title('Python Terminal')
root.geometry('700x550')

title = tk.Label(root,text="Python GUI Terminal",font=('Verdana',22,"bold"),fg='#0493e5')
title.place(relx=0.5, rely=0.3, anchor='center')
subtitle = tk.Label(root,text="Let's get started!!",font=('Verdana',18,"bold"))
subtitle.place(relx=0.5,rely=0.5,anchor='center')

info=tk.Label(root,text="Press Ctrl+Shift+t",font=('Consolas',16,"bold"),fg='grey')
info.place(relx=0.5,rely=0.6,anchor='center')
backgroundColor = root.config()['background'][-1]

#defining notebook widget with traversal option
tabs = ttk.Notebook(root)
tabs.enable_traversal()

class TextShell(TextBody):
	def __init__(self,root,master,textWidget):
		TextBody.__init__(self,root,master,textWidget)
		self.intrcolor='#00bfff'
		self.PS = False
		self.interactiveprompt=f"{os.getcwd()}:~$ "
		self.show_prompt(self.interactiveprompt)

	#shell build cmds
	def gui_cmd(self,cmd):
		if cmd=='gui-cmd':
			gui_cmd={'clear':'clear the screen','intr':'change color for interactive prompt',\
		'themedark':'dark mode for shell','themelight':'light theme for shell','history':'display command history',\
		'gui-cmd':'display shell options','listdir':'list files and folders','read':'read files','write':'write content to files',\
		'rot':'executes rot ciphers','base64':'base64 text encoders','sysinfo':'display base system info',\
		'python/py':'invoke python shell','\\c':'command won\'t executed when include \\c at end'}
			for key,value in sorted(gui_cmd.items()):
				self.insert_text(f'{key}:\t\t{value}')
			self.insert_text()
		elif cmd=="history -c":
			self.cmdList.clear()
			self.insert_text('History Cleared (\'-\')')
		else:
			history = '\n'.join(self.cmdList)
			self.insert_text(history)

	#defining write feature with change in attributes
	def writeFile(self,file):
		self.write=True;self.file=file
		print("file: ",file)
		self.insert_text(f'Writing to the file, "{self.file}". Type "$" to exit.')

	#defining write feature
	def writeValue(self):
		try:
			if self.cmd=="$":
				self.write=False
				self.interactiveprompt=f"{os.getcwd()}:~$ "
				self.insert_text('Done')
			else:
				with open(self.file,'a') as f:
					f.write(self.cmd+'\n')
			#print('y',self.cmd)
		except Exception as e:
			logger.error('writting file:', exc_info=True)
			self.write=False;self.interactiveprompt=f"{os.getcwd()}:~$ "
			self.insert_text('Error in writing to file')

	#execute the commands
	def do(self,cmd):
		command = cmd.strip().split()
		#print(command,self.write)
		
		if not cmd or not command:
			return
		
		elif self.write:
			self.writeValue();return
		
		elif cmd in ("gui-cmd","history",'history -c'):
			self.gui_cmd(cmd)
		
		elif cmd == "clear":
			self.text.delete('1.0',tk.END)
		
		elif bool(cmd.find('\\c')>=0):
			return
		
		elif command[0].lower() == 'ps' and len(command)>1:
			self.PS=True
			if command[1] == 'pwd':
				self.PS=False
				self.interactiveprompt = f"{os.getcwd()}:~$ "
			else:
				self.interactiveprompt = ' '.join(command[1:])

		elif command[0] in ('python','py','py3','python3'):
			addPython();return
		
		elif command[0]=='write':
			if len(command)>1:
				self.writeFile(command[1])
			else:
				self.insert_text('format: write <file-name>')
				
		elif command[0]=='read':
			if len(command)>1:
				read=getutils.readFile(command[1])
				self.insert_text(f'>> Reading file "{command[1]}"\n\n'+read)
			else:
				self.insert_text('format: read <file-name>')
		
		elif command[0] == "themedark":
			self.text.config(bg="grey14",fg="white",insertbackground="white")
			self.intrcolor="#00bfff"
		
		elif command[0] == "themelight":
			self.text.config(bg="white",fg="black",insertbackground="black")
			self.intrcolor="black"
		
		elif command[0] == "intr":
			if command[0] and len(command)<=1:
				self.insert_text("Help: intr [Option]\nInteractive color option: specify white/blue/green/red/black")
			elif len(command)>1:
				if command[1] == "blue":
					self.intrcolor="#00bfff"
				elif command[1]== "red":
					self.intrcolor="red"
				elif command[1]== "green":
					self.intrcolor="#40DA27"
				elif command[1]== "black":
					self.intrcolor="black"
				elif command[1]== "white":
					self.intrcolor="white"
				else:
					self.insert_text("Help: intr [Option]\nInteractive color option: specify white/blue/green/red/black")				
		else:
			x=getutils.getoutput(cmd)
			if not self.PS:
				self.interactiveprompt=f"{os.getcwd()}:~$ "
			self.insert_text(x)

#defining class with required functions for python interpreter
class Python(TextBody):
	def __init__(self,root,master,textWidget):
		TextBody.__init__(self,root,master,textWidget)
		self.interactiveprompt='>>> '
		self.fg='#ffffff';self.shellcolor='white'
		self.show_prompt()
		
	def do(self, cmd):
		f = io.StringIO()
		with redirect_stdout(f):
			try:
				exec(cmd, globals())
			except Exception as e:
				logger.exception('Exception at interpreter:')
				#print(e)
		self.insert_text(f.getvalue(), end='')

#initializing list to work with multiple tabs and text widgets
tabs_ = []
text_widget_list = []

#defining add tab func
def addTab(*args):
	"""Add new tab"""
	tab=ttk.Frame(tabs)
	tabs.add(tab,text=f" {user} - Shell ")
	tabs.pack(expand=1,fill='both')
	text_widget = tk.Text(tab,tabs=4)
	text_widget.pack(fill=tk.BOTH,expand=1,side=tk.LEFT)
	Shell=TextShell(root,tab,text_widget)#,f"{os.getcwd()}:~$ ")
	text_widget_list.append(text_widget)
	tabs_.append(Shell)

#defining close tab func
def closeTab(*args):
	"""Close current tab in the notebook"""
	try:
		currenttab_index = tabs.index(tabs.select())
		totalTabs = tabs.tabs()
		if len(totalTabs) == 1:
			root.destroy()
			sys.exit(0)
		else:
			tabs_.pop(currenttab_index)
			text_widget_list.pop(currenttab_index)
			tabs.forget(currenttab_index)
	except Exception as e:
		pass

#defining right click menu func
def rightclickMenu(event):
	try: edit_menu.tk_popup(event.x_root,event.y_root)
	except Exception as e: logger.exception('Right Click Exception')

#defining keys
def keys(event):
	"""Initializing hot keys"""
	if event.keysym=="Escape":
		root.destroy()

#defining cut, copy and paste
def cutcopypaste(work):
	"""Manipulate cut, cop and paste"""
	tab_index = tabs.index(tabs.select())
	present_tab = text_widget_list[tab_index]
	present_tab.event_generate(work)

#defining clear, zoom in & out & reset
def basic_func(work):
	"""Manipulate clear, zoom in, zoom out and zoom reset"""
	tab_index = tabs.index(tabs.select())
	present_tab = tabs_[tab_index]
	if work=='clear':
		present_tab.clearText()
	elif work=='zoom-in':
		present_tab.zoom_in()
	elif work=='zoom-out':
		present_tab.zoom_out()
	elif work=='zoom-reset':
		present_tab.zoom_reset()

#defining func, change color attributres
def colorch(yesno):
	if yesno=='y':
		tab_index = tabs.index(tabs.select())
		present_tab = tabs_[tab_index]
		present_tab.colorpreference()
	else:
		colorchooser.askcolor(title='Choose Color')

#defining python interpreter func
def addPython():
	"""Add python interpreter to notebook"""
	tab=ttk.Frame(tabs)
	tabs.add(tab,text=f" Python Shell ")
	tabs.pack(expand=1,fill='both')
	text_widget = tk.Text(tab,font=('verdana',12))
	text_widget.pack(fill=tk.BOTH,expand=1,side=tk.LEFT)
	Shell=Python(root,tab,text_widget)#,'>>> ')
	text_widget_list.append(text_widget)
	tabs_.append(Shell)

#defining  dark theme func
def darktheme():
	title.config(bg='grey14',fg='#00bfff')
	subtitle.config(bg='grey14',fg='white')
	info.config(bg='grey14',fg='grey')
	menubar.config(bg='grey14',fg='white',activebackground='grey14',activeforeground='#00bfff')
	file_menu.config(bg='grey14',fg='white',activebackground='gray14',activeforeground='#00bfff')
	edit_menu.config(bg='grey14',fg='white',activebackground='gray14',activeforeground='#00bfff')
	edit_menu_pref.config(bg='grey14',fg='white',activebackground='gray14',activeforeground='#00bfff')
	tools_menu.config(bg='grey14',fg='white',activebackground='gray14',activeforeground='#00bfff')
	help_menu.config(bg='grey14',fg='white',activebackground='gray14',activeforeground='#00bfff')
	root.config(bg='grey14')

#defining  dafault theme func
def defaulttheme():
	title.config(bg=backgroundColor,fg='#0493e5')
	subtitle.config(bg=backgroundColor,fg='black')
	info.config(bg=backgroundColor,fg='grey')
	menubar.config(bg=backgroundColor,fg='#000000',activebackground='skyblue',activeforeground='#000000')
	file_menu.config(bg=backgroundColor,fg='#000000',activebackground='skyblue',activeforeground='#000000')
	edit_menu.config(bg=backgroundColor,fg='#000000',activebackground='skyblue',activeforeground='#000000')
	edit_menu_pref.config(bg=backgroundColor,fg='#000000',activebackground='skyblue',activeforeground='#000000')
	tools_menu.config(bg=backgroundColor,fg='#000000',activebackground='skyblue',activeforeground='#000000')
	help_menu.config(bg=backgroundColor,fg='#000000',activebackground='skyblue',activeforeground='#000000')
	root.config(bg=backgroundColor)

#defining help options func
def help_options():
	top = getutils.help_win(root)
	top.grab_set()
	top.mainloop()

#defining visit func
def visit():
	try:
		import webbrowser
		webbrowser.open_new('https://github.com/smac01')
	except Exception as e: logger.exception('Webbrowser Exception')

#defining about menu
def about():
	top=tk.Toplevel(root)
	top.grab_set()
	top.geometry('300x175')
	top.resizable(0,0)
	tk.Label(top,text='Python Based Terminal Shell',font=('serif','14')).pack(pady=20)
	tk.Label(top,text='https://github.com/smac01',font=('courier','12'),fg='#0071e1').pack()
	tk.Label(top,text='Copyright (c) 2020',font=('verdana','10'),fg='#2b2b2b').pack()
	ttk.Button(top,text=' Visit ',command=visit).pack(anchor='w',padx=10,side='left')
	ttk.Button(top,text=' Close ',command=lambda: top.destroy()).pack(anchor='e',padx=10,side='right')
	top.mainloop()

if __name__ == "__main__":
	logger.info('Program Started')
	#find the user name
	user=os.getlogin() if os.name=='nt' else os.getenv('USER',os.getenv('USERNAME','user')).capitalize()
	#creating the menubar
	menubar = tk.Menu(root,tearoff=0)
	root.config(menu=menubar)
	
	#initializing submenus
	file_menu = tk.Menu(menubar,tearoff=0)
	edit_menu = tk.Menu(menubar,tearoff=0)
	tools_menu = tk.Menu(menubar,tearoff=0)
	help_menu = tk.Menu(menubar,tearoff=0)
	menubar.add_cascade(label='File',menu=file_menu)
	menubar.add_cascade(label='Edit',menu=edit_menu)
	menubar.add_cascade(label='Tools',menu=tools_menu)
	menubar.add_cascade(label='Help',menu=help_menu)

	#creating file menu
	file_menu.add_command(label='New Tab',compound=tk.LEFT,accelerator='Ctrl+Shift+T',command=addTab)
	file_menu.add_command(label='Close Tab',accelerator='Ctrl+Shift+W',command=closeTab)
	file_menu.add_command(label='Quit',accelerator='Ctrl+Shift+Q',command=lambda: root.destroy())

	#creating edit menu
	edit_menu.add_command(label='Cut',accelerator='Ctrl+X', command=lambda : cutcopypaste('<<Cut>>') if len(tabs.tabs())>0 else False)
	edit_menu.add_command(label='Copy',accelerator='Ctrl+C',command=lambda: cutcopypaste('<<Copy>>') if len(tabs.tabs())>0 else False)
	edit_menu.add_command(label='Paste',accelerator='Ctrl+P',command=lambda: cutcopypaste('<<Paste>>') if len(tabs.tabs())>0 else False)
	edit_menu.add_command(label='Clear',accelerator='Ctrl+L',command=lambda: basic_func('clear') if len(tabs.tabs())>0 else False)
	edit_menu.add_command(label='Zoom In',accelerator='Ctrl++',command=lambda: basic_func('zoom-in') if len(tabs.tabs())>0 else False)
	edit_menu.add_command(label='Zoom Out',accelerator='Ctrl+-',command=lambda: basic_func('zoom-out') if len(tabs.tabs())>0 else False)
	edit_menu.add_command(label='Zoom Reset',accelerator='Ctrl+0',command=lambda: basic_func('zoom-reset') if len(tabs.tabs())>0 else False )
	edit_menu.add_separator()
	edit_menu_pref = tk.Menu(edit_menu,tearoff=0)
	edit_menu.add_cascade(label='Preference',menu=edit_menu_pref)
	edit_menu_pref.add_command(label='Default Theme',command=defaulttheme)
	edit_menu_pref.add_command(label='Dark Theme',command=darktheme)

	#creating tool menu
	tools_menu.add_command(label='Python Interpreter',command=addPython)
	tools_menu.add_command(label='Color Picker', command=lambda: colorch('y') if len(tabs.tabs())>0 else colorch('n'))
	#creating help menu
	help_menu.add_command(label='Documentation',command=help_options)
	help_menu.add_command(label='About',command=about)

	#open, close and exit tab binding
	root.bind('<Control-T>', lambda event : addTab(event))
	root.bind('<Control-W>', lambda event : closeTab(event))
	root.bind('<Control-Q>', lambda event : root.destroy())
	root.bind('<Key>',keys)
	root.bind('<Button-3>',rightclickMenu)
	if os.name == 'posix':
		darktheme()
	root.mainloop()
