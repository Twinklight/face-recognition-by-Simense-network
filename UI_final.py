import tkinter.filedialog
from tkinter import *
from PIL import Image,ImageTk
from back_g import process
import math

import datetime
root=Tk()
root.geometry('600x630')

path1 = StringVar() #图片1地址
path2 = StringVar() #图片2地址
dissimilarity =StringVar() #不相似度
standard =StringVar() # 标准结果
run_time = StringVar()  #运行时间

root.title('人脸识别系统')
def start():#启动操作
    # time1 = datetime.datetime.now() #开始运行时的时间
    filename1 = path1.get()#图片1的地址
    filename2 = path2.get()#图片2的地址
    im1 = Image.open(filename1)
    im2 = Image.open(filename2)
    res = process(im1, im2)
    # dis_standard = math.tanh(res[0]/5)*(1/(1+math.exp(-res[0])-0.5))*2*100
    dis_standard = math.tanh(res[0]/5)*(1/(1+math.exp(-res[0]))-0.5)*2*100
    dissimilarity.set(str(dis_standard.__format__(".2f"))+'%' )  # 括号里填不相似度
    A = ""
    if res[0] < 1.5:
        A = "可能是一个人"
    else:
        A = "可能不是同一个人"
    standard.set(A)  # 括号里填标签
    # time2 =  datetime.datetime.now() # 运行结束时的时间

    run_time.set(res[1])

def callback1():
    fileName = filedialog.askopenfilename(filetypes=[("PNG",".png"),("JPG",".jpg")])
    path1.set(fileName)
    global tkImage1
    pilImage = Image.open(fileName)
    img = pilImage.resize((250, 250), Image.ANTIALIAS)
    tkImage1 = ImageTk.PhotoImage(image=pilImage)
    label = Label(root, image=tkImage1, width=250, height=250)
    label.place(relx=0.25,rely=0.5,anchor=CENTER,x=0,y=+35)

def callback2():
    fileName =filedialog.askopenfilename(filetypes=[("PNG",".png"),("JPG",".jpg")])
    path2.set(fileName)
    global tkImage2
    pilImage = Image.open(fileName)
    img = pilImage.resize((250, 250), Image.ANTIALIAS)
    tkImage2 = ImageTk.PhotoImage(image=pilImage)
    label = tkinter.Label(root, image=tkImage2, width=250, height=250)
    label.place(relx=0.75,rely=0.5,anchor=CENTER,x=0,y=+35)

#打开文件askopenfilename
#defaultextension自动添加后缀


entry1 = Entry(root, textvariable = path1,width=60)
entry2 = Entry(root, textvariable = path2,width=60)
entry3 = Entry(root, textvariable = dissimilarity,width=40)
entry4 = Entry(root, textvariable = standard,width=40)
entry5 = Entry(root, textvariable = run_time,width=40)

btn1 = Button(root, text="选择图片1",command =callback1,height=1,font=('微软雅黑',9))
btn2 = Button(root, text="选择图片2",command =callback2,height=1,font=('微软雅黑',9))
btn_start = Button(root, text="运行",command =start,font=('微软雅黑',15))

l_title = Label(root,text='人脸识别系统',borderwidth=3,font=('微软雅黑',30),width=25,background = 'white')
l_p1 = Label(root,text='图片1',borderwidth=3,font=('微软雅黑',15),width=25,background = 'white')
l_p2 = Label(root,text='图片2',borderwidth=3,font=('微软雅黑',15),width=25,background = 'white')
l_show1 = Label(root,width=38,height=16)
l_show2 = Label(root,width=38,height=16)
l_dissimilarity = Label(root,text='不相似度:',borderwidth=3,font=('微软雅黑',10),width=10,background = 'white')
l_standard = Label(root,text='      预测:',borderwidth=3,font=('微软雅黑',10),width=10,background = 'white')
l_time = Label(root,text='运行时间:',borderwidth=3,font=('微软雅黑',10),width=10,background = 'white')

l_title.place(relx=0.5, rely=0.08, anchor=CENTER)
entry1.place(relx=0.5, rely=0.5, anchor=CENTER, x=-40, y=-200)
btn1.place(relx=0.5, rely=0.5, anchor=CENTER, x=+220, y=-200)

entry2.place(relx=0.5, rely=0.5, anchor=CENTER, x=-40, y=-160)
btn2.place(relx=0.5, rely=0.5, anchor=CENTER, x=+220, y=-160)

l_p1.place(relx=0.25,rely=0.5,anchor=CENTER,x=0,y=-120)
l_p2.place(relx=0.75,rely=0.5,anchor=CENTER,x=0,y=-120)
l_show1.place(relx=0.25,rely=0.5,anchor=CENTER,x=0,y=+35)
l_show2.place(relx=0.75,rely=0.5,anchor=CENTER,x=0,y=+35)

l_dissimilarity.place(relx=0.15,rely=0.85,anchor=CENTER)
entry3.place(relx=0.50,rely=0.85,anchor=CENTER)
l_standard.place(relx=0.15,rely=0.90,anchor=CENTER)
entry4.place(relx=0.50,rely=0.90,anchor=CENTER)
l_time.place(relx = 0.15,rely=0.95,anchor=CENTER)
entry5.place(relx=0.50,rely=0.95,anchor=CENTER)
btn_start.place(relx=0.85,rely=0.875,anchor=CENTER)
root.resizable(0, 0) # 窗口大小不可变
root["background"] = "white"
root.mainloop()
