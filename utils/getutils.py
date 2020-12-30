#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import platform, subprocess, os
import base64, hashlib

class Rotate:
	"""To manipulate ROT ciphers"""
	def RotateString(self,shift:int ,string: str):
		out=''
		self.shift=shift
		if self.shift > 26: raise Exception("Invalid shift rotation")
		self.string=string
		for i in self.string:
		    if (ord(i)>=110) and (ord(i)<=122):
		        if self.shift > 13:
		            count=ord(i) - (26 - self.shift)
		        else:
		            count = ord(i) + self.shift
		            if count > 122:
		                count=count-26
		        out+=chr(count)
		    elif (ord(i)>=97) and (ord(i)<=109):
		        count=ord(i)+self.shift
		        if count > 122:
		            count=count-26
		        out+=chr(count)
		    elif (ord(i)>=78) and (ord(i)<=90):
		        if self.shift > 13:
		            count=ord(i) - (26 - self.shift)
		        else:
		            count = ord(i) + self.shift
		            if count > 90:
		                count=count-26
		        out+=chr(count)
		    elif (ord(i)>=65) and (ord(i)<=77):
		        count=ord(i) + self.shift
		        if count > 90:
		            count = count - 26
		        out+=chr(count)
		    else:
		        out+=i
		return out

	def RotateNum(self,string:str):
	    out=""
	    self.string=string
	    for i in self.string:
	        if (ord(i)>=53) and (ord(i)<=57):
	            num=ord(i)
	            out+=str(chr(num-5))
	        elif (ord(i)>=48) and (ord(i)<=52):
	            num=ord(i)
	            out+=str(chr(num+5))
	        else:
	            out+=i
	    return out
	def rot47(self,string: str):
		rot47=''
		for i in string:
			if (ord(i)>=80) and (ord(i)<=126):
				count = ord(i) - 47
				rot47 += chr(count)
			elif (ord(i) >= 33) and (ord(i) <= 79):
				count = ord(i) + 47
				rot47 += chr(count)
			else:
				rot47 += i
		return rot47

rot=Rotate()
exceptions = ['sh','/bin/sh','bash','/bin/bash','vim','nano','ssh','top','htop','firefox']

