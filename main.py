import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from concrete import *
from pipe import *


class App(tk.Tk):
    def __init__(self, concrete, pipe):
        super().__init__()
        self.coef = None
        self.type_of_res = None
        self.selected_pipe = None
        self.concr_class = None
        self.concr_type = None
        self.eff = None
        self.concrete = concrete
        self.pipe = pipe
        self.title("Расчет трубобетона")  # название окна

        frm = ttk.Frame(self, padding=15)  # создает "рамку" с отступом от элементов в нужное кол-во единиц
        frm.grid()  # инициализация сетки

        ttk.Label(frm, text="Внимание! Расчёт ведётся для стали 09Г2С \n и только для сжатых элементов",
                  foreground='#ff0000', justify='center').grid(columnspan=3, row=0, pady=5)

        ttk.Label(frm, text="Продольное усилие", width=20).grid(column=0, row=1, sticky='w', pady=5)
        ttk.Label(frm, text="Тип бетона", width=20).grid(column=0, row=2, sticky='w', pady=5)
        ttk.Label(frm, text="Класс бетона", width=20).grid(column=0, row=3, sticky='w', pady=5)
        ttk.Label(frm, text="Сечение трубы", width=20).grid(column=0, row=4, sticky='w', pady=5)
        ttk.Label(frm, text="Результат:", width=20, font='Arial 10 bold').grid(column=0, row=6, sticky='e', pady=10)
        self.result_lbl = ttk.Label(frm, text="", width=20)
        self.result_lbl.grid(column=1, row=6, sticky='w', pady=5)

        # ввод продольного усилия
        self.effort = ttk.Entry(frm, width=23)
        self.effort.grid(column=1, row=1, sticky='w', pady=5)
        ttk.Label(frm, text="кН", width=5).grid(column=2, row=1, pady=5)

        # пока делаем только на сжатие, этот фрагмент мб позже пригодится
        # if pd.to_numeric(self.effort.get()) < 0:
        #     self.type_of_resistance = 'Сжатие осевое (призменная прочность)'
        # else:
        #     self.type_of_resistance = 'Растяжение осевое'
        self.type_of_resistance = 'Сжатие осевое (призменная прочность)'

        # ввод типа бетона
        self.combo_type = ttk.Combobox(frm, width=20, values=concrete.concrete_type())
        self.combo_type.grid(column=1, row=2, sticky='w', pady=5)
        self.combo_type.current(0)

        # ввод класса бетона
        self.combo_class = ttk.Combobox(frm, width=20, values=concrete.concrete_class())
        self.combo_class.grid(column=1, row=3, sticky='w', pady=5)
        self.combo_class.current(10)

        # ввод сечения трубы
        self.combo_pipe = ttk.Combobox(frm, width=20, values=pipe.section_list())
        self.combo_pipe.grid(column=1, row=4, sticky='w', pady=5)
        self.combo_pipe.current(0)

        # кнопка расчета
        calculation = ttk.Button(frm, text="Вычислить", command=self.calc)  # ДОБАВИТЬ КОМАНДУ !!!!!!!!!
        calculation.grid(column=0, row=7, pady=5)

        # кнопка выхода
        ttk.Button(frm, text="Выход", command=self.destroy).grid(column=1, row=7, pady=5)

    def calc(self):
        self.eff = self.effort.get()
        self.type_of_res = self.type_of_resistance  # в будущем можно поменять под combobox или что-то другое
        self.concr_type = self.combo_type.get()
        self.concr_class = self.combo_class.get()
        self.selected_pipe = self.combo_pipe.get()
        if len(self.eff) == 0:
            messagebox.showerror("Ошибка!", "Не введено усилие!")
        else:
            res_concrete = self.concrete.get_concrete(self.type_of_res, self.concr_type, self.concr_class)
            if np.isnan(res_concrete):
                messagebox.showerror("Ошибка!", "Такого бетона не существует! Выберите другой.")
            else:
                strength_pipe, square_concrete = self.pipe.section(self.selected_pipe)
                strength_concrete = res_concrete * square_concrete
                strength = strength_pipe + 2.5 * strength_concrete
                if pd.to_numeric(self.eff) == 0:
                    messagebox.showerror("Ошибка!", "Усилие должно быть не равным нулю!")
                else:
                    self.coef = pd.to_numeric(self.eff) / strength  # коэффициент запаса по прочности
                    if self.coef < 1:
                        self.result_lbl.config(text=f'{self.coef:.5f}', font='Arial 10 bold', background='#4dff4d')
                    else:
                        self.result_lbl.config(text=f'{self.coef:.5f}', font='Arial 10 bold', background='#ff3333')


if __name__ == "__main__":
    concretes = Concrete()
    concretes.download_df_concrete('data/concrete.xlsx')

    pipes = Pipe()
    pipes.download_df_pipe('data/gost_r_58064-2018.xlsx')

    app = App(concretes, pipes)
    app.mainloop()
