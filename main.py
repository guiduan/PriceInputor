# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter.filedialog
import os
import pyautogui, time, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

root = Tk()
root.title('综合单价自动输入工具')  # 窗口名字
root.geometry('400x450')  # 设置主窗口大小
root.resizable(width=False, height=False)


def openfile():
    filename = tkinter.filedialog.askopenfilename(filetypes=[('txt文件', '*.txt')])
    e1.delete(0, END)
    e1.insert(0, filename)
    if filename != '':
        try:
            with open(filename) as f:
                text.delete(0.0, END)
                for each_line in f:
                    text.insert(INSERT, each_line)
                basename = os.path.basename(filename)
                text1.insert(0.0,
                             '[%s]加载单价文件%s...\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), basename))
                text1.update()
        except OSError as reason:
            print('文件不存在！\n请重新输入文件名' + str(reason))
            return


def savefile():
    filename = str(e1.get())
    if filename == '':
        text1.insert(0.0, '[%s]未选择单价文件，请重新选择...\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        text1.update()
        messagebox.showinfo(title='message', message='未找到单价文件，请重新选择。')
        return
    file = Path(filename)
    if file.is_file():
        file_exist= messagebox.askokcancel('消息框标题', '文件已经存在，是否覆盖原文件？')
        if file_exist:
            with open(filename, 'w') as f:
                try:
                    f.write(text.get(0.0, END))
                    f.flush()
                    basename = os.path.basename(filename)
                    messagebox.showinfo(title='message', message='%s  保存成功' % basename)
                except:
                    messagebox.showinfo(title='unfortunately ', message='保存失败')
        else:
            pass
    return


def inputprice():
    filename = str(e1.get())
    if filename == '':
        text1.insert(0.0, '[%s]未选择单价文件，请重新选择...\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        text1.update()
        print(messagebox.showinfo(title='message', message='未找到单价文件，请重新选择。'))
        return
    text1.insert(0.0, '[%s]程序开始运行，正在寻找坐标点...\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    text1.update()
    a = pyautogui.locateOnScreen('1.png')
    if a is None:
        text1.insert(0.0, '[%s]未找到定位图片...\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        text1.update()
        print(messagebox.showinfo(title='message', message='未找到定位图片'))
        return
    else:
        text1.insert(0.0, '[%s]找到定位图片%s...\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(a)))
        text1.update()
    b = pyautogui.center(a)
    text1.insert(0.0,
                 '[%s]找到定位图片中心点坐标%s，鼠标移动到坐标点...\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(b)))
    text1.update()
    pyautogui.moveTo(b, duration=2, tween=pyautogui.easeInOutQuad)
    pyautogui.moveRel(80, 25, duration=2, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    pyautogui.scroll(-99999999)
    if filename == '':
        text1.insert(0.0, '[%s]未找到单价文件，请重新选择...\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        text1.update()
        print(messagebox.showinfo(title='message', message='未找到单价文件，请重新选择。'))
        return
    else:
        start = time.perf_counter()
        basename = os.path.basename(filename)
        text1.insert(0.0, '[%s]读取单价文件%s...\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), basename))
        text1.update()
        with open(filename) as f:
            list = f.readlines()
        text1.insert(0.0, '[%s]开始自动输入单价...\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        text1.update()
        for i in range(len(list)):
            pyautogui.typewrite(str(list[i].strip('\n')), interval=0.01)
            pyautogui.press('down')
        end = time.perf_counter()
        text1.insert(0.0,
                     '[%s]自动输入单价完成，用时%2f秒...\n' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), (end - start)))
        text1.update()
        print(messagebox.showinfo(title='message', message='自动输入单价完成，用时%s秒' % (end - start)))
        return


topFrame = Frame(root, bd=1, relief=SUNKEN)
topFrame.pack(fill=BOTH)

middleFrame = Frame(root, bd=1, relief=SUNKEN)
middleFrame.pack(fill=BOTH)

bottomFrame = Frame(root, bd=1, relief=SUNKEN)
bottomFrame.pack(fill=BOTH)

label = Label(topFrame, text="综合单价文件：")
label.grid(row=0, column=0, sticky=W)

v1 = StringVar()
e1 = Entry(topFrame, textvariable=v1)
e1.grid(row=0, column=1, sticky=W)

b1 = Button(topFrame, text="选择", command=openfile)
b1.grid(row=0, column=2, padx=5, sticky=W)

b3 = Button(topFrame, text="保存", command=savefile)
b3.grid(row=0, column=3, padx=5, sticky=W)

b4 = Button(topFrame, text="开始", command=inputprice)
b4.grid(row=0, column=4, padx=5, sticky=W)

# text = Text(bottomFrame, height=100)
# text.pack(fill=BOTH)
text = scrolledtext.ScrolledText(middleFrame, wrap=WORD)
text.pack(fill=BOTH)

text1 = scrolledtext.ScrolledText(middleFrame, height=6, wrap=WORD)
text1.pack(fill=BOTH)

root.mainloop()
