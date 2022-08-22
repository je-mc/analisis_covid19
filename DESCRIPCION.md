# Análisis Covid-19 en USA

## Descripción
El CDC (Centro de Control y Prevención de Enfermedades) de EE. UU. es la entidad encargada de monitorear la salud pública y desarrollar estrategias para la prevención y control de enfermedades. Por esto ha contratado a nuestra consultora para organizar, con base en los datos recolectados, los recursos hospitalarios para prevenir que lo ocurrido durante la pandemia COVID-19 suceda de vuelta.
Análisis de dataset de COVID-19 proporcionado por el CDC (Centro de Control y Prevención de Enfermedades) de USA

![image](https://user-images.githubusercontent.com/103291440/185990533-97970c00-6920-4cdc-8ca2-df52656c0531.png)

Para el proyecto se utilizó Streamlit como herramienta de visualización, el dashboard cuenta un mapa interactivo en el que se puede observar el número de hospitalizados por estado y un ranking de los estados con mayor ocupación hospitalaria a lo largo de la pandemia.

Adicionalmente, es posible seleccionar un estado específico para revisar métricas importantes como la cantidad de camas UCI, el número de muertos durante la pandemia, etc.

Con la data obtenida se realiza el siguiente análisis:

## Estados con mayor ocupación hospitalaria por COVID durante los 6 primeros meses del 2020

![image](https://user-images.githubusercontent.com/103291440/185991752-038c6663-7317-44f4-9a4e-30d5ac74db90.png)

## Uno de los estados más afectados por la pandemia fue Nueva York por lo que se realiza un análisis de la ocupación de camas (Común) por COVID durante los 6 primeros meses de 2020 y se identifican los puntos críticos o de mayor crecimiento y decrecimiento en la ocupación de camas como se observa en la siguiente figura.

![image](https://user-images.githubusercontent.com/103291440/185992445-b005e08a-e429-4d67-8c3b-27605a0eabfe.png)

## Estados que más camas UCI -Unidades de Cuidados Intensivos- utilizaron durante el año 2020

![image](https://user-images.githubusercontent.com/103291440/185996367-ddd10135-671e-4e73-b688-aba9a7d12072.png)

## Cantidad de camas utilizadas, por Estado, para pacientes pediátricos con COVID durante el 2020

![image](https://user-images.githubusercontent.com/103291440/185994931-0f7251b9-dad4-42b2-903e-1ba96b71a607.png)

## Porcentaje de camas UCI corresponden a casos confirmados de COVID-19

![image](https://user-images.githubusercontent.com/103291440/185995106-a02e0b09-b8bf-45ea-9038-bf9468db746b.png)

## Cantidad de muertes por covid hubo, por Estado, durante el año 2021

![image](https://user-images.githubusercontent.com/103291440/185995714-9b51544b-276a-4bb7-97ae-29d982e01d78.png)

## Relación entre falta de personal médico con la cantidad de muertes por covid durante el año 2021

![image](https://user-images.githubusercontent.com/103291440/185995857-4fb54a6c-01de-4f88-bd83-ef11bc009a06.png)

Se observa que las curvas tienen una tendencia similar y presentan una relación directa, es decir si hay escasez de recursos médicos hay un aumento en las muertes por COVID-19.

## ¿Cuál fue el peor mes de la pandemia para USA en su conjunto?

![image](https://user-images.githubusercontent.com/103291440/185995999-8fbceb1d-8cd7-4d59-897e-875d12c8cd39.png)

![image](https://user-images.githubusercontent.com/103291440/185996040-169dcc5e-1fba-495a-9c55-7960574dbbc6.png)

## Las curvas de muertes por COVID-19 y de cantidad de unidades médicas que reportan escasez de recursos están altamente relacionadas, en este caso el mes con mayor cantidad de muertes reportadas fue en 01-2021 mientras que la cantidad de unidades médicas que reportaron escasez de recursos hospitalarios alcanzó su pico el mes anterior, 12-2020, por lo que se recomienda mejorar el equipamento de las unidades médicas y dotarlas de mayores y mejores recursos para evitar que aumente la cantidad de muertes por COVID-19.

Fuente: 'https://healthdata.gov/api/views/g62h-syeh/rows.csv?accessType=DOWNLOAD&api_foundry=true'
