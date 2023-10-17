from tkinter import*
from tkinter. filedialog import*
from tkinter. messagebox import*
from tkinter. scrolledtext import*
import time
import os
from subprocess import Popen,PIPE
def pydata(com):
	xm=os.Popen(com,stdin=PIPE,stderr=PIPE,shell=True)
def mainx():
	calc=Tk()
	calc. title("SimpleCalc")
	calc. geometry("200x150+200+200")
	out=ScrolledText(calc, height=1,width=20)
	out. grid()
	def equal():
		ou=out. get(0.0,END)
		out. delete(0.0,END)
		out.insert(0.0,eval(ou))
	Button(calc, text="=", command=equal). 	grid()
	calc. mainloop()
def mainy():
	def he():
		def save():
			with open("index.html",'w') as f:
				f. write(n. get(0.0,END))
				f. close()
		x. destroy()
		html=Tk()
		html. title("Editor")
		Label(html, text="index.html"). pack()
		n=ScrolledText(html, height=10,width=10)
		n. pack(fill=Y)
		if os. path. isfile("index.html"):
			with open("index.html",'r') as f:
				n. insert(0.0,f. read())
		else:
			n. insert(0.0,"<html>\n<body>\n</body>\n</html>")
		Button(html, text="Save", command=save). pack()
	x=Tk()
	Button(x, text="Go", command=he). pack()
def mainz():
	rr=Tk()
	rr. title("PyConsole-NewRun")
	def run():
		aweq=ad. get(0.0,END)
	Label(rr, text="Output in the gpo portion"). pack()
	ad=Text(rr, height=5,width=10)
	ad. pack()
	Button(rr, text="Run", command=run). 		pack()
	rr. mainloop()
def maina():
	r=Tk()
	r. title("FunWriter")
	x=ScrolledText(r,state='normal', height=5,	width=5, wrap='word', pady=2, padx=3, undo=True)
	x. pack()
	r. mainloop()
	
def cco():
	r=Tk()
	r.title("gclock")
	x=Frame(r)
	x.pack(anchor="center",side='left',	fill=BOTH)
	def cc():
		ax=time.strftime("%H:%M:%S %p")
		a.configure(text=ax)
		r.after(1000,cc)
	a=Label(x,fg="white",bg="black")
	a.pack()
	cc()