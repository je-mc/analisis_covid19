import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime as dt
from datetime import datetime
import matplotlib.dates as mdates
from PIL import Image

st.set_page_config(layout="wide")


df = pd.read_csv('COVID-19_Dataset.csv')
df = df.fillna(0)

def main_page():
    st.markdown("# PROYECTO INDIVIDUAL II")
    st.subheader('Descripción')
    st.write('#### El CDC (Centro de Control y Prevención de Enfermedades) de EE. UU. es la entidad encargada de monitorear la salud pública y desarrollar estrategias para la prevención y control de enfermedades. Por esto ha contratado a nuestra consultora para organizar, con base en los datos recolectados, los recursos hospitalarios para prevenir que lo ocurrido durante la pandemia COVID-19 suceda de vuelta.')
    st.write('\n\n\n')
    image = Image.open('cdc.jpg')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(image,caption='Logo Centro para el Control y Prevención de Enfermedades')

    with col3:
        st.write(' ')

    
    st.sidebar.markdown("# Presentación")

def page2():

    st.title('COVID-19 Facts')
    col1, col2 = st.columns(2)

    with col1:
        # Un mapa que muestre la cantidad de hospitalizados debido al COVID-19 por Estado.
        df1 = pd.DataFrame(df, columns = ['state',
                                        'total_pediatric_patients_hospitalized_confirmed_covid',
                                        'total_adult_patients_hospitalized_confirmed_covid'])
        df1['Total'] = df1['total_pediatric_patients_hospitalized_confirmed_covid'] + df1['total_adult_patients_hospitalized_confirmed_covid']
        df1 = df1.groupby(by='state',as_index=False).sum()
        fig = px.choropleth(df1,
                        locations= 'state', 
                        locationmode="USA-states", 
                        scope="usa",
                        color= 'Total',
                        color_continuous_scale="hot_r", 
                        labels={'locations':'Estado','color':'Total Hospitalizados'}
                        )
        fig.update_layout(
                        title_text = 'Numero de hospitalizados por COVID-19 por estado en USA',
                        geo_scope='usa'
                        )

        st.plotly_chart(fig)

    with col2:
        
        # Ranking de Estados con mayor ocupación hospitalaria por COVID

        df1 = pd.DataFrame(df, columns = ['state',
                                        'hospital_onset_covid_coverage'])
        df1 = df1.groupby(by='state',as_index=False).sum().set_index('state').sort_values(by="hospital_onset_covid_coverage",ascending=False).astype(int).iloc[0:15]
        
        fig = plt.figure(figsize=(6, 3))
        ax = fig.add_axes([0,0,1,1])
        x=df1.index.values.astype(str)
        y=df1['hospital_onset_covid_coverage']
        ax.bar(x,y)
        ax.set_xlabel('Estados')
        ax.set_ylabel('Reportes')
        ax.set_title('Ranking de Estados con mayor ocupación hospitalaria por COVID-19')
        ax.tick_params(axis='x',rotation=45)
        st.write(fig)

    

    # Uso de camas UCI por Estado.

    filter = st.selectbox("Selecciona un estado", np.sort(pd.unique(df["state"])))

    col1, col2, col3 = st.columns(3)

    with col1:
        df1 = pd.DataFrame(df, columns = ['state',
                                    'staffed_adult_icu_bed_occupancy',
                                    'staffed_pediatric_icu_bed_occupancy'])
        df1['Total'] = df1['staffed_adult_icu_bed_occupancy'] + df1['staffed_pediatric_icu_bed_occupancy']
        df1 = df1.groupby(by='state',as_index=False).sum().reset_index()
        df1 = df1.rename(columns={'staffed_adult_icu_bed_occupancy':'UCI Adultos','staffed_pediatric_icu_bed_occupancy':'UCI Pediátricos'})
        a = df1[df1["state"] == filter]
        st.metric(label="Camas UCI Adultos", value=a['UCI Adultos'].astype(int))
        st.metric(label="Camas UCI Pediátricos", value=a['UCI Pediátricos'].astype(int))
        st.metric(label="Total Camas UCI", value=a['Total'].astype(int))

    with col2:
        df1 = pd.DataFrame(df, columns = ['state',
                                            'staffed_icu_pediatric_patients_confirmed_covid',
                                            'staffed_icu_adult_patients_confirmed_covid'])
        df1['Total_camas_uci_covid_ocupadas'] = df1['staffed_icu_pediatric_patients_confirmed_covid'] + df1['staffed_icu_adult_patients_confirmed_covid']
        df1 = df1.groupby(by='state',as_index=False).sum().reset_index()
        a = df1[df1["state"] == filter]
        st.metric(label="Camas UCI COVID-19 Adultos", value=a['staffed_icu_adult_patients_confirmed_covid'].astype(int))
        st.metric(label="Camas UCI COVID-19 Pediátricos", value=a['staffed_icu_pediatric_patients_confirmed_covid'].astype(int) )
        st.metric(label="Total Camas UCI COVID-19", value=a['Total_camas_uci_covid_ocupadas'].astype(int))

    with col3:

        df1 = pd.DataFrame(df, columns = ['state',
                                        'critical_staffing_shortage_today_yes'])
        df1 = df1.groupby(by='state',as_index=False).sum().reset_index()
        a = df1[df1["state"] == filter]
        st.metric(label="Reportes por falta de recursos hospitalarios", value=a['critical_staffing_shortage_today_yes'].astype(int))

        df1 = pd.DataFrame(df, columns = ['state',
                                    'deaths_covid'])
        df1 = df1.groupby(by='state',as_index=False).sum().reset_index()
        a = df1[df1["state"] == filter]
        st.metric(label="Muertes por COVID-19", value=a['deaths_covid'].astype(int))

    st.write('Cantidad de camas ocupadas por COVID-19 entre dos fechas')

    # Cantidad de camas ocupadas por COVID-19 entre dos fechas elegidas por el usuario.
    fecha = pd.to_datetime(df['date'], infer_datetime_format=True)
    today = datetime.date(fecha.min())
    tomorrow = today + dt.timedelta(days=1)
    start_date = st.date_input('Inicio', today)
    end_date = st.date_input('Fin', tomorrow)
    if st.button('Consultar'): 
        if start_date < end_date and start_date >= today:
            df1 = df[(df['date'] >= start_date.isoformat()) & (df['date'] <= end_date.isoformat())]
            df1 = pd.DataFrame(df1, columns = ['staffed_pediatric_icu_bed_occupancy',
                                                                        'staffed_adult_icu_bed_occupancy',
                                                                        'staffed_icu_pediatric_patients_confirmed_covid',
                                                                        'staffed_icu_adult_patients_confirmed_covid'])
            df1['Total_camas_uci_ocupadas'] = df1['staffed_pediatric_icu_bed_occupancy'] + df1['staffed_adult_icu_bed_occupancy']
            df1['Total_camas_uci_covid_ocupadas'] = df1['staffed_icu_pediatric_patients_confirmed_covid'] + df1['staffed_icu_adult_patients_confirmed_covid']
            total_camas_uci = int(df1['Total_camas_uci_ocupadas'].sum())
            total_camas_uci_covid = int(df1['Total_camas_uci_covid_ocupadas'].sum())

            st.metric(label="CAMAS UCI OCUPADAS", value=total_camas_uci)
            st.metric(label="CAMAS UCI OCUPADAS POR COVID-19", value=total_camas_uci_covid)
        else:
            st.error('Ingrese fechas a partir del 2020-01-01')



