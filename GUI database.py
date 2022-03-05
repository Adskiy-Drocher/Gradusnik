from tkinter import *
import tkinter.filedialog as td
from SQLite import engine, metadata, session, User
from Face_Pomni import Image_maker
from Trainner_script import Trainer
from Raspoznal import Recognizer
import os
import json
import shutil

#Создания ока приложения Tkinter
window = Tk()
window.title('Утилита для работы с базой данных')
window.geometry('855x550')





#Здесь функции по созданию базы и архива, и перехода по страницам
def delete():
    select = base.curselection()
    select_text = base.get(first=select)
    pupil = session.query(User, User.image_path).filter_by(id=select_text[0:3]).first()
    print(f'Ученик ------{pupil} {pupil[0]}')
    shutil.rmtree(pupil[1])
    session.delete(pupil[0])
    session.commit()
    base.delete(select)

def recognize():
    with open('data') as data_file:
        data = json.load(data_file)
    recognizer = Recognizer()
    print()
    for x in os.listdir(data["dir_path"]):
        yml_path = data["dir_path"] + '/' + str(x) + '/' + 'trainner.yml'
        print(data["dir_path"])
        print(f"путь yml {yml_path}")
        recognizer.start(yml_path, str(x))



def choose_dir():
    global val_direct
    val_direct = td.askdirectory()
    data = {
        'dir_path': val_direct
    }
    print(val_direct)
    direct.set(f"{val_direct}")
    with open(f'{os.getcwd()}/data', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    btn5.config(text='Изменить папку архива')


def create_user_make_im():
    if len(name.get()) == 0 or len(surname.get()) == 0:
        print(len(name.get()))
        print(len(surname.get()))
        user_f_o.set('Одно из полей/оба пусты!')
        print("""
        H
        """)
        return
    user_name = name.get()
    user_surname = surname.get()
    global val_direct
    maker = Image_maker()
    maker.take_image(len(session.query(User).all())+1, path=direct.get())
    user_f_o.set('Пользователь не добавлен')
    name.set('')
    surname.set('')
    trainer = Trainer()
    #print(session.query(User).all())
    path = direct.get() + '/' + str(len(session.query(User).all())+1)
    #print(f'Путь {path}')
    #print(f'Файлы папки юзера{os.listdir(path)}')
    trainer.getImagesAndLabels(path)
    user = User(name=user_name, surname=user_surname, health='True', image_path=path)
    session.add(user)
    base_lis.append(f'{user.id}  Ф.И: {user.surname} {instance.name}; сост. здоровья: {user.health}; Фото: {user.image_path}')
    session.commit()
    #x = session.query(User.name, User.surname)[-1]
    #user_f_o.set(f'Сделать фото для: {x[0]} {x[1]}')

def page3():
    global page1, page3, active_page, base_lis
    base.delete(1, 999)
    font = ('Arial', 12, 'bold')
    base.config(font=font)
    for el in page1:
        el.pack_forget()
    btn_back.pack()
    for el in base_lis:
        print(el)
        base.insert(END, el)
    for el in page3:
        if str(el) == '.!listbox':
            el.pack(side=LEFT, fill=Y)
        elif el == '.!scrollbar':
            el.pack(side=RIGHT, fill=Y)
        else:
            el.pack()
    #del_lab.pack()
    #del_btn.pack()
    #base.pack(side=LEFT, fill=Y)
    #sb.pack(side=RIGHT, fill=Y)
    base.config(yscrollcommand=sb.set)
    sb.config(command=base.yview)
    active_page = page3

def page2():
    with open('data') as data_file:
        data = json.load(data_file)
    global page1, page2, active_page
    if len(data["dir_path"]) > 0:
        direct.set(data["dir_path"])
        btn5.config(text='Изменить папку')
    elif len(data["dir_path"]) == 0:
        direct.set('Папка не выбрана')
        btn5.config(text='Выбрать окончательную папку')
    for el in page1:
        el.pack_forget()
    for el in page2:
        el.pack()
    btn_back.pack()
    active_page = page2

def pack_page1():
    with open('data') as data_file:
        data = json.load(data_file)
    for el in page1:
        print(el)
        el.pack()
    if len(data["dir_path"]) > 0:
        ras_str.set(f'Папка распознования {data["dir_path"]}')
    elif len(data["dir_path"]) == 0:
        ras_str.set('Вы еще ничего не добавляли в базу данных')

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
base_lis = []

#Переменные, отвечающие за внешность интерфейса
font = ('Arial', 20, 'bold')
col1 = '#ccc'
col2 = '#555'

btn_back = Button(text='На главную', command=page1_back, font=font, fg=col1, bg=col2)

#Страница №1
ras_str = StringVar()
ras_lab = Label(textvariable=ras_str, font=font)
btn1 = Button(text='Открыть базу данных', command=page3, font=font, fg=col1, bg=col2)
btn2 = Button(text='Добавить нового пользователя', command=page2, font=font, fg=col1, bg=col2)
btn_test = Button(text='Сделать фото с вебки', font=font, fg=col1, bg=col2, command=recognize)
page1 = [btn1, btn2, ras_lab, btn_test]


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

btn4 = Button(text='Сделать фото', fg=col1, bg=col2, font=font, command=create_user_make_im)
#btn3 = Button(text='Добавить пользователя', font=font, fg=col1, bg=col2, command=create_user)
btn5 = Button(text='Выбрать окончательную папку для архива', command=choose_dir, font=font, fg=col1, bg=col2)

page2 = [entry_name, entry_surname, user_lab,btn5, dir_lab, btn4]



#Страница №3
del_btn = Button(text='Удалить ученика', font=font, fg=col1, bg=col2, command=delete)
sb = Scrollbar(orient=VERTICAL)
base = Listbox(width=93)
del_lab = Label(text='Потом доделаю', font=font)
page3 = [del_lab, del_btn, base, sb]

#Отрисовка
for instance in session.query(User).all():
    base_lis.append(
        f'{instance.id}  Ф.И: {instance.surname} {instance.name}; сост. здоровья: {instance.health}; Фото: {instance.image_path}')
#print(base_lis)
pack_page1()
window.mainloop()



#biba  200 strok