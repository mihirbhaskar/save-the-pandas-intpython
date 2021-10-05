import tkinter
from tkinter import *
from tkinter import ttk
from numpy import longcomplex
import csv
import tkinter.messagebox

root=Tk()
root.title('Upload UI')  #title
#root.geometry('500x300') window大小

Label(root,text='Name:').grid(row=0,column=0)
Label(root,text='Place ID:').grid(row=0,column=2)
Label(root,text='Category:').grid(row=0,column=4)
Label(root,text='Latitute:').grid(row=2,column=0)
Label(root,text='Longitude:').grid(row=2,column=2)
Label(root,text='Vicinity:').grid(row=2,column=4)


e1=Entry(root)
e1.grid(row=0,column=1,padx=7,pady=5) #name
e2=Entry(root)
e2.grid(row=0,column=3,padx=7,pady=5) #Place ID
comvalue=tkinter.StringVar()
e3=ttk.Combobox(root,textvariable=comvalue) #Category
e3.grid(row=0,column=5,padx=7,pady=5) #Place ID
e3['value']=('Clothing','Food','Household Goods','Housing','Training and other services')
#e3.current(1)  #default setting->Food
e4=Entry(root)
e4.grid(row=2,column=1,padx=7,pady=5) #Latitute
e5=Entry(root)
e5.grid(row=2,column=3,padx=7,pady=5) #Longitude
e6=Entry(root)
e6.grid(row=2,column=5,padx=10,pady=5)#Vicinity
e7=Entry(root)

def required():
    r1=e1.get()
    r2=e6.get()
    flag=1
    if len(r1)==0:
        tkinter.messagebox.showwarning('Warning','Please enter the name!')
        flag=0
    if len(r2)==0:
        tkinter.messagebox.showwarning('Warning','Please enter the Vicinity!')
        flag=0
    return flag


def yes_or_no():
    flag=required()
    if flag:
        a=tkinter.messagebox.askokcancel('Upload data','Do you want upload this data?')
        if a:
            upload_val()

def upload_val():
    name=e1.get()
    place=e2.get()
    cat=e3.get()
    if cat=='Clothing':
        flag1=1
        flag2=e7.get()
        flag3=e7.get()
        flag4=e7.get()
        flag5=e7.get()
    elif cat=='Food':
        flag1=e7.get()
        flag2=1
        flag3=e7.get()
        flag4=e7.get()
        flag5=e7.get()
    elif cat=='Household Goods':
        flag1=e7.get()
        flag2=e7.get()
        flag3=1
        flag4=e7.get()
        flag5=e7.get()
    elif cat=='Housing':
        flag1=e7.get()
        flag2=e7.get()
        flag3=e7.get()
        flag4=1
        flag5=e7.get()
    elif cat=='Training and other services':
        flag1=e7.get()
        flag2=e7.get()
        flag3=e7.get()
        flag4=e7.get()
        flag5=1  
    lat=e4.get()
    long=e5.get()
    vin=e6.get()

    # write into file
    with open('MainFrame.csv','r') as file:
        count=len(file.readlines())-1
    placeall=[count,name,place,lat,long,vin,flag1,flag2,flag3,flag4,flag5]
    with open('MainFrame.csv','a') as file:       
        writer=csv.writer(file)
        writer.writerow(placeall)

    b=tkinter.messagebox.showinfo('Result','Uploaded Successfully')

Button(root,text='Upload',width=10,command=yes_or_no).grid(row=3,column=0,sticky=E,padx=10,pady=5)
Button(root,text='Exit',width=10,command=root.quit).grid(row=3,column=4,sticky=E,padx=10,pady=5)

root.mainloop()
