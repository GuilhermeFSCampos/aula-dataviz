import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns

from utils.data_utils import load_data

df = load_data()

def build_page():
    cities_count = df.groupby(['STATE'])['CITY'].nunique().sort_index()
    state_pop = df.groupby(['STATE'])['ESTIMATED_POP'].sum()
    perc_state_pop = round(((state_pop / state_pop.sum()) * 100), 2).sort_index()

    trace1 = go.Bar(
        x=cities_count.index, name='Cidades',
        y=cities_count.values, showlegend=False
    )

    trace2 = go.Scatter(
        x=perc_state_pop.index,
        y=perc_state_pop.values, yaxis='y2',
        name='%Population', opacity=0.6,
        marker=dict(
            color='black',
            line=dict(color='#000000',
                      width=2)
        )
    )

    layout = dict(title=f'Quantidades de cidades em cada Estado e a % de população por Estado',
                  xaxis=dict(),
                  yaxis=dict(title='Quantidade de cidades'),
                  yaxis2=dict(range=[0, 40],
                              overlaying='y',
                              anchor='x',
                              side='right',
                              zeroline=False,
                              showgrid=False,
                              title='% da população total'
                              ))

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Empresas nos Estados')

    col1, col2 = st.columns(2)
    total_companies = df.groupby(['STATE'])['COMP_TOT'].sum()
    fig = px.bar(total_companies,
                 y='COMP_TOT',
                 labels={'COMP_TOT': 'Empresas',
                         'STATE': 'Estado'},
                 title='Empresas por Estado')
    col1.plotly_chart(fig, use_container_width=True)

    companies = ['COMP_A', 'COMP_B', 'COMP_C', 'COMP_D', 'COMP_E', 'COMP_F',
                 'COMP_G', 'COMP_H', 'COMP_I', 'COMP_J', 'COMP_K', 'COMP_L',
                 'COMP_M', 'COMP_N', 'COMP_O', 'COMP_P', 'COMP_Q', 'COMP_R',
                 'COMP_S', 'COMP_T', 'COMP_U']
    for col in companies:
        df[f'%_{col}'] = df[col] / df['COMP_TOT']

    comp_ratio = ['%_COMP_A', '%_COMP_B', '%_COMP_C', '%_COMP_D', '%_COMP_E',
                  '%_COMP_F', '%_COMP_G', '%_COMP_H', '%_COMP_I', '%_COMP_J',
                  '%_COMP_K', '%_COMP_L', '%_COMP_M', '%_COMP_N', '%_COMP_O',
                  '%_COMP_P', '%_COMP_Q', '%_COMP_R', '%_COMP_S', '%_COMP_T',
                  '%_COMP_U', 'STATE']

    companies_perc = df[comp_ratio].groupby('STATE').mean() * 100
    fig = px.bar(companies_perc,
                 barmode='stack',
                 title='Porcentagem por setor')
    col2.plotly_chart(fig, use_container_width=True)

    st.subheader('Turismo nos Estados')

    tur_col1, tur_col2 = st.columns(2)
    df_tourism = df[df.CATEGORIA_TUR!='0']
    total_touristic_regions = df_tourism.groupby(['STATE'])['REGIAO_TUR'].nunique()
    fig = px.bar(total_touristic_regions,
                 y='REGIAO_TUR',
                 hover_data=['REGIAO_TUR'],
                 labels={'REGIAO_TUR': 'regiões turisticas',
                         'STATE': 'Estado'},
                 title='Total de regiões turisticas por Estado',
                 )
    tur_col1.plotly_chart(fig, use_container_width=True)

    perc_cat_touristic_regions = pd.crosstab(df_tourism['STATE'], df_tourism['CATEGORIA_TUR'], normalize='index')*100
    fig = px.bar(perc_cat_touristic_regions,
                 barmode='stack',
                 labels={
                     'CATEGORIA_TUR': 'Categoria',
                     'STATE': 'Estado',
                     'value': '% do total'
                 },
                 title='% do tipo de turismo por Estado'
                 )
    tur_col2.plotly_chart(fig, use_container_width=True)

    pop = ['IBGE_1', 'IBGE_1-4', 'IBGE_5-9', 'IBGE_10-14', 'IBGE_15-59', 'IBGE_60+']
    for col in pop:
        df[f'perc_{col}'] = df[col] / df['IBGE_POP']
    age_ranges = ['STATE', 'perc_IBGE_1', 'perc_IBGE_1-4', 'perc_IBGE_5-9',
                  'perc_IBGE_10-14', 'perc_IBGE_15-59', 'perc_IBGE_60+']
    mean_age_ranges = df[age_ranges].groupby('STATE').mean() * 100
    fig = px.bar(mean_age_ranges,
                 title='Média do range de idade por Estado')
    st.plotly_chart(fig, use_container_width=True)

    selected_state = st.selectbox('Selecione um Estado', sorted(df.STATE.unique()), index=12)
    st.title(selected_state)
    df_state = df[df['STATE'] == selected_state]
    selected_state_pop = df_state['ESTIMATED_POP'].sum()
    selected_state_area = df_state['AREA'].sum()
    selected_state_companies = df_state['COMP_TOT'].sum()
    selected_state_cities = cities_count[selected_state]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f'População do estado - {selected_state}', f'{selected_state_pop:,}')
    col2.metric(f'Area - {selected_state}', f'{selected_state_area:,.2f} km²')
    col3.metric(f'Empreas - {selected_state}', f'{selected_state_companies:,}')
    col4.metric(f'Quantidade de cidades - {selected_state}', selected_state_cities)

    st.title(f'Distribuições de IDH e PIB per capita - {selected_state}')

    graph_col1, graph_col2 = st.columns(2)

    with graph_col1:
        plot = sns.displot(df_state['IDHM'],
                           kde=True)
        st.pyplot(plot.fig)

        fig_hist = px.histogram(df_state,
                                x='IDHM',
                                marginal='box',
                                hover_data=['IDHM', 'CITY'])
        st.plotly_chart(fig_hist, use_container_width=True)

        df_idh = df_state.sort_values('IDHM', ascending=False)[['CITY', 'IDHM', 'IDHM Ranking 2010']].head(10)
        st.markdown('**10 Maiores IDHs**')
        st.dataframe(df_idh,
                     hide_index=True,)

    with graph_col2:
        plot = sns.displot(df_state['GDP_CAPITA'],
                           kde=True)
        st.pyplot(plot.fig)

        fig_hist = px.histogram(df_state,
                                x='GDP_CAPITA',
                                marginal='box')
        st.plotly_chart(fig_hist, use_container_width=True)
        df_gdp_capita = df_state.sort_values('GDP_CAPITA', ascending=False)[['CITY', 'GDP_CAPITA', 'GDP']].head(10)
        st.markdown('**10 Maiores PIB per capita**')
        st.dataframe(df_gdp_capita,
                     hide_index=True,)



    #hist_data  = [df_state['IDHM'].values]
    #group_labels = ['IDHM']
    #fig_distplot = ff.create_distplot(hist_data,
    #                          group_labels=group_labels,
    #                          show_rug=False)
    #fig_distplot.data[0].autobinx = True
    #st.plotly_chart(fig_distplot, use_container_width=True)




build_page()