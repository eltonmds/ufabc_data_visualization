# qual e o número total de estudantes (sum) por estado norte-americano que utilizaram a modalidade de ensino presencial (in person), remoto, ou hibrido
# Cria DF para melhorar o tratamento de dados pelo tableau
import pandas as pd

df = pd.read_csv('School_Learning_Modalities__2021-2022.csv')
df.head()
filtered_df = df[['State', 'Student Count', 'Learning Modality']]
grouped_df = filtered_df.groupby(['State', 'Learning Modality'], as_index = True)['Student Count'].sum().unstack(-1)
grouped_df
grouped_df.to_csv('School_learning.csv')
