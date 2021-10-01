from tkinter import *
from numpy import longcomplex
import csv
import tkinter.messagebox

def yes_or_no():
    a=tkinter.messagebox.askokcancel('Upload data','Do you want upload this data?')
    if a:
        upload_val()

def upload_val():
    name=e1.get()
    type=e2.get()
    tag1=e3.get()
    tag2=e4.get()
    zip=e5.get()
    website=e6.get()
    lat=e7.get()
    long=e8.get()
    adds=e9.get()
    street=e10.get()
    note=e11.get()

    # write into file
    #df=pd.DataFrame({'name':str(name),'type':str(type),'tag1':str(tag1),'tag2':str(tag2),'zipcode':str(zip),'website':str(website),'latitute':str(lat),
    #'longtitute':str(long),'address_number':str(adds),'street':str(street),'note':str(note)})
    #df.to_csv('pittCity_final.csv',mode='a')
    place=[name,lat,long,adds,street,zip,type,tag1,tag2,note,website]
    with open('pittCity_final.csv','a') as file:
        writer=csv.writer(file)
        writer.writerow(place)

    b=tkinter.messagebox.showinfo('Result','Uploaded Successfully')

def UI():
    root=Tk()
    root.title('Upload UI')  #title
    #root.geometry('500x300') window大小

    Label(root,text='Name:').grid(row=0,column=0)
    Label(root,text='Type:').grid(row=0,column=2)
    Label(root,text='Tag1:').grid(row=0,column=4)
    Label(root,text='Tag2:').grid(row=0,column=6)
    Label(root,text='Latitute:').grid(row=1,column=0)
    Label(root,text='Longitude:').grid(row=1,column=2)
    Label(root,text='Address Number:').grid(row=1,column=4)
    Label(root,text='Street:').grid(row=1,column=6)
    Label(root,text='Zipcode:').grid(row=2,column=0)
    Label(root,text='Website:').grid(row=2,column=2)
    Label(root,text='Note:').grid(row=2,column=4)

    e1=Entry(root)
    e1.grid(row=0,column=1,padx=7,pady=5) #name
    e2=Entry(root)
    e2.grid(row=0,column=3,padx=7,pady=5) #type
    e3=Entry(root)
    e3.grid(row=0,column=5,padx=7,pady=5) #tag1
    e4=Entry(root)
    e4.grid(row=0,column=7,padx=7,pady=5) #tag2
    e5=Entry(root)
    e5.grid(row=2,column=1,padx=7,pady=5) #zipcode
    e6=Entry(root)
    e6.grid(row=2,column=3,padx=10,pady=5)#website
    e7=Entry(root)
    e7.grid(row=1,column=1,padx=7,pady=5) #latitute
    e8=Entry(root)
    e8.grid(row=1,column=3,padx=7,pady=5) #longtitude
    e9=Entry(root)
    e9.grid(row=1,column=5,padx=7,pady=5) #adds num
    e10=Entry(root)
    e10.grid(row=1,column=7,padx=7,pady=5)#street
    e11=Entry(root)
    e11.grid(row=2,column=5,padx=7,pady=5)#note

    Button(root,text='Upload',width=10,command=yes_or_no).grid(row=3,column=0,sticky=E,padx=10,pady=5)
    Button(root,text='Exit',width=10,command=root.quit).grid(row=3,column=4,sticky=E,padx=10,pady=5)

    root.mainloop()