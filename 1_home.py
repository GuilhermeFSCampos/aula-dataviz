import streamlit as st
import plotly.express as px

from utils.data_utils import load_data, get_domestic_units, get_planted_area


st.set_page_config(layout="wide")
df = load_data()

def build_page():
    st.title("Cidades do Brasil")
    st.write('Fonte dos dados: https://www.kaggle.com/datasets/crisparada/brazilian-cities')
    col1, col2, col3, col4 = st.columns(4)

    total_pop = df['ESTIMATED_POP'].sum()
    total_area = df['AREA'].sum()

    total_companies = df['COMP_TOT'].sum()
    total_cities = df['CITY'].count()

    IDH_range = f'{df["IDHM"].min():.2f} - {df["IDHM"].max():.2f}'
    PIB_range = f'{df["GDP_CAPITA"].min():,.2f} - {df["GDP_CAPITA"].max():,.2f}'

    total_cars = df['Cars'].sum()
    total_motorcycles = df['Motorcycles'].sum()

    with col1:
        st.metric('População estimada total', f'{total_pop:,}')
        st.metric('Area total', f'{total_area:,} km²')

    with col2:
        st.metric('Empresas', f'{total_companies:,}')
        st.metric('Cidades', f'{total_cities:,}')

    with col3:
        st.metric('Range IDH', IDH_range)
        st.metric('Range PIB per capita', PIB_range)

    with col4:
        st.metric('Quantidade de carros', f'{total_cars:,}')
        st.metric('Quantidade de motos', f'{total_motorcycles:,}')

    graph_col1, graph_col2 = st.columns(2)

    with graph_col1:
        planted_area_hc = df['IBGE_PLANTED_AREA'].sum()
        df_areas = get_planted_area(total_area, planted_area_hc)
        fig = px.pie(df_areas,
                     title='Area plantada',
                     values='area',
                     names='tipo_area')
        st.plotly_chart(fig)

        fig_hist = px.histogram(df,
                                x='IDHM',
                                marginal='box',
                                color='region',
                                hover_data=['IDHM', 'CITY'])
        st.plotly_chart(fig_hist, use_container_width=True)

        df_idh = df.sort_values('IDHM', ascending=False)[['CITY', 'STATE', 'IDHM', 'IDHM Ranking 2010']].head(10)
        st.markdown('**10 Maiores IDHs**')
        st.dataframe(df_idh,
                     hide_index=True)

    with graph_col2:
        urban_res = df['IBGE_DU_URBAN'].sum()
        rural_res = df['IBGE_DU_RURAL'].sum()
        df_domestic_res = get_domestic_units(urban_res, rural_res)

        fig_homes = px.pie(df_domestic_res,
                           title='Quantidade de residencias (urbanas e rurais)',
                           values='qntd',
                           names='tipo_res')
        st.plotly_chart(fig_homes, use_container_width=True)

        fig_hist = px.histogram(df,
                                x='GDP_CAPITA',
                                color='region',
                                marginal='box')
        st.plotly_chart(fig_hist, use_container_width=True)
        df_gdp_capita = df.sort_values('GDP_CAPITA', ascending=False)[['CITY', 'STATE', 'GDP_CAPITA', 'GDP']].head(10)
        st.markdown('**10 Maiores PIB per capita**')
        st.dataframe(df_gdp_capita,
                     hide_index=True, )

build_page()