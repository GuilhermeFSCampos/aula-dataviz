import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df_full = pd.read_csv('data/BRAZIL_CITIES_REV2022.CSV')
    df_full = df_full[df_full.LAT!=0]
    df_full = df_full[df_full.AREA > 0]
    df_full['population_density'] = df_full['ESTIMATED_POP'] / df_full['AREA']
    df_full['estimated_pop_size'] = ((df_full['ESTIMATED_POP'] - df_full['ESTIMATED_POP'].min()) / df_full['ESTIMATED_POP'].max()) * 500000
    df_full['region'] = df_full['STATE'].apply(lambda x: map_region(x))
    return df_full


def get_planted_area(full_area_km2, planted_area_hc):
    planted_area_km2 = planted_area_hc / 100
    non_planted_area = abs(full_area_km2 - planted_area_km2)
    area_dict = {0: ['não plantada', non_planted_area],
                 1: ['plantada', planted_area_km2]}
    df_areas = pd.DataFrame.from_dict(area_dict, orient='index', columns=['tipo_area', 'area'])
    return df_areas


def get_domestic_units(urban, rural):
    domestic_units = {0: ['Urbana', urban],
                      1: ['Rural', rural]}
    df_domestic_units = pd.DataFrame.from_dict(domestic_units, orient='index', columns=['tipo_res', 'qntd'])
    return df_domestic_units


def map_region(state):
    centro_oeste = ['GO', 'MT', 'MS', 'DF']
    if state in centro_oeste:
        return 'Centro Oeste'
    sul = ['RS', 'PR', 'SC']
    if state in sul:
        return 'Sul'
    sudeste = ['SP', 'MG', 'RJ', 'ES']
    if state in sudeste:
        return 'Sudeste'
    norte = ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO']
    if state in norte:
        return 'Norte'
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    if state in nordeste:
        return 'Nordeste'
