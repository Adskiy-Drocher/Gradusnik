from tkinter import *
import tkinter.filedialog as td
from SQLite import engine, metadata, session, User
from Face_Pomni import Image_maker
from Trainner_script import Trainer
from Raspoznal import Recognizer
import os
import json

#Создания ока приложения Tkinter
window = Tk()
window.title('Утилита для работы с базой данных')
window.geometry('855x550')





#Здесь функции по созданию базы и архива, и перехода по страницам


def recognize():
    recognizer = Recognizer()
    for x in os.listdir('C:/Users/1/Pictures/archive/'):
        yml_path = 'C:/Users/1/Pictures/archive/' + str(x) + '/' + 'trainner.yml'
        recognizer.start(yml_path, str(x))



def choose_dir():
    global val_direct
    val_direct = td.askdirectory()
    data = {
        'dir_path': val_direct
    }
    direct.set(f"Папка: {val_direct}")
    with open('C:/Users/1/PycharmProjects/............./' + '/' + 'data', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def make_image():
    global val_direct
    y = session.query(User.id)[-1]
    maker = Image_maker()
    maker.take_image(user_id=y[0], path=val_direct)
    user_f_o.set('Пользователь не добавлен')
    name.set('')
    surname.set('')
    trainer = Trainer()
    path = val_direct + '/' + str(y[0])
    print(f'Путь {path}')
    print(f'Файлы папки юзера{os.listdir(path)}')
    trainer.getImagesAndLabels(path)

def create_user():
    user_name = name.get()
    user_surname = surname.get()
    user = User(name=user_name, surname=user_surname, health='True', image_path='None')
    session.add(user)
    session.commit()
    x = session.query(User.name, User.surname)[-1]
    user_f_o.set(f'Сделать фото для: {x[0]} {x[1]}')

def page3():
    global page1, page3, active_page
    font = ('Arial', 12, 'bold')
    base.config(font=font)
    for el in page1:
        el.pack_forget()
    btn_back.pack()
    for instance in session.query(User).all():
        base.insert(END, f'Ф.И: {instance.surname} {instance.name}; сост. здоровья: {instance.health}; Фото: {instance.image_path}')
    base.pack(side=LEFT, fill=Y)
    sb.pack(side=RIGHT, fill=Y)
    base.config(yscrollcommand=sb.set)
    sb.config(command=base.yview)
    active_page = page3

def page2():
    global page1, page2, active_page
    for el in page1:
        el.pack_forget()
    for el in page2:
        el.pack()
    btn_back.pack()
    active_page = page2




def page1_back():
    global active_page, page1
    for el in active_page:
        el.pack_forget()
    for el in page1:
        el.pack()
    btn_back.pack_forget()





#Какие-то переменные, не уверен нужны ли они теперь
val_direct = ''
filename = ''
user_name = ''
user_surname = ''
active_user_data = [filename, user_name, user_surname]
active_page = []

#Переменные, отвечающие за внешность интерфейса
font = ('Arial', 20, 'bold')
col1 = '#ccc'
col2 = '#555'

btn_back = Button(text='На главную', command=page1_back, font=font, fg=col1, bg=col2)

#Страница №1
btn1 = Button(text='Открыть базу данных', command=page3, font=font, fg=col1, bg=col2)
btn2 = Button(text='Добавить нового пользователя', command=page2, font=font, fg=col1, bg=col2)
btn_test = Button(text='Сделать фото с вебки', font=font, fg=col1, bg=col2, command=recognize)
page1 = [btn1, btn2, btn_test]

for el in page1:
    print(el)
    el.pack()

#Страница №2
user_f_o = StringVar()
name = StringVar()
surname = StringVar()
direct = StringVar()

direct.set('Папка не выбрана')
user_f_o.set('Пользователь не добавлен')

entry_name = Entry(text='имя', textvariable=name, font=font)
entry_surname = Entry(text='фамилия', textvariable=surname, font=font)

user_lab = Label(textvariable=user_f_o, font=font, pady=35)
dir_lab = Label(font=font, textvariable=direct, pady=10, wraplength=False, width=100000)

btn4 = Button(text='Сделать фото', fg=col1, bg=col2, font=font, command=make_image)
btn3 = Button(text='Добавить пользователя', font=font, fg=col1, bg=col2, command=create_user)
btn5 = Button(text='Выбрать папку', command=choose_dir, font=font, fg=col1, bg=col2)

page2 = [entry_name, entry_surname, btn3, user_lab,btn5, dir_lab, btn4]



#Страница №3
sb = Scrollbar(orient=VERTICAL)
base = Listbox(width=93)
page3 = [base]

#Отрисовка
window.mainloop()

