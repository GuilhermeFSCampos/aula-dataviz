import streamlit as st
import pydeck as pdk
import plotly.express as px

from utils.map_utils import get_view_port_details
from utils.data_utils import load_data, get_planted_area, get_domestic_units


_DEFAULT_COLOR = '[200, 30, 0, 160]'
_DEFAULT_RADIUS = 100
_DEFAULT_MIN_RADIUS_PIXEL = 4

df = load_data()
state = st.sidebar.selectbox('Selecione o Estado',sorted(df['STATE'].unique()), index=12)
city = df[(df['STATE'] == state) & (df['CAPITAL'] == 1)]['CITY'].values[0]
cities = df[df['STATE'] == state]['CITY'].unique()
default_index = cities.tolist().index(city)
city = st.sidebar.selectbox('Selecione a cidade', cities, index=default_index)


def build_map(df_data, color, radius, radius_min_pixels):
    zoom, center_lat, center_lon = get_view_port_details(df_data, 'LAT', 'LONG')

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_data,
                get_position='[LONG, LAT]',
                get_color=color,
                get_radius=radius,
                radius_min_pixels=radius_min_pixels,
                pickable=True,
                auto_highlight=True
            )
        ],
        tooltip={
            'text': '{CITY}-{STATE}\n '
                    'População estimada: {ESTIMATED_POP}\n'
                    'Area: {AREA} km²\n'
                    'PIB: {GDP}\n'
                    'IDH: {IDHM}\n'
                    'Categoria Turismo: {CATEGORIA_TUR}'
        }
    ))

def build_cities():
    st.title('Cidades no Brasil')

    #st.map(df, latitude='LAT', longitude='LONG')


    color_map = {
        '0': [73, 144, 194, 160],
        'A': [167, 99, 151, 160],
        'B': [218, 57, 55, 160],
        'C': [255, 131, 23, 160],
        'D': [144, 84, 66, 160],
        'E': [43, 157, 50, 160]
    }
    df['color'] = df.CITY.apply(lambda x: [200, 30, 0, 255] if x == city else [73, 144, 194, 160])
    df['radius'] = df.CITY.apply(lambda x: _DEFAULT_RADIUS * 20 if x == city else _DEFAULT_RADIUS)
    df['tourism_color'] = df.CATEGORIA_TUR.map(color_map)

    #with st.expander('Dados do Brasil'):
    #   st.dataframe(df)

    option = st.selectbox('Qual visualização?',
                          ('Distribuição de cidades',
                           'Distribuição da população',
                           'Categorias de turismo'),
                          index=0)

    color = 'color'#_DEFAULT_COLOR
    radius_min_pixels = _DEFAULT_MIN_RADIUS_PIXEL
    radius = 'radius'#_DEFAULT_RADIUS

    if option == 'Categorias de turismo':
        color = 'tourism_color'

    if option == 'Distribuição da população':
        radius_min_pixels = 1
        radius = 'estimated_pop_size'
        color = '[73, 144, 194]'

    build_map(df, color, radius, radius_min_pixels)

def build_city_detail():
    st.subheader('Detalhe da cidade')
    city_row = df[df['CITY'] == city]
    city_str = f'{city} - {state}'

    with st.expander('Detalhes'):
        st.dataframe(city_row)

    st.header(city_str)

    selected_city_pop = city_row['ESTIMATED_POP'].values[0]
    selected_city_area = city_row['AREA'].values[0]

    selected_city_companies = city_row['COMP_TOT'].values[0]
    selected_city_idhm = city_row['IDHM'].values[0]

    selected_city_gdp = city_row['GDP'].values[0]
    selected_city_gdp_capita = city_row['GDP_CAPITA'].values[0]

    selected_city_cars = city_row['Cars'].values[0]
    selected_city_motorcycles = city_row['Motorcycles'].values[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(f'População - {city_str}', f'{selected_city_pop:,}')
        st.metric(f'Area - {city_str}', f'{selected_city_area:,.2f} km²')

    with col2:
        st.metric(f'Empreas - {city_str}', f'{selected_city_companies:,}')
        st.metric(f'IDHM - {city_str}', f'{selected_city_idhm:.3f}')

    with col3:
        st.metric(f'PIB (x1000) - {city_str}', f'{selected_city_gdp:,.2f}')
        st.metric(f'PIB per capita - {city_str}', f'{selected_city_gdp_capita:,.2f}')

    with col4:
        st.metric(f'Carros - {city_str}', f'{selected_city_cars:,}')
        st.metric(f'Motorcycles - {city_str}', f'{selected_city_motorcycles:,}')

    graph_col1, graph_col2 = st.columns(2)

    full_area_km2 = city_row['AREA'].values[0]
    planted_area_hc = city_row['IBGE_PLANTED_AREA'].values[0]
    df_areas = get_planted_area(full_area_km2, planted_area_hc)

    fig_area = px.pie(df_areas,
                      title='Porcentagem de area plantada',
                      values='area',
                      names='tipo_area')
    graph_col1.plotly_chart(fig_area, use_container_width=True)

    urban_res = city_row['IBGE_DU_URBAN'].values[0]
    rural_res = city_row['IBGE_DU_RURAL'].values[0]
    df_domestic_res = get_domestic_units(urban_res, rural_res)

    fig_homes = px.pie(df_domestic_res,
                       title='Quantidade de residencias (urbanas e rurais)',
                       values='qntd',
                       names='tipo_res')
    graph_col2.plotly_chart(fig_homes, use_container_width=True)


build_cities()
build_city_detail()