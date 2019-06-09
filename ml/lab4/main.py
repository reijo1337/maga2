import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

if __name__ == "__main__":
    dataset_test = pd.read_csv('dataset/fashion-mnist_test.csv')
    dataset_train = pd.read_csv('dataset/fashion-mnist_train.csv')
    # sc = StandardScaler()
    # dataset_test = sc.fit_transform(dataset_test)
    # dataset_train = sc.fit_transform(dataset_train)

    y_train = dataset_train.label
    X_train = dataset_train.drop(['label'], axis=1)

    y_test = dataset_test.label
    X_test = dataset_test.drop(['label'], axis=1)
    # X_test = dataset_test[:, 1:].values
    # y_test = dataset_test[:, 0].values

    classifier = MLPClassifier(activation='relu', solver='sgd', hidden_layer_sizes=(100, 10,), random_state=3)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print(f'precision_score {precision_score(y_test, y_pred, average="macro")}')
    print(f'recall_score {recall_score(y_test, y_pred, average="macro")}')
    print(f'f1_score {f1_score(y_test, y_pred, average="macro")}')
