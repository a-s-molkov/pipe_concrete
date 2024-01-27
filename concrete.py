import pandas as pd
import numpy as np
import os


class Concrete:

    def __init__(self):
        self.df_c = None

    def download_df_concrete(self, path):
        self.df_c = pd.read_excel(os.path.abspath(path), header=1, decimal=',')
        self.df_c = self.df_c.replace('-', np.nan)

    # def concrete_resistance(self):
    #     """Возвращает массив уникальных видов сопротивления"""
    #     return self.df_c['Вид сопротивления'].unique()

    def concrete_type(self):
        """Возвращает список уникальных типов бетона"""
        return self.df_c['Бетон'].unique().tolist()

    def concrete_class(self):
        """Возвращает список классов бетона"""
        col = self.df_c.filter(regex='В[0-9]', axis=1).columns.values.tolist()
        return col

    def get_concrete(self, type_of_res, concr_type, concr_class):
        """Возвращает сопротивление выбранного бетона в кН/м2"""
        res_con = self.df_c.loc[
            (self.df_c['Вид сопротивления'] == type_of_res) & (self.df_c['Бетон'] == concr_type), concr_class].values[0]
        return res_con * 1000
