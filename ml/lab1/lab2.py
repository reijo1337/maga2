import pandas as pd
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

if __name__ == "__main__":
    DataFrame = pd.read_csv("dataset/mushrooms.csv")
    DataFrame = DataFrame.apply(LabelEncoder().fit_transform)
    labels = DataFrame.target_class.values
    DataFrame.drop(["target_class"], axis=1, inplace=True)
    features = DataFrame.values
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # features_scaled = scaler.fit_transform(features)

    cnt_clusters = 20

    # data = {'Completeness': [], 'V-measure': [], 'Silhouette':[], 'Homogenity':[]}
    data = {'Silhouette': [], 'Accuracy': [], 'Completeness': []}

    for i in range(2, cnt_clusters + 1):
        k_means = KMeans(n_clusters=i)
        k_means.fit(features)
        data['Silhouette'].append(metrics.silhouette_score(features, k_means.labels_))
        data['Accuracy'].append(metrics.accuracy_score(labels, k_means.labels_))
        data['Completeness'].append(metrics.completeness_score(labels, k_means.labels_))

    results = pd.DataFrame(data=data, index=range(2, cnt_clusters + 1))
    print(results)
    # dfgui.show(results)

    inertia = []
    for i in range(2, cnt_clusters + 1):
        kmeans = KMeans(n_clusters=i).fit(features)
        inertia.append(kmeans.inertia_)
    plt.plot(range(2, cnt_clusters + 1), inertia, marker='o')
    plt.xlabel("$clusters$")
    plt.ylabel("$inertia$")
    plt.grid(True, linestyle='-')
    plt.show()

