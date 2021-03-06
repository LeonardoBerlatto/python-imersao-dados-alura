# -*- coding: utf-8 -*-
"""aula_04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PFzTiYfxThWp4UosX85cx4SxzRnJrBpx

## Bibliotecas
"""

import pandas
import matplotlib.pyplot as plot
import seaborn as sns
import numpy

"""## Lendo os Dados"""

dataset = pandas.read_csv('https://raw.githubusercontent.com/alura-cursos/imersao-dados-2-2020/master/MICRODADOS_ENEM_2019_SAMPLE_43278.csv')

"""### Variáveis importantes"""

tests = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_MT', 'NU_NOTA_LC','NU_NOTA_REDACAO']

dataset['NU_NOTA_TOTAL'] = dataset[tests].sum(axis=1)

students_without_zero_score = dataset.query('NU_NOTA_TOTAL != 0')

"""## Insights da Aula

### Variáveis
"""

# Varíaveis funcionais ou independentes (x)
input_tests = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC','NU_NOTA_REDACAO']

# Varíavel dependente (y)
output_test = 'NU_NOTA_MT'

# Removendo notas NaN
students_without_zero_score = students_without_zero_score[tests].dropna()

input_scores = students_without_zero_score[input_tests]
output_score = students_without_zero_score[output_test]

input_scores, output_score

# Nomenclatura padrão
x = input_scores
y = output_score

from sklearn.model_selection import train_test_split

# Número aleatório para selecionar sempre os mesmos dados
SEED = 1313

x_train, x_test, y_train, y_test = train_test_split(x, 
                                                    y, 
                                                    test_size=0.25)


print(f"Notas no total: {len(x)} | Notas de treino: {len(x_train)} | Notas de teste: {len(x_test)}")

from sklearn.svm import LinearSVR

model = LinearSVR(random_state = SEED)

model.fit(x_train, y_train)

math_predictions = model.predict(x_test)

y_test[:5]

plot.figure(figsize=(10,10))

sns.scatterplot(x=math_predictions, y = y_test)
plot.title('Notas de Matemática pelas Notas de Matemática previstas')
plot.xlabel('Notas de Matemática Previstas')
plot.ylabel('Notas de Matemática')

plot.figure(figsize=(10,10))

sns.scatterplot(x=y_test, y = y_test - math_predictions)
plot.title('Diferença das Notas de Matemática pelas Notas de Matemática previstas')
plot.xlabel('Notas de Matemática Previstas')
plot.ylabel('Notas de Matemática')

plot.ylim((-50, 1050))
plot.xlim((-50, 1050))

results = pandas.DataFrame()
results['Real'] = y_test
results['Previsao'] = math_predictions
results['Diferenca'] = results['Real'] - results['Previsao']
results['Quadrado_Diferenca'] = (results['Real'] - results['Previsao'])**2

results['Quadrado_Diferenca'].mean()**(1/2)

from sklearn.dummy import DummyRegressor

dummy_model = DummyRegressor()
dummy_model.fit(x_train, y_train)

dummy_predictions = dummy_model.predict(x_test)

from sklearn.metrics import mean_squared_error

dummy_mean_error = mean_squared_error(y_test, dummy_predictions)
math_mean_error = mean_squared_error(y_test, math_predictions)

print(f'Erro médio "dummy": {dummy_mean_error} | Erro médio no modelo treinado: {math_mean_error}')