def help_win(master):
	win = tk.Toplevel(master)
	win.geometry('650x500')
	win.resizable(0,0)
	tabs = ttk.Notebook(win); tabs.pack(expand=1,fill='both')
	tab1=ttk.Frame(tabs); tab2=ttk.Frame(tabs)
	tabs.add(tab1,text=f"Keys"); tabs.add(tab2,text=f"Commands")
	tk.Label(tab1,text='Shortcut Keys', font=('consolas',18,'bold')).grid(row=0,padx=10,pady=20)
	tk.Label(tab1,text='1',font=('verdana',12)).grid(row=1,column=0,pady=5)
	tk.Label(tab1,text='New Tab',font=('verdana',12)).grid(row=1,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Shift+Ctrl+T',font=('verdana',12)).grid(row=1,column=2,padx=10,pady=5)
	tk.Label(tab1,text='2',font=('verdana',12)).grid(row=2,column=0,pady=5)
	tk.Label(tab1,text='Close Tab',font=('verdana',12)).grid(row=2,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Shift+Ctrl+W',font=('verdana',12)).grid(row=2,column=2,padx=10,pady=5)
	tk.Label(tab1,text='3',font=('verdana',12)).grid(row=3,column=0,pady=5)
	tk.Label(tab1,text='Close Window',font=('verdana',12)).grid(row=3,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Shift+Ctrl+Q',font=('verdana',12)).grid(row=3,column=2,padx=10,pady=5)
	tk.Label(tab1,text='4',font=('verdana',12)).grid(row=4,column=0,pady=5)
	tk.Label(tab1,text='Previous Tab',font=('verdana',12)).grid(row=4,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Ctrl+Page Up/Ctrl+Tab',font=('verdana',12)).grid(row=4,column=2,padx=10,pady=5)
	tk.Label(tab1,text='5',font=('verdana',12)).grid(row=5,column=0,pady=5)
	tk.Label(tab1,text='Next Tab',font=('verdana',12)).grid(row=5,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Ctrl+Page Down/Shift+Ctrl+Tab',font=('verdana',12)).grid(row=5,column=2,padx=10,pady=5)
	tk.Label(tab1,text='6',font=('verdana',12)).grid(row=6,column=0,pady=5)
	tk.Label(tab1,text='Zoom In',font=('verdana',12)).grid(row=6,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Ctrl+=',font=('verdana',12)).grid(row=6,column=2,padx=10,pady=5)
	tk.Label(tab1,text='7',font=('verdana',12)).grid(row=7,column=0,pady=5)
	tk.Label(tab1,text='Zoom Out',font=('verdana',12)).grid(row=7,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Ctrl+-',font=('verdana',12)).grid(row=7,column=2,padx=10,pady=5)
	tk.Label(tab1,text='8',font=('verdana',12)).grid(row=8,column=0,pady=5)
	tk.Label(tab1,text='Zoom Reset',font=('verdana',12)).grid(row=8,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Ctrl+0',font=('verdana',12)).grid(row=8,column=2,padx=10,pady=5)
	tk.Label(tab1,text='9',font=('verdana',12)).grid(row=9,column=0,pady=5)
	tk.Label(tab1,text='Clear Line',font=('verdana',12)).grid(row=9,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Ctrl+U',font=('verdana',12)).grid(row=9,column=2,padx=10,pady=5)
	tk.Label(tab1,text='10',font=('verdana',12)).grid(row=10,column=0,pady=5)
	tk.Label(tab1,text='Clear Scren',font=('verdana',12)).grid(row=10,column=1,padx=10,pady=5)
	tk.Label(tab1,text='Ctrl+L',font=('verdana',12)).grid(row=10,column=2,padx=10,pady=5)
	tk.Label(tab2,text='Buildin Commands', font=('consolas',18,'bold')).grid(row=0,padx=20,pady=20)
	tk.Label(tab2,text='Gui-cmd',font=('verdana',12)).grid(row=1,column=0,padx=10,pady=5)
	tk.Label(tab2,text='Display shell cmds',font=('verdana',12)).grid(row=1,column=1,padx=10,pady=5)
	tk.Label(tab2,text='History',font=('verdana',12)).grid(row=2,column=0,padx=10,pady=5)
	tk.Label(tab2,text='Display cmd histroy',font=('verdana',12)).grid(row=2,column=1,padx=10,pady=5)
	tk.Label(tab2,text='Python',font=('verdana',12)).grid(row=3,column=0,padx=10,pady=5)
	tk.Label(tab2,text='Open Python Interpreter',font=('verdana',12)).grid(row=3,column=1,padx=10,pady=5)
	tk.Label(tab2,text='Themelight',font=('verdana',12)).grid(row=4,column=0,padx=10,pady=5)
	tk.Label(tab2,text='Display shell in light theme',font=('verdana',12)).grid(row=4,column=1,padx=10,pady=5)
	tk.Label(tab2,text='Themedark',font=('verdana',12)).grid(row=5,column=0,padx=10,pady=5)
	tk.Label(tab2,text='Display shell in light dark',font=('verdana',12)).grid(row=5,column=1,padx=10,pady=5)
	tk.Label(tab2,text='Intr',font=('verdana',12)).grid(row=6,column=0,padx=10,pady=5)
	tk.Label(tab2,text='Color for interactive prompt',font=('verdana',12)).grid(row=6,column=1,padx=10,pady=5)
	tk.Label(tab2,text='Read',font=('verdana',12)).grid(row=7,column=0,padx=10,pady=5)
	tk.Label(tab2,text='display the content of the file',font=('verdana',12)).grid(row=7,column=1,padx=10,pady=5)
	tk.Label(tab2,text='Write',font=('verdana',12)).grid(row=8,column=0,padx=10,pady=5)
	tk.Label(tab2,text='Write content to the file',font=('verdana',12)).grid(row=8,column=1,padx=10,pady=5)
	return win

def readFile(file):
	checkFile = os.path.isfile(file)
	try:
		if checkFile:
			with open(file) as f:
				content = f.read()
			return str(content)
		else:
			return f'{file} does not exists'
	except Exception as e:
		return f'{file}: error in reading file'		

def getoutput(cmd):
	cmd = cmd.split()
	cmdsList = [str(i) for i in cmd]
	if cmdsList[0] in exceptions:
		return f'Exception commands cannot be executed.'
	
	if cmdsList[0] == "echo":
		return ' '.join(cmdsList[1:])

	elif cmdsList[0] == "pwd" or cmdsList[0] == "cwd":
			return os.getcwd()

	elif cmdsList[0] == 'cd':
		try:
			os.chdir(cmdsList[1])
			return f'Directory changed to {os.getcwd()}'
		except:
			return 'Directory: does not exists'
	
	elif cmdsList[0]=="base64" and len(cmdsList)>=1:
		try:
			if cmdsList[1] == "-e":
				return base64.b64encode(' '.join(cmdsList[2:]).encode()).decode()
			elif cmdsList[1] == "-d":
				return base64.b64decode(' '.join(cmdsList[2:])).decode()
			elif cmdsList[1] == '--file' and len(cmdsList)>1:
				file_content = readFile(cmdsList[2])
				temp = base64.b64encode(' '.join(file_content).encode()).decode()
				return temp
			elif cmdsList[1] in ["-h",'--help']:
				return "Options:\n-e	encode\n-d	decode\n--file	encode\\decode file"
			else:
				return "base64: Invalid options\nOptions:\n-e	encode\n-d	decode\n--file	encode\\decode file"
		except:
			return "base64: Invalid input\nTry 'base64 -h'"
	
	elif cmdsList[0] in ["md5",'sha1','sha224','sha256','sha384','sha512']:
		try:
			if cmdsList[0]=='md5':
				return hashlib.md5(cmdsList[1].encode()).hexdigest()
			elif cmdsList[0]=='sha1':
				return hashlib.sha1(cmdsList[1].encode()).hexdigest()
			elif cmdsList[0]=='sha224':
				return hashlib.sha224(cmdsList[1].encode()).hexdigest()
			elif cmdsList[0]=='sha256':
				return hashlib.sha256(cmdsList[1].encode()).hexdigest()
			elif cmdsList[0]=='sha384':
				return hashlib.sha384(cmdsList[1].encode()).hexdigest()
			elif cmdsList[0]=='sha512':
				return hashlib.sha512(cmdsList[1].encode()).hexdigest()
		except:
			return f"{cmdsList[0]}: Invalid input"		

	elif cmdsList[0]=='ipconfig' or cmdsList[0]=='ifconfig':
		return subprocess.run(['ipconfig'],stdout=subprocess.PIPE).stdout.decode() if os.name == 'nt' \
		else subprocess.run(['ifconfig'],stdout=subprocess.PIPE).stdout.decode() 
	
	elif cmdsList[0]=='sysinfo':
		sysinfo = "System Info:-\n"+"-"*30
		x=platform.uname()
		sysinfo += F"\nSystem: {x.system}\nHostname: {x.node}"
		sysinfo += F"\nRelease: {x.release}\nVersion: {x.version}\nMachine: {x.machine}"
		return sysinfo
	
	elif cmdsList[0]=='rot' and len(cmdsList)==1:
		return "Available rot ciphers:\n\trot5, rot13, rot18, rot47\nUse rot -c to genearate custom rot cipher between 0 - 25"
	
	elif cmdsList[0] == 'rot' and cmdsList[1]=='-c' and len(cmdsList)>2:
		if cmdsList[2].isdigit() and len(cmdsList)>3:
			return rot.RotateString(int(cmdsList[2]),' '.join(cmdsList[3:]))
		else:
			return "Invalid Input:\nsample: rot -c 14 hello"
	
	elif cmdsList[0]=='rot47':
		if len(cmdsList)>1 and cmdsList[1]:
			shift=47
			rot47 = rot.rot47(' '.join(cmdsList[1:]))
			return rot47
		else:
			return 'Help: rot47 hello@$123'

	elif cmdsList[0]=='rot18':
		if len(cmdsList)>1 and cmdsList[1]:
			shift=13
			StringResponse = rot.RotateString(shift,' '.join(cmdsList[1:]))
			rot18 = rot.RotateNum(StringResponse)
			return rot18
		else:
			return 'Help: rot18 hello@$123'
	
	elif cmdsList[0]=='rot13':
		if len(cmdsList)>1 and cmdsList[1]:
			shift=13
			rot13=rot.RotateString(shift,' '.join(cmdsList[1:]))
			return rot13
		else:
			return 'Help: rot13 hello@$123'

	elif cmdsList[0]=='rot5':
		if len(cmdsList)>1 and cmdsList[1]:
			return rot.RotateNum(' '.join(cmdsList[1:]))
		else:
			return 'Help: rot5 abc123"'
	
	elif cmdsList[0] == 'listdir':
		try:
			listdir = '\n'.join(os.listdir(cmdsList[1]))
		except:
			listdir = '\n'.join(os.listdir())
		return listdir

	elif cmdsList[0]=='folders':
		folder = [i for i in os.listdir() if os.path.isdir(i)]
		return '\n'.join(folder)

	elif cmdsList[0]=='listfile':
		file = [i for i in os.listdir() if os.path.isfile(i)]
		return "\n".join(file)

	else:
		try:
			temp = subprocess.run(cmdsList,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			temp = (temp.stdout+temp.stderr).decode()
			return temp
		except:	
			return ' '.join(cmd)+": can't execute command"

