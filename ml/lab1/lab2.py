import pandas as pd
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt

if __name__ == "__main__":
    DataFrame = pd.read_csv("dataset/mushrooms.csv")
    # DataFrame = DataFrame.apply(LabelEncoder().fit_transform)
    # labels = DataFrame.target_class.values
    # DataFrame.drop(["target_class"], axis=1, inplace=True)
    # features = DataFrame.values

    X = DataFrame.iloc[:, 1:].values
    y = DataFrame.iloc[:, 0].values

    for i in range(0, 22):
        labelencoder_X = LabelEncoder()
        X[:, i] = labelencoder_X.fit_transform(X[:, i])
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    onehotencoder = OneHotEncoder(categorical_features=[0, 1, 2, 4, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21])
    X = onehotencoder.fit_transform(X).toarray()

    cnt_clusters = 7

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # data = {'Completeness': [], 'V-measure': [], 'Silhouette':[], 'Homogenity':[]}
    data = {'precision_score': [], 'recall_score': [], 'f1_score': []}

    for i in range(2, cnt_clusters + 1):
        k_means = KMeans(n_clusters=i, random_state=0)
        k_means.fit(X_train, y_train)
        labels__ = k_means.predict(X_test)
        data['precision_score'].append(precision_score(y_test, labels__, average='weighted'))
        data['recall_score'].append(recall_score(y_test, labels__, average='micro'))
        data['f1_score'].append(f1_score(y_test, labels__, average='macro'))

    results = pd.DataFrame(data=data, index=range(2, cnt_clusters + 1))
    print(results)
    # dfgui.show(results)

    # inertia = []
    # for i in range(2, cnt_clusters + 1):
    #     kmeans = KMeans(n_clusters=i).fit(X_train)
    #     inertia.append(kmeans.inertia_)
    # plt.plot(range(2, cnt_clusters + 1), inertia, marker='o')
    # plt.xlabel("$clusters$")
    # plt.ylabel("$inertia$")
    # plt.grid(True, linestyle='-')
    # plt.show()

