import tkinter as tk
from tkinter import ttk,messagebox, colorchooser
from math import floor, ceil
import os,subprocess,sys

class TextBody:
	def __init__(self,root,master,textWidget):
		self.root = root
		self.master=master
		self.text=textWidget
		self.fontsize=12;self.intrcolor='#00bfff';self.bg='#242424'
		self.fg='#ffffff';self.cursorcolor='#ffffff'
		self.scroll = tk.Scrollbar(self.text,command=self.text.yview, cursor='hand2',width=12 )
		self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
		self.text.config(font=("Consolas",self.fontsize),fg=self.fg,bg=self.bg,insertbackground=self.cursorcolor,yscrollcommand=self.scroll.set)
		self.text.bind('<Key>',self.on_key) #to bind keys to text widget
		self.cmd=None
		self.cmdList=[]
		self.cmdPos=0;self.write=False
		self.text.bind('<Control-l>',lambda event: self.clearText(event))
		self.text.bind('<Control-u>',self.clearLine)
		self.text.bind('<Control-d>',self.clearText)
		self.text.bind('<Control-equal>',self.zoom_in)
		self.text.bind('<Control-minus>',self.zoom_out)
		self.text.bind('<Control-0>',self.zoom_reset)

	def insert_text(self, txt="", end="\n"):
		self.text.insert(tk.END, txt+end)
		self.text.see(tk.END) # make sure it is visible

	def show_prompt(self,interactiveprompt='>>> '):
		if self.write: self.interactiveprompt='write>>' 
		self.insert_text(f"{self.interactiveprompt} ", end='')
		self.text.mark_set(tk.INSERT, tk.END) # make sure the input cursor is at the end
		self.cursor = self.text.index(tk.INSERT) # save the input position
		self.text.tag_add("changecolor",floor(float(self.cursor))+0.0,self.cursor)
		self.text.tag_config("changecolor",foreground=self.intrcolor,font=("Courier",self.fontsize,"bold"))

	#basic key func (up, down, left, right keys)
	def on_key(self,event):
		if event.keysym == 'Return':
			self.cmd = self.text.get(self.cursor, tk.END).strip()
			if self.cmd:
				self.cmdList.append(self.cmd)
			self.insert_text()
			self.do(self.cmd)
			self.show_prompt(self.interactiveprompt)
			return "break"
		elif event.keysym == "Up":
			if len(self.cmdList)!=0:
				if self.cmdPos > len(self.cmdList):
					return "break"
				self.cmdPos+=1;
				self.temp=self.cmdList[len(self.cmdList)-self.cmdPos]
				self.text.delete(self.cursor,tk.END)
				self.text.insert(self.cursor,self.temp)
			else:
				pass
			return "break"

		elif event.keysym == "Down":
			if len(self.cmdList)!=0 :
				try:
					if self.cmdPos <= 0:
						return "break"
					self.cmdPos+=(-1);
					self.temp=self.cmdList[len(self.cmdList)-self.cmdPos]
					self.text.delete(self.cursor,tk.END)
					self.text.insert(self.cursor,self.temp)
				except:
					self.text.delete(self.cursor,tk.END)
					return "break"
		elif event.keysym in ("Left","BackSpace"):
			current = self.text.index(tk.INSERT)
			if self.text.compare(current,"==",self.cursor):
				return "break"

	#clear line
	def clearLine(self,*args):
		self.text.delete(self.cursor,tk.END)
	
	#clear text
	def clearText(self,*args):
		self.text.delete(1.0,tk.END)
		self.show_prompt()
	
	#zoom in func
	def zoom_in(self,*args):
		self.fontsize+=1
		self.text.config(font=("Consolas",self.fontsize))
		self.text.tag_config("changecolor",foreground=self.intrcolor,font=("Consolas",self.fontsize,"bold"))

	#zoom in func
	def zoom_out(self,*args):
		self.fontsize-=1
		self.text.config(font=("Consolas",self.fontsize))
		self.text.tag_config("changecolor",foreground=self.intrcolor,font=("Consolas",self.fontsize,"bold"))

	#zoon reset func
	def zoom_reset(self,*args):
		self.fontsize=10
		self.text.config(font=("Consolas",self.fontsize))
		self.text.tag_config("changecolor",foreground=self.intrcolor,font=("Consolas",self.fontsize,"bold"))

	#defining colorprefernece
	def colorpreference(self):
		top = tk.Toplevel(self.root)
		top.geometry('400x270') if os.name == 'nt' else top.geometry('500x270')
		self.root.grab_set()
		top.resizable(0,0)
		self.bgColor=tk.StringVar();self.intrColor=tk.StringVar();self.fgColor=tk.StringVar();self.cursorColor=tk.StringVar()
		self.bgColor.set(self.bg);self.intrColor.set(self.intrcolor);self.fgColor.set(self.fg);self.cursorColor.set(self.cursorcolor)
		ttk.Label(top,text='Preference',font=('Consolas','14','bold')).grid(row=0,column=1,padx=15,pady=10)
		ttk.Label(top,text='Background',font=('Consolas','12')).grid(row=1,column=0,padx=15,pady=10)
		ttk.Entry(top,textvariable=self.bgColor).grid(row=1,column=1,padx=10)
		ttk.Button(top,text='Change',command=self.colorBg).grid(row=1,column=2,padx=10)
		ttk.Label(top,text='Foreground',font=('Consolas','12')).grid(row=2,column=0,pady=10)
		ttk.Entry(top,textvariable=self.fgColor).grid(row=2,column=1)
		ttk.Button(top,text='Change',command=self.colorFg).grid(row=2,column=2)
		ttk.Label(top,text='Intr-Color',font=('Consolas','12')).grid(row=3,column=0,pady=10)
		ttk.Entry(top,textvariable=self.intrColor).grid(row=3,column=1)
		ttk.Button(top,text='Change',command=self.colorIntr).grid(row=3,column=2)
		ttk.Label(top,text='Cursor-color',font=('Consolas','12')).grid(row=4,column=0,pady=10)
		ttk.Entry(top,textvariable=self.cursorColor).grid(row=4,column=1)
		ttk.Button(top,text='Change',command=self.colorCursor).grid(row=4,column=2)
		ttk.Button(top,text=' Done ',command=lambda: top.destroy()).place(relx=0.4,rely=0.85)
		top.mainloop()
	
	#background color
	def colorBg(self):
		self.bg = colorchooser.askcolor(title='Choose Color')[1]
		self.bgColor.set(self.bg)
		self.text.config(fg=self.fg,bg=self.bg,insertbackground=self.cursorcolor)
	
	#foreground color
	def colorFg(self):
		self.fg = colorchooser.askcolor(title='Choose Color')[1]
		self.fgColor.set(self.fg)
		self.text.config(fg=self.fg,bg=self.bg,insertbackground=self.cursorcolor)
	
	#cursor color
	def colorCursor(self):
		self.cursorcolor = colorchooser.askcolor(title='Choose Color')[1]
		self.cursorColor.set(self.cursorcolor)
		self.text.config(fg=self.fg,bg=self.bg,insertbackground=self.cursorcolor)
	
	#interactive prompt color
	def colorIntr(self):
		self.intrcolor = colorchooser.askcolor(title='Choose Color')[1]	
		self.intrColor.set(self.intrcolor)
		self.text.tag_config("changecolor",foreground=self.intrcolor,font=("Consolas",self.fontsize,"bold"))
