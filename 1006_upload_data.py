#Provide information
import tkinter
from tkinter import *
from tkinter import ttk
from numpy import longcomplex
import csv
import tkinter.messagebox
import json
import requests


google_apikey = 'AIzaSyDtHG5_OuzsebcXqnofVA6P-9tZ3Go5tl0'

def getAddressCoords(input_address, api_key):
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=' 
           + input_address + '&key=' + api_key)
    
    response = requests.get(url)
    result = json.loads(response.text)
    
    # Check these error codes again - there may be more
    if result['status'] not in ['INVALID_REQUEST', 'ZERO_RESULTS']:
                
        lat = result['results'][0]['geometry']['location']['lat']
        long = result['results'][0]['geometry']['location']['lng']

        return (lat, long) 
    
    # Flagging if there was an error
    else:
        return "Invalid address"


root=Tk()
root.title('Upload UI')  #title
#root.geometry('500x300') window大小

Label(root,text='Name:').grid(row=0,column=0)
Label(root,text='Vicinity:').grid(row=0,column=2)
Label(root,text='Category:').grid(row=1,column=0)
Label(root,text='Notes:').grid(row=2,column=0)
Label(root,text='Website:').grid(row=2,column=2)

e1=Entry(root)
e1.grid(row=0,column=1,padx=7,pady=5) #name
#comvalue=tkinter.StringVar()
#e3=ttk.Combobox(root,textvariable=comvalue) #Category
#e3.grid(row=0,column=5,padx=7,pady=5) #Place ID
#e3['value']=('Clothing','Food','Household Goods','Housing','Training and other services')
#e3.current(1)  #default setting->Food
category = {0:'Clothing',1:'Food',2:'Household Goods',3:'Housing',4:'Training and other services'}
dic1 = {}
for i in range(len(category)):
    dic1[i] = BooleanVar()
    Checkbutton(root,text=category[i],variable=dic1[i]).grid(row=1,column=i+1)
e4=Entry(root)
e4.grid(row=2,column=1,padx=7,pady=5)#Notes
e5=Entry(root)
e5.grid(row=2,column=3,padx=7,pady=5)#Website   
e6=Entry(root)
e6.grid(row=0,column=3,padx=7,pady=5)#Vicinity
e7=Entry(root)

def required(): #name,vicinity
    r1=e1.get()
    r2=e6.get()
    flag=1
    if len(r1)==0:
        tkinter.messagebox.showwarning('Warning','Please enter the name!')
        flag=0
    if len(r2)==0:
        tkinter.messagebox.showwarning('Warning','Please enter the Vicinity!')
        flag=0
    if getAddressCoords(e6.get(), 'AIzaSyDtHG5_OuzsebcXqnofVA6P-9tZ3Go5tl0') == 'Invalid address':
        tkinter.messagebox.showwarning('Warning','Please enter a valid address!')
        flag=0
    return flag

def mutichoice():
    cats=[]
    for key,value in dic1.items():
        if value.get() == True:
            cats.append(category[key])
    numb=len(cats)
    return cats,numb

def yes_or_no():
    flag=required()
    if flag:
        a=tkinter.messagebox.askokcancel('Upload data','Do you want upload this data?')
        if a:
            upload_val()
#**************************            

def upload_val():
    name=e1.get()
    place = 'na'
    notes=e4.get()
    website=e5.get()
    cat,numb=mutichoice()
    flag1=e7.get()
    flag2=e7.get()
    flag3=e7.get()
    flag4=e7.get()
    flag5=e7.get()
    for i in range(numb):
        if cat[i]=='Clothing':
            flag1=1
        elif cat[i]=='Food':
            flag2=1
        elif cat[i]=='Household Goods':
            flag3=1
        elif cat[i]=='Housing':
            flag4=1
        elif cat[i]=='Training and other services':
            flag5=1
    #flag1,flag2,flag3,flag4,flag5=fill(flag1,flag2,flag3,flag4,flag5)
    lat= list(getAddressCoords(e6.get(), 'AIzaSyDtHG5_OuzsebcXqnofVA6P-9tZ3Go5tl0'))[0]
    long=list(getAddressCoords(e6.get(), 'AIzaSyDtHG5_OuzsebcXqnofVA6P-9tZ3Go5tl0'))[1]
    vin=e6.get()

    # write into file
    with open('MainFrame.csv','r') as file:
        count=len(file.readlines())-1
    placeall=[count,name,place,lat,long,vin,flag1,flag2,flag3,flag4,flag5,notes,website]
    with open('MainFrame.csv','a') as file:       
        writer=csv.writer(file)
        writer.writerow(placeall)

    b=tkinter.messagebox.showinfo('Result','Uploaded Successfully')

Button(root,text='Upload',width=10,command=yes_or_no).grid(row=3,column=0,sticky=E,padx=10,pady=5)
Button(root,text='Exit',width=10,command=root.quit).grid(row=3,column=3,sticky=E,padx=10,pady=5)

root.mainloop()
