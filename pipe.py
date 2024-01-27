import pandas as pd
import numpy as np
import os


class Pipe:

    def __init__(self):
        self.a_c = None
        self.a = None
        self.s = None
        self.d = None
        self.df_p = None

    def download_df_pipe(self, path):
        """Загружаем датафрейм"""
        self.df_p = pd.read_excel(os.path.abspath(path))

    def section_list(self):
        """Получаем список сечений"""
        return self.df_p['Сечение'].unique().tolist()

    def section(self, selected_pipe):
        """На вход - выбранное сечение. Получаем прочность трубы и площадь сечения бетона"""
        # внешний диаметр трубы переводим из мм в м
        self.d = self.df_p.loc[self.df_p['Сечение'] == selected_pipe, 'D, мм'].values[0] / 1000
        # площадь сечений трубы, переводим из см2 в м2
        self.a = self.df_p.loc[self.df_p['Сечение'] == selected_pipe, 'A, см2'].values[0] / 10000
        # площадь сечения бетона
        self.a_c = (np.pi * self.d ** 2) / 4 - self.a
        # 315 МПа (Ry)- сопротивление стали 09Г2С, переводим в кН/м2, получаем прочность в кН
        return self.a * 315 * 1000, self.a_c
