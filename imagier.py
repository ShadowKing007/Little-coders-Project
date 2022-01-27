##.............Sketch Imagier............##
##-------------------Required Libraries-------------------------##

from tkinter import *
import cv2
import numpy as np
from tkinter import filedialog
from PIL import Image,ImageTk

my_font=('Comic Sans MS',40,'bold')       
bt_font=('Calibre',20,'bold')
label_font=('Calibre',15,'italic')
img_title=('Calibre',10,'italic')

##--------------------------------Defined Functions--------------------------##

def cartoonf(imgi):
    global original, converted
    img=cv2.imread(imgi)
    data=np.float32(img).reshape((-1,3))
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,0.001)

    ret,label,center = cv2.kmeans(data,12,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center=np.uint8(center)
    result=center[label.flatten()]
    result=result.reshape(img.shape)
    image=Image.fromarray(result)

    #fin=Image.fromarray(result)
    #fin.show()
    #fina=PhotoImage(file=fin)
    #converted.create_image(50,10,image=fina,ANCHOR=CENTER)
    return None

def w_sketch():
    global panelA, panelB
    path=filedialog.askopenfilename()
    if len(path) > 0:
        image=cv2.imread(path)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edged=cv2.Canny(gray,50,100)
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        image=Image.fromarray(image)
        edged=Image.fromarray(edged)

        image=ImageTk.PhotoImage(image)
        edged=ImageTk.PhotoImage(edged)
        
        if panelA is None or panelB is None:
            panelA=Label(image=image)
            panelA.image=image
            panelA.place(x=80,y=330)

            panelB=Label(image=edged)
            panelB.image=image
            panelB.place(x=660,y=330)
        else:
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image=image
            panelB.image=image




##-------------------------------------App Window------------------------------##

img_file='kriti.jpg'

root=Tk()
root.title("Sketch Imagier")
root.configure(bg='#3f00a7')
root.geometry('1000x1000')

##-----------Start-------------------------##

heading=Label(root,text='Sketch',bg='#000',font=my_font,fg='#fff').place(x=0,y=0,height=100,width=1000)
order=Label(root,text='Please upload your image in jpg/jpeg/png image here:',font=label_font,bg='#3f00a7',fg='white').place(x=260,y=112) 
upload_btn=Button(root, text='Upload',bg='white',font=bt_font,fg='black',activebackground='#bbbbbb').place(x=430,y=150)

##-------------Options---------------------##

convert=Label(root,text='Convert to:',bg='#3f00a7',font=label_font,fg='white').place(x=440,y=200)
sketch=Button(root,text='Sketch',bg='white',fg='black',activebackground='black',activeforeground='white',command=lambda:w_sketch()).place(x=260,y=240)
black_and_white=Button(root,text='B & W',bg='white',fg='black',activebackground='black',activeforeground='white').place(x=350,y=240)
cartoon=Button(root,text='Cartoon',bg='white',fg='black',activebackground='black',activeforeground='white',command=lambda:cartoonf(img_file)).place(x=440,y=240)
word_sketch=Button(root,text='Word Sketch',bg='white',fg='black',activebackground='black',activeforeground='white').place(x=540,y=240)
painting=Button(root,text='Painting',bg='white',fg='black',activebackground='black',activeforeground='white').place(x=670,y=240)

divider=Canvas(root,width=900,height=1).place(x=50,y=290)

##---------------Image Section-------------##

original_title=Label(root,text='Your Original Image:',font=img_title,bg='#3f00a7',fg='white').place(x=100,y=310)
converted_title=Label(root,text='Your Converted Image:',font=img_title,bg='#3f00a7',fg='white').place(x=620,y=310)
panelA=None                                       #Canvas(root,width=300,height=300,bg='#260062',confine=True,scrollregion=(50,50,50,50))   # bg='white'
panelB=None                                       #Canvas(root,width=300,height=300,bg='#260062',confine=True,scrollregion=(50,50,50,50))


export=Button(root, text='Export',bg='white',font=bt_font,fg='black',activebackground='#bbbbbb').place(x=430,y=650)

root.mainloop()