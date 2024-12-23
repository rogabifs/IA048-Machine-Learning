# -*- coding: utf-8 -*-
"""ProjetoIA048.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14iMMF9p4Vam9RGu7m8SDsSbwTNNu-wHC
"""

pip install yellowbrick

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
from matplotlib import style
import warnings
warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import random

# Carregamento dos dados e suas informações
wine_df = pd.read_csv('winequality-red.csv')

from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler()
values= scaler.fit_transform(wine_df)
wine_df= pd.DataFrame(values,columns=["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality"])
wine_df.head()

# Geracao o heatmap das correlações entre as colunas do DataFrame wine_df
plt.figure(figsize=(10,7))
sns.heatmap(wine_df.corr(), annot=True)
plt.title('Correlation between the columns')
plt.show()

# Visualizacao do Elbow Method) e determinacao o número ótimo de clusters para o algoritmo KMeans.
from yellowbrick.cluster import KElbowVisualizer
model = KMeans()
visualizer = KElbowVisualizer(model, k=(1, 10), timings = False)
visualizer.fit(wine_df)
visualizer.show()

kmeans= KMeans(n_clusters=4)
wine_matrix= wine_df.values
label= kmeans.fit_predict(wine_matrix)
unique_labels= np.unique(label)


num_plots = 4  # Número de gráficos de dispersão a serem gerados
num_attributes = 12  # Número total de atributos
random.seed(42)  # Definir semente aleatória para reprodução

plt.figure(figsize=(16, 10))  # Tamanho da figura ajustável

for plot_idx in range(num_plots):
    # Escolher aleatoriamente dois índices de atributos diferentes
    attr1, attr2 = random.sample(range(num_attributes), 2)

    plt.subplot(2, 2, plot_idx + 1)

    for i in unique_labels:
        plt.scatter(wine_matrix[label==i, attr1], wine_matrix[label==i, attr2], label=f'Cluster {i}')

    plt.xlabel(f'{wine_df.columns[attr1]}')
    plt.ylabel(f'{wine_df.columns[attr2]}')
    plt.title(f'Scatter Plot: {wine_df.columns[attr1]} vs {wine_df.columns[attr2]}')
    plt.legend()

plt.tight_layout()
plt.show()

# Adicionar 'label' como uma coluna ao DataFrame
wine_df['label'] = label

# Plotar boxplots para cada atributo por cluster
plt.figure(figsize=(7, 10))
for i, col in enumerate(wine_df.columns[:-1]):  # Excluir a coluna 'label' da iteração
    plt.subplot(6, 2, i + 1)  # 4 linhas, 3 colunas, posição atual
    sns.boxplot(x='label', y=col, data=wine_df)
    plt.title(f'{col} por Cluster')
    plt.xlabel('Cluster')
    plt.ylabel(col)
plt.tight_layout()
plt.show()

wine_df = wine_df.drop(labels=['label'], axis=1)

# Determinacao do numero ótimo de clusters por meio do Silhouette Method
for i in range(2,10):
  kmeans = KMeans(n_clusters=i, max_iter=100)
  kmeans.fit(wine_df)
  score = silhouette_score(wine_df, kmeans.labels_)
  print("For cluster: {}, the silhouette score is {} ".format(i, score))

# Analise grafica do Silhouette Method
silhouette_coeficients = []
for i in range(2,10):
  kmeans = KMeans(n_clusters=i, max_iter=100)
  kmeans.fit(wine_df)
  score = silhouette_score(wine_df, kmeans.labels_)
  silhouette_coeficients.append(score)

plt.plot(range(2,10), silhouette_coeficients)
plt.xticks(range(2, 10))
plt.xlabel("Number of clustters")
plt.ylabel("Silhouette coefficient")

pca= PCA()
X= pca.fit_transform(wine_df)
print(sum(pca.explained_variance_[0:9])/sum(pca.explained_variance_))
pca_df = pd.DataFrame(X)

