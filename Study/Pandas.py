import pandas as pd
from IPython.display import display

# Ler a planilha
df_Test = pd.read_excel(r'C:\Workspace1\TestePanda.xlsx', usecols= [0,1,2])
print (df_Test)
display(df_Test)