def page3():
    st.sidebar.markdown("# Cuestionario - Pregunta 1")
    st.subheader('¿Cuáles fueron los 5 Estados con mayor ocupación hospitalaria por COVID? Criterio de ocupación por cama común. Considere la cantidad de camas ocupadas con pacientes confirmados y tome como referencia los 6 primeros meses del 2020 - recuerde incluir la cifra de infectados en esos meses (acumulativo).')
    df1 = df[df['date'] < '2020/07/01'].sort_values('date')
    df1 = pd.DataFrame(df1, columns = ['state',
                                    'inpatient_beds_used_covid',
                                    'total_adult_patients_hospitalized_confirmed_covid',
                                    'total_pediatric_patients_hospitalized_confirmed_covid'])
    total = df1['inpatient_beds_used_covid'].sum()
    df1 = df1.groupby(by='state',as_index=False).sum().set_index('state').sort_values(by="inpatient_beds_used_covid",ascending=False).iloc[0:5].astype(int)
    df1 = df1.rename(columns={'inpatient_beds_used_covid':'Camas COVID','total_adult_patients_hospitalized_confirmed_covid':'COVID Adultos','total_pediatric_patients_hospitalized_confirmed_covid':'COVID Pediátricos'})
    df1['Porcentaje Total'] = (100*df1['Camas COVID']/total).astype(int)
    st.dataframe(df1)

    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("#### Mapa")
        fig = px.choropleth(df1,
                    locations= df1.index, 
                    locationmode="USA-states", 
                    scope="usa",
                    color= 'Camas COVID',
                    color_continuous_scale="hot_r", 
                    labels={'locations':'Estado','color':'Ocupación hospitalaria'}
                    )
        fig.update_layout(
                    title_text = 'Estados con mayor ocupación hospitalaria',
                    geo_scope='usa'
                    )

        st.plotly_chart(fig)
    
    with fig_col2:
        st.markdown("#### Gráfico de barras")
        fig = plt.figure(figsize=(6, 3))
        ax = fig.add_axes([0,0,1,1])
        x=df1.index.values.astype(str)
        y=df1['Camas COVID']
        ax.bar(x,y)
        ax.set_xlabel('Estados')
        ax.set_ylabel('Camas Ocupadas')
        ax.set_title('Ocupación de camas COVID por estado')
        st.write(fig)


