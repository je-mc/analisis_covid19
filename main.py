import sys
from streamlit import cli as stcli
import pandas as pd

def run():
    df = pd.read_csv('https://healthdata.gov/api/views/g62h-syeh/rows.csv?accessType=DOWNLOAD&api_foundry=true')
    df.to_csv('COVID-19_Dataset.csv')
    print('Data cargada correctamente')
    sys.argv = ["streamlit", "run", "PI_II.py"]
    sys.exit(stcli.main())

if __name__ == '__main__':
    run()
    