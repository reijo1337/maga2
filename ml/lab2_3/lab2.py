from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def optimal_number_of_clusters(x):
    wcss = []
    for i in range(1, 11):
        km = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        km.fit(x)
        wcss.append(km.inertia_)

    plt.style.use('fivethirtyeight')
    plt.plot(range(1, 11), wcss)
    plt.title('The Elbow Method', fontsize=20)
    plt.xlabel('No. of Clusters')
    plt.ylabel('wcss')
    plt.show()


def clustering(x):
    km = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_means = km.fit_predict(x)

    plt.style.use('fivethirtyeight')
    plt.scatter(x[y_means == 0, 0], x[y_means == 0, 1], s=200, c='pink', label='miser')
    plt.scatter(x[y_means == 1, 0], x[y_means == 1, 1], s=200, c='yellow', label='general')
    plt.scatter(x[y_means == 2, 0], x[y_means == 2, 1], s=200, c='cyan', label='target')
    plt.scatter(x[y_means == 3, 0], x[y_means == 3, 1], s=200, c='magenta', label='spendthrift')
    plt.scatter(x[y_means == 4, 0], x[y_means == 4, 1], s=200, c='orange', label='careful')
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s=50, c='blue', label='centeroid')

    plt.title('K Means Clustering', fontsize=12)
    plt.xlabel('Annual Income')
    plt.ylabel('Spending Score')
    plt.legend()
    plt.show()


def lab2():
    data = pd.read_csv('dataset/mushrooms.csv')
    labels = data.target_class.values
    data.drop(['target_class'], axis=1, inplace=True)
    features = data.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    features_scaled = scaler.fit_transform(features)
    cnt_clusters = 10
    