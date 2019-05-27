import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

if __name__ == "__main__":
    dataset = pd.read_csv('dataset/mushrooms.csv')
    X = dataset.iloc[:, 1:].values
    y = dataset.iloc[:, 0].values

    for i in range(0, 22):
        labelencoder_X = LabelEncoder()
        X[:, i] = labelencoder_X.fit_transform(X[:, i])
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    onehotencoder = OneHotEncoder(categorical_features=[0, 1, 2, 4, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21])
    X = onehotencoder.fit_transform(X).toarray()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # classifier = RandomForestClassifier(n_estimators=100, criterion='entropy')
    layer_sizes = [i for i in range(1, 11)]
    activations = ['relu', 'logistic']

    data = {'precision_score': [], 'recall_score': [], 'f1_score': []}
    indexes = []
    for a in activations:
        for size in layer_sizes:
            print(f'processing {a}_{size}')
            indexes.append(f'{a}_{size}')

            classifier = MLPClassifier(activation=a, solver='sgd', hidden_layer_sizes=(size,), max_iter=75, random_state=3)
            classifier.fit(X_train, y_train)

            y_pred = classifier.predict(X_test)

            cm = confusion_matrix(y_test, y_pred)

            data['precision_score'].append(precision_score(y_test, y_pred))
            data['recall_score'].append(recall_score(y_test, y_pred))
            data['f1_score'].append(f1_score(y_test, y_pred))

    results = pd.DataFrame(data=data, index=indexes)
    print(results)
