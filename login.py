import re
import tkinter
from re import search, split, fullmatch
from demo01weather import query_weather
import pymysql
from tkinter import *
from tkinter.messagebox import *
import test03weather

list1 = []
list2 = []

# 主窗口
window = Tk()
window.geometry('500x300')
window.title('登陆账号')


def create_window2():
    window2 = Tk()
    window2.geometry('500x300')
    window2.title('查询天气')

    # def insert_text(str):
    #     text_box.delete('1.0',tkinter.END)
    #     text_box.insert('0.0', insert_text(str))
    # def clear_text():
    #     text_box.delete('1.0', tkinter.END)

    def insert_text(str):
        text_box.delete('1.0', tkinter.END)
        text_box.insert('0.0', test03weather.insert_list(str))

    # Button(window2, text='查询当前所在城市的天气',
    #        command=lambda: clear_text and text_box.insert('0.0', test03weather.insert_list('北京'))).place(relx=0.1, relwidth=0.35)
    Button(window2, text='查询当前所城市的天气',
           command=lambda: insert_text('北京')).place(relx=0.1, relwidth=0.35)
    city1 = StringVar()
    Entry(window2, textvariable=city1).place(relx=0.1, rely=0.1, relwidth=0.35)
    # Button(window2, text='输入所要查询城市的天气',
    #        command=lambda: clear_text() and text_box.insert('0.0', test03weather.insert_list(city1.get()))).place(relx=0.1, rely=0.2,
    #                                                                                              relwidth=0.35)
    Button(window2, text='输入所要查询城市的天气',
           command=lambda: insert_text(city1.get())).place(relx=0.1, rely=0.2, relwidth=0.35)

    #
    # Button(window2,text='保存天气记录'
    #        command=lambda : insert_text())

    text_box = Text(window2, wrap=WORD)
    text_box.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.6)
    # text_box.insert('0.0', query_weather(city1.get()))
    window2.mainloop()


# 文字
Label(window, text='账号:').place(relx=0.1, rely=0.3, relwidth=0.3)
Label(window, text='密码:').place(relx=0.1, rely=0.4, relwidth=0.3)

username = StringVar()
password = StringVar()

# 输入框
Entry(window, textvariable=username).place(relx=0.35, rely=0.3, relwidth=0.3)
Entry(window, textvariable=password, show='*').place(relx=0.35, rely=0.4, relwidth=0.3)


def connect():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        db='login',
        charset='utf8'
    )
    return conn


def select():
    conn = connect()
    cur = conn.cursor()
    sql = 'select * from user;'
    cur.execute(sql)
    f = cur.fetchall()  # 结果集
    for i in f:
        list1.append(i[0])
        list2.append(i[1])
    return f


# 插入 注册时插入value1、value2
def insert(value1, value2):
    conn = connect()
    cur = conn.cursor()
    sql = 'insert into user(username,password) values (%s,%s);'
    cur.execute(sql, (value1, value2))
    conn.commit()  # 执行完插入后提交


def login():
    f = select()
    if (username.get(), password.get()) in f:
        showinfo('提示！', '登陆成功')
        window.destroy()
        create_window2()
        # window.destroy()

    elif username.get() not in list1 and password.get() not in list2:
        showerror('错误', '账号未注册，请前往注册')
    else:
        showerror('错误', '账号或密码错误')


def register_check():  # 处理用户账号新注册逻辑
    window.withdraw()

    register_window = Toplevel()

    register_window.title('注册')
    register_window.geometry('500x300')
    Label(register_window, text='账号:').place(relx=0.1, rely=0.3, relwidth=0.3)
    Label(register_window, text='密码:').place(relx=0.1, rely=0.4, relwidth=0.3)
    Label(register_window, text='确认密码:').place(relx=0.1, rely=0.5, relwidth=0.3)

    username1 = StringVar()
    password1 = StringVar()
    password2 = StringVar()

    # 输入框
    Entry(register_window, textvariable=username1).place(relx=0.35, rely=0.3, relwidth=0.3)
    Entry(register_window, textvariable=password1, show='*').place(relx=0.35, rely=0.4, relwidth=0.3)
    Entry(register_window, textvariable=password2, show='*').place(relx=0.35, rely=0.5, relwidth=0.3)

    def register():
        select()
        if username1.get() in list1:
            showerror('错误', '账号已注册，请返回登陆')
        elif username1.get() == '':
            showerror('错误', '账号不能为空')
        elif password1.get() == '':
            showerror('错误', '密码不能为空')
        elif password1.get() != '' and password2.get() != '' and password1.get() == password2.get():
            print(username1.get())
            insert(username1.get(), password1.get())
            showinfo('提示', '注册成功，请返回登陆')
        # window.deiconify()

    def re_login():
        window.deiconify()
        register_window.destroy()

    Button(register_window, text='注册', command=register).place(relx=0.45, rely=0.6)
    Button(register_window, text='返回', command=re_login).place(relx=0.55, rely=0.6)


# 登录和注册按钮
Button(window, text='登录', command=login).place(relx=0.25, rely=0.5, relwidth=0.2)
Button(window, text='注册', command=register_check).place(relx=0.5, rely=0.5, relwidth=0.2)

window.mainloop()