def page4():
    st.sidebar.markdown("# Cuestionario - Pregunta 2")
    st.subheader('Analice la ocupación de camas (Común) por COVID en el Estado de Nueva York durante la cuarentena establecida.')
    
    df2 = df[(df['state'] == 'NY') & (df['date'] < '2020/07/01')].sort_values('date')
    df2 = pd.DataFrame(df2, columns = ['state',
                                        'date',
                                        'inpatient_beds_used_covid'])
    var = df2['inpatient_beds_used_covid'] / df2['inpatient_beds_used_covid'].shift(1) - 1  # variacion diaria
    df2['variacion'] = np.around(var,2)
    df2 = df2.fillna(0)

    x = df2.date.values
    y1 = df2.inpatient_beds_used_covid.values
    y2 = df2.variacion.values

    max_val = df2[df2['variacion'] == df2['variacion'].max()]
    min_val = df2[df2['variacion'] == df2['variacion'].min()]
    

    fig, ax = plt.subplots(2, figsize=(15, 5), sharex='col', sharey='row')
    ax[0].plot(x, y1)
    ax[0].set(ylabel='Camas',
        title='Ocupación de camas por COVID-19')
    ax[1].plot(x, y2)
    ax[1].scatter(max_val['date'].values,max_val['variacion'].values,color='r')
    ax[1].scatter(min_val['date'].values,min_val['variacion'].values,color='r')

    ax[1].set(xlabel='Fecha', ylabel='Variación',
        title='Variación porcentiual de ocupación de camas por COVID-19')

    ax[1].xaxis.set_major_locator(mdates.AutoDateLocator())
    ax[1].tick_params(axis='x', labelrotation=45)
    st.write(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
        fecha = max_val.date.values.tolist()
        porcentaje = max_val.variacion.values.tolist()
        st.markdown('Datos punto máximo')
        st.metric(label="Fecha", value= fecha[0])
        st.metric(label="Variación", value= porcentaje[0])
  

    with col2:
        st.markdown('Datos punto mínimmo')
        fecha = min_val.date.values.tolist()
        porcentaje = min_val.variacion.values.tolist()
        st.metric(label="Fecha", value= fecha[0])
        st.metric(label="Variación", value= porcentaje[0])

    with col3:

        a = df2[df2['inpatient_beds_used_covid'] == df2['inpatient_beds_used_covid'].max()].reset_index().drop(columns=['state','index'])
        a = a.rename(columns={'date':'Fecha','inpatient_beds_used_covid':'Camas COVID','variacion':'Variación Diaria'})
        fecha = a.Fecha.values.tolist()
        st.markdown('Punto de mayor ocupación en términos absolutos')
        st.metric(label="Fecha", value= fecha[0])
        st.metric(label="Variación", value= a['Variación Diaria'].values)
        st.metric(label="Camas COVID", value= a['Camas COVID'].values.astype(int))




def page5():
    st.sidebar.markdown("# Cuestionario - Pregunta 3")
    st.subheader('¿Cuáles fueron los cinco Estados que más camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020?')
    df3 = df[df['date'] < '2021/01/01'].sort_values('date')
    df3 = pd.DataFrame(df3, columns = ['state',
                                        'staffed_adult_icu_bed_occupancy',
                                        'staffed_pediatric_icu_bed_occupancy'])
    df3['Total'] = df3['staffed_adult_icu_bed_occupancy'] + df3['staffed_pediatric_icu_bed_occupancy']
    df3 = df3.groupby(by='state',as_index=False).sum().set_index('state').sort_values(by="Total",ascending=False).iloc[0:5].astype(int)
    df3 = df3.rename(columns={'staffed_adult_icu_bed_occupancy':'Ocupación Adultos','staffed_pediatric_icu_bed_occupancy':'Ocupación Pediátricos'})

    st.dataframe(df3)




    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("#### Mapa")
        fig = px.choropleth(df3,
                    locations= df3.index, 
                    locationmode="USA-states", 
                    scope="usa",
                    color= 'Total',
                    color_continuous_scale="hot_r", 
                    labels={'locations':'Estado','color':'Ocupación UCI'}
                    )
        fig.update_layout(
                    title_text = 'Estados con mayor ocupación de camas UCI',
                    geo_scope='usa'
                    )
        st.plotly_chart(fig)
    
    with fig_col2:
        st.markdown("#### Gráfico de barras")
        fig = plt.figure(figsize=(6, 3))
        ax = fig.add_axes([0,0,1,1])
        x=df3.index.values.astype(str)
        y=df3['Total'].astype(int)
        ax.bar(x,y)
        ax.set_xlabel('Estados')
        ax.set_ylabel('Ocupación de camas UCI')
        ax.set_title('Estados con mayor ocupación de camas UCI')
        st.write(fig)


def page6():
    st.sidebar.markdown("# Cuestionario - Pregunta 4")
    st.subheader('¿Qué cantidad de camas se utilizaron, por Estado, para pacientes pediátricos con COVID durante el 2020?')

    col1, col2, col3 = st.columns(3)

    with col1:
        df4 = df[df['date'] < '2021/01/01'].sort_values('date')
        df4 = pd.DataFrame(df4, columns = ['state',
                                        'total_pediatric_patients_hospitalized_confirmed_covid',
                                        'staffed_icu_pediatric_patients_confirmed_covid'])

        df4 = df4.groupby(by='state',as_index=False).sum().set_index('state').sort_values(by="total_pediatric_patients_hospitalized_confirmed_covid",ascending=False).astype(int)
        df4 = df4.rename(columns={'total_pediatric_patients_hospitalized_confirmed_covid':'Ocupación Pediátricos','staffed_icu_pediatric_patients_confirmed_covid':'Ocupación UCI Pediátricos'})
        
        st.dataframe(df4)

    with col2:
        fig = px.choropleth(df4,
                    locations= df4.index, 
                    locationmode="USA-states", 
                    scope="usa",
                    color= 'Ocupación Pediátricos',
                    color_continuous_scale="hot_r", 
                    labels={'locations':'Estado','color':'Ocupación Pediátricos'}
                    )
        fig.update_layout(
                    title_text = 'Estados con mayor ocupación para pacientes pediátricos',
                    geo_scope='usa'
                    )

        st.plotly_chart(fig)
    
    with col3:
        st.write(' ')
    

def page7():
    st.sidebar.markdown("# Cuestionario - Pregunta 5")
    st.subheader('¿Qué porcentaje de camas UCI corresponden a casos confirmados de COVID-19?')


    col1, col2, col3 = st.columns(3)

    with col1:
        df5 = pd.DataFrame(df, columns = ['state',
                                            'staffed_pediatric_icu_bed_occupancy',
                                            'staffed_adult_icu_bed_occupancy',
                                            'staffed_icu_pediatric_patients_confirmed_covid',
                                            'staffed_icu_adult_patients_confirmed_covid'])
        df5['Total_camas_uci_ocupadas'] = df5['staffed_pediatric_icu_bed_occupancy'] + df5['staffed_adult_icu_bed_occupancy']
        df5['Total_camas_uci_covid_ocupadas'] = df5['staffed_icu_pediatric_patients_confirmed_covid'] + df5['staffed_icu_adult_patients_confirmed_covid']
        df5 = df5.groupby(by='state').sum().reset_index()
        df5 = pd.DataFrame(df5, columns = ['state',
                                        'Total_camas_uci_ocupadas',
                                        'Total_camas_uci_covid_ocupadas'])
        df5['Porcentaje'] = (100*df5['Total_camas_uci_covid_ocupadas'] / df5['Total_camas_uci_ocupadas']).astype(int)
        df5 = df5.set_index('state')
        df5 = df5.rename(columns={'Total_camas_uci_ocupadas':'Total UCI','Total_camas_uci_covid_ocupadas':'Total UCI COVID'})
        df5 = df5.sort_values(by="Porcentaje",ascending=False)
        st.dataframe(df5)


    with col2:
        fig = px.choropleth(df5,
                    locations= df5.index, 
                    locationmode="USA-states", 
                    scope="usa",
                    color= 'Porcentaje',
                    color_continuous_scale="hot_r", 
                    labels={'locations':'Estado','color':'Porcentaje'}
                    )
        fig.update_layout(
                        title_text = 'Porcentaje camas UCI por estado',
                        geo_scope='usa'
                        )

        st.plotly_chart(fig)
        
    
    with col3:

        st.write(' ')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        total_uci = df5['Total UCI'].sum()
        total_uci_covid = df5['Total UCI COVID'].sum()
        porcentaje = round(100*total_uci_covid/total_uci,2)
        st.metric(label="Porcentaje Ocupación UCI COVID-19", value=porcentaje)
    
    with col3:
        st.write(' ')


        
        


def page8():
    st.sidebar.markdown("# Cuestionario - Pregunta 6")
    st.subheader('¿Cuántas muertes por covid hubo, por Estado, durante el año 2021?')

    col1, col2, col3 = st.columns(3)

    with col1:
        df6 = df[(df['date'] > '2020/12/31') & (df['date'] < '2022/01/01')].sort_values('date')
        df6 = pd.DataFrame(df6, columns = ['state',
                                            'deaths_covid'])
        df6 = df6.groupby(by='state',as_index=False).sum().set_index('state').sort_values(by="deaths_covid",ascending=False).astype(int)
        df6 = df6.rename(columns={'deaths_covid':'Muertes COVID'})
        st.dataframe(df6)

    with col2:
        fig = px.choropleth(df6,
                        locations= df6.index, 
                        locationmode="USA-states", 
                        scope="usa",
                        color= 'Muertes COVID',
                        color_continuous_scale="hot_r", 
                        labels={'locations':'Estado','color':'Muertes'},
                        )
        fig.update_layout(
                            title_text = 'Muertes por COVID-19 en 2021 por estado',
                            geo_scope='usa', 
                            )

        st.plotly_chart(fig)
        
    with col3:
        st.write(' ')

def page9():
    st.sidebar.markdown("# Cuestionario - Pregunta 7")
    st.subheader('¿Qué relación presenta la falta de personal médico, con la cantidad de muertes por covid durante el año 2021?')

    df7 = df[(df['date'] > '2020/12/31') & (df['date'] < '2022/01/01')].sort_values('date')
    df7 = pd.DataFrame(df7, columns = ['date',
                                    'deaths_covid',
                                    'critical_staffing_shortage_today_yes'])

    df7 = df7.groupby(by='date', as_index=False).sum()
    x1 = df7.deaths_covid.values
    x2 = df7.critical_staffing_shortage_today_yes.values
    y = df7.date.values
    fig, ax = plt.subplots(2, figsize=(15, 5),
            sharex='col', sharey='row')
    ax[0].plot(y, x1)
    ax[0].set(ylabel='Muertes',
        title='Muertes por COVID-19 2021')
    ax[1].plot(y, x2)
    ax[1].set(xlabel='Fecha', ylabel='Hospitales',
        title='Hospitales con recursos insuficientes')
    ax[1].xaxis.set_major_locator(mdates.AutoDateLocator())
    ax[1].tick_params(axis='x', labelrotation=45)
    st.pyplot(fig)

    st.write('#### Se observa que las curvas tienen una tendencia similar y presentan una relación directa, es decir si hay escasez de recursos médicos hay un aumento en las muertes por COVID-19.')


def page10():
    st.sidebar.markdown("# Cuestionario - Pregunta 8")
    st.subheader('Siguiendo las respuestas anteriores, ¿cuál fue el peor mes de la pandemia para USA en su conjunto?')

    df8 = pd.DataFrame(df, columns = ['date',
                                    'deaths_covid',
                                    'critical_staffing_shortage_today_yes']).sort_values('date')
    df8['month_year'] = pd.to_datetime(df8['date']).dt.to_period('M')
    df8 = df8.groupby(by='month_year', as_index=False).sum()
    
    x1 = df8.deaths_covid.values
    x2 = df8.critical_staffing_shortage_today_yes.values
    y = df8['month_year'].astype(str)

    fig, ax = plt.subplots(2, figsize=(15, 5),
            sharex='col', sharey='row')
    ax[0].plot(y, x1)
    ax[0].set(ylabel='Muertes',
        title='Muertes por COVID-19 2021')
    ax[1].plot(y, x2)
    ax[1].set(xlabel='Fecha', ylabel='Hospitales',
        title='Hospitales con recursos insuficientes')
    ax[1].tick_params(axis='x', labelrotation=45)

    st.pyplot(fig)



    col1, col2 = st.columns(2)

    with col1:
        df8['month_year'] = df8['month_year'].astype(str)
        df8 = df8.rename(columns={'deaths_covid':'Muertes COVID','critical_staffing_shortage_today_yes':'Reportes de Hospitales','month_year':'Periodo'})
        a = df8.sort_values(by="Muertes COVID",ascending=False).set_index('Periodo').iloc[0:1]
        st.dataframe(a)

        b = df8.sort_values(by="Reportes de Hospitales",ascending=False).set_index('Periodo').iloc[0:1]
        st.dataframe(b)

    with col2:
        st.write('#### La cantidad de muertes por COVID-19 está relacionada con los recursos médicos disponibles, en este caso el peor momento de la pandemia por cantidad de muertes por COVID-19 fue en Enero de 2021 y se observa que Diciembre de 2020 fue el mes con mayor cantidad de reportes por falta de recursos hospitalarios.')
    
    

    


def page11():
    st.sidebar.markdown("# Cuestionario - Pregunta 9")
    st.subheader('¿Qué recomendaciones haría, ex post, con respecto a los recursos hospitalarios y su uso?')

    st.write('#### Las curvas de muertes por COVID-19 y de cantidad de unidades médicas que reportan escasez de recursos están altamente relacionadas, en este caso el mes con mayor cantidad de muertes reportadas fue en 01-2021 mientras que la cantidad de unidades médicas que reportaron escasez de recursos hospitalarios alcanzó su pico el mes anterior, 12-2020, por lo que se recomienda mejorar el equipamento de las unidades médicas y dotarlas de mayores y mejores recursos para evitar que aumente la cantidad de muertes por COVID-19.')

page_names_to_funcs = {
    "Presentación": main_page,
    "Dashboard": page2,
    "Cuestionario - Pregunta 1": page3,
    "Cuestionario - Pregunta 2": page4,
    "Cuestionario - Pregunta 3": page5,
    "Cuestionario - Pregunta 4": page6,
    "Cuestionario - Pregunta 5": page7,
    "Cuestionario - Pregunta 6": page8,
    "Cuestionario - Pregunta 7": page9,
    "Cuestionario - Pregunta 8": page10,
    "Cuestionario - Pregunta 9": page11,
}

selected_page = st.sidebar.selectbox("Selecciona una página", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()