plt.figure(figsize=(10,7))
sns.heatmap(pca_df.corr())
plt.title('Correlation between the columns')
plt.show()

# Obter os autovalores
autovalores = pca.explained_variance_

# Obter os autovetores
autovetores = pca.components_

# Criar um DataFrame para os autovetores (component loadings)
loading_matrix = pd.DataFrame(autovetores, columns=wine_df.columns)

# Exibir os autovalores
print("Autovalores (variância explicada por cada componente):")
print(autovalores)

# Exibir a matriz de carga (component loadings)
print("\nMatriz de Carga (Component Loadings):")
print(loading_matrix)

# Identificar as colunas com maior contribuição para cada componente principal
# Selecionando as colunas com os maiores valores absolutos nos autovetores
for i in range(len(autovalores)):
    loading_vector = loading_matrix.iloc[i]
    top_columns = loading_vector.abs().nlargest(3).index  # Top 3 colunas com maior contribuição
    print(f"\nComponente Principal {i+1} (Autovalor: {autovalores[i]}):")
    print(top_columns)

# Determinacao do numero ótimo de clusters por meio do Silhouette Method
for i in range(2,10):
  kmeans = KMeans(n_clusters=i, max_iter=100)
  kmeans.fit(pca_df)
  score = silhouette_score(pca_df, kmeans.labels_)
  print("For cluster: {}, the silhouette score is {} ".format(i, score))

# Analise grafica do Silhouette Method
silhouette_coeficients = []
for i in range(2,10):
  kmeans = KMeans(n_clusters=i, max_iter=100)
  kmeans.fit(pca_df)
  score = silhouette_score(pca_df, kmeans.labels_)
  silhouette_coeficients.append(score)

plt.plot(range(2,10), silhouette_coeficients)
plt.xticks(range(2, 10))
plt.xlabel("Number of clustters")
plt.ylabel("Silhouette coefficient")

from yellowbrick.cluster import KElbowVisualizer
model = KMeans()
visualizer = KElbowVisualizer(model, k=(1, 10), timings = False)
visualizer.fit(pca_df[0:9])
visualizer.show()

kmeans= KMeans(n_clusters=3)
label= kmeans.fit_predict(X)
unique_labels= np.unique(label)

for i in unique_labels:
  plt.scatter(X[label==i,0],X[label==i,1],label=i)

plt.legend()
plt.title("wine groups")

num_plots = 6  # Número de gráficos de dispersão a serem gerados
num_attributes = 9  # Número total de atributos


plt.figure(figsize=(10, 8))  # Tamanho da figura ajustável

for plot_idx in range(num_plots):
    # Escolher aleatoriamente dois índices de atributos diferentes
    attr1, attr2 = random.sample(range(2,num_attributes), 2)

    plt.subplot(3, 2, plot_idx + 1)

    for i in unique_labels:
        plt.scatter(X[label==i, attr1], X[label==i, attr2], label=f'Cluster {i}')

    plt.xlabel(f'Atributo {attr1}')
    plt.ylabel(f'Atributo {attr2}')
    plt.title(f'Scatter Plot: Atributo {attr1} vs Atributo {attr2}')
    plt.legend()

plt.tight_layout()
plt.show()

# Adicionar 'label' como uma coluna ao DataFrame
pca_df['label'] = label

# Plotar boxplots para cada atributo por cluster
plt.figure(figsize=(8, 8))
for i, col in enumerate(pca_df.columns[:9]):  # Excluir a coluna 'label' da iteração
    plt.subplot(5, 2, i + 1)  # 4 linhas, 3 colunas, posição atual
    sns.boxplot(x='label', y=col, data=pca_df)
    plt.title(f'{col} por Cluster')
    plt.xlabel('Cluster')
    plt.ylabel(col)
plt.tight_layout()
plt.show()

pca_df = pca_df.drop(labels=['label'], axis=1)