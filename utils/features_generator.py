import pandas as pd
from datetime import datetime
from typing import Tuple, Union, List


class FeatrueGenerator():

    @staticmethod
    def get_period_day(date: str) -> str:
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("4:59", '%H:%M').time()

        if (date_time > morning_min and date_time < morning_max):
            return 'mañana'
        elif (date_time > afternoon_min and date_time < afternoon_max):
            return 'tarde'
        elif (
            (date_time > evening_min and date_time < evening_max) or
            (date_time > night_min and date_time < night_max)
        ):
            return 'noche'

    @staticmethod
    def is_high_season(fecha: str) -> int:
        fecha_año = int(fecha.split('-')[0])
        fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        range1_min = datetime.strptime(
            '15-Dec', '%d-%b').replace(year=fecha_año)
        range1_max = datetime.strptime(
            '31-Dec', '%d-%b').replace(year=fecha_año)
        range2_min = datetime.strptime(
            '1-Jan', '%d-%b').replace(year=fecha_año)
        range2_max = datetime.strptime(
            '3-Mar', '%d-%b').replace(year=fecha_año)
        range3_min = datetime.strptime(
            '15-Jul', '%d-%b').replace(year=fecha_año)
        range3_max = datetime.strptime(
            '31-Jul', '%d-%b').replace(year=fecha_año)
        range4_min = datetime.strptime(
            '11-Sep', '%d-%b').replace(year=fecha_año)
        range4_max = datetime.strptime(
            '30-Sep', '%d-%b').replace(year=fecha_año)

        if ((fecha >= range1_min and fecha <= range1_max) or
            (fecha >= range2_min and fecha <= range2_max) or
            (fecha >= range3_min and fecha <= range3_max) or
                (fecha >= range4_min and fecha <= range4_max)):
            return 1
        else:
            return 0

    @staticmethod
    def get_min_diff(data: pd.DataFrame) -> float:
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff

    @staticmethod
    def get_important_fetures(data: pd.DataFrame) -> pd.DataFrame:
        top_10_features = [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

        # Create dummy variables for categorical columns
        opera_dummies = pd.get_dummies(data['OPERA'], prefix='OPERA')
        tipo_vuelo_dummies = pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO')
        mes_dummies = pd.get_dummies(data['MES'], prefix='MES')
        
        # Combine dummy variables
        features = pd.concat([opera_dummies, tipo_vuelo_dummies, mes_dummies], axis=1)
        
        # Ensure all expected columns are present and in the correct order
        features = features.reindex(columns=top_10_features, fill_value=0)
        
        return features