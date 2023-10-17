from tkinter import*
from tkinter.filedialog import*
from subprocess import Popen,PIPE
def run(com):
    xm=Popen(com,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    out,err=xm.communicate()
    cout.insert(0.0,out)
    cout.insert(0.0,err)
PyDE = Tk()
t = 'new'
PyDE.title(t+"-PyDE By Testbot")
temp=''
def tit(s):
    global t
    t=s   
    PyDE.title(t+"-PyDE By Testbot")
def Openfile():
        p=askopenfilename(filetypes=[('Python Files','*.py'),('HTML Files','*.html'),('Turtle Scripts','*.ts')])
        with open(p,'r') as file:
            code=file.read()
            IOsys.delete('1.0',END)
            IOsys.insert('1.0',code)
            global temp
            temp=p
            tit(p) 
def Save():
        p=asksaveasfilename(filetypes=[('Python Files','*.py'),('HTML Files','*.html'),(' Turtle Scripts','*.ts')])
        with open(p,'w') as file:
            code=IOsys.get('1.0',END)
            file.write(code)
            global temp
            temp=p
            tit(p)    
def info():
    try:
        with open('Pyde-Linux.py','r') as file:
            code=file.read()
            IOsys.delete('1.0',END)
            IOsys.insert('1.0',code)
            global temp
            temp='/home/user/Desktop/ICT/vspc/Pyde-Linux.py'
            tit(temp)
    except:
        pass        
def clear():
        IOsys.delete('1.0',END)
def execute():
        if temp=='':
            fo=Toplevel()
            fo.title("comfig save!")
            Label(fo,text="save your code please!!!!!!!!!!").pack()
            Button(fo,text="ok",command=exit)    
        else:
            if TRUE:
                if 'input()'  in IOsys.get(0.0,END):
                    a= IOsys.get(0.0,END)
                    exec(a) 
                else:
                    if '.py' in temp:
                        com=f'python {temp}'
                    run(com)
                   
def ter():
   
    ssx=Tk()
    ssx.title("terminal(python || bash)")
    def ccx():
        ax=a.get()
        run(ax)
    a=Entry(ssx)
    a.pack()
    but=Button(ssx,text="run",command=ccx)
    but.pack()
top=Menu(PyDE)
executer=Menu(top)
executer.add_command(label="execute ",command=execute)
executer.add_command(label="clear all ",command=clear)
executer.add_command(label="Open",command=Openfile)
executer.add_command(label="Save",command=Save)
executer.add_command(label="terminal",command=ter)
executer.add_command(label="SRC code here",command=info)
executer.add_command(label="close PyDE(your code will be lost!)",command=exit)
top.add_cascade(label="IO System",menu=executer)
PyDE.config(menu=top)
IOsys=Text(PyDE,height=20,width=100)
IOsys.pack()
cout=Text(PyDE,height=12,width=100)
cout.pack()
cout.insert('1.0','')
PyDE.mainloop()   