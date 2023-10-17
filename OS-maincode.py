from tkinter import*
from tkinter. filedialog import*
from tkinter. messagebox import*
from tkinter. scrolledtext import*
import app
import os
from subprocess import Popen,PIPE
def subber(doing):
	xm=Popen(doing,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
	out,err=xm.communicate()
	ai.insert(0.0,out)
	ai.insert(0.0,err)
def apper():
	dupe=askopenfilename(filetypes=[('Python Files','*.py')])
	python=f'python {dupe}'
	subber(python)
	with open(dupe,'r') as r:
		nex=r.read()
		exec(nex)

def edit():
	app. mainy()
gos=Tk()
gos. title("version- 2023.1")
menu=Menu(gos)
prog=Menu(menu)
write=Menu(prog)
def exrt():
	ad=askyesno(title="-Shut Down", message="Shut Down the computer?")
	if ad:
		gos. destroy()

def con():
	app.mainz()
def setui():
	def exec():
		a.configure(text="")
		abc.insert(0,"Welcome to -version- 2023.1")
	def exe():
		aw=abc. get()
		xy. configure(text=aw)
		with open('xy.txt','w') as f:
			f. write(aw)
			f. close()
		app. destroy()
	def ext():
		aw=abc. get()
		a. configure(text="look like: "+aw)
	app=Toplevel()
	app. title("setup")
	a=Label(app, text="Set the OS")
	a. pack()
	abc=Entry(app)
	abc. pack()
	Button(app, text="Set", command=ext). pack()
	Button(app, text="apply", command=exe). pack()
	Button(app, text="Reset", command=exec). pack()
def ccc():
	app.cco()
def cal():
	app. mainx()
def writer():
	app.maina()
prog. add_cascade(label="System Apps", menu=write)
write. add_command(label="HtmEdit", command=edit)
write.add_command(label="GClock",command=ccc)
write. add_command(label="PyConsole", command=con)
write. add_command(label="Calculator", command=cal)
write. add_command(label="FunWriter", command=writer)
write. add_command(label="Shut Down", command=exrt)
write. add_command(label="Setup", command=setui)
write.add_command(label="softlauncher",command=apper)
menu. add_cascade(label="<LAUNCH>", menu=prog)
gos. config(menu=menu)
xy=Label(gos, text="Welcome to os")
xy. pack()
if os.path.isfile('xy.txt'):
	with open('xy.txt','r') as f:
		text=f. read()
		xy. configure(text=text)
ai=Text(gos)
ai.pack()		
gos. mainloop()