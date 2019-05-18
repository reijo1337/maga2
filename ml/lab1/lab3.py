import pandas as pd
from sklearn import decomposition
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

if __name__ == "__main__":
    DataFrame = pd.read_csv("dataset/mushrooms.csv")
    target_names = DataFrame.target_class.values
    DataFrame = DataFrame.apply(LabelEncoder().fit_transform)
    y = DataFrame.target_class.values
    DataFrame.drop(["target_class"], axis=1, inplace=True)
    X = DataFrame.values
    pca = decomposition.PCA(n_components=5)
    X = pca.fit(X).transform(X)
    for ii in range(5):
        for j in range(ii+1, 5):
            plt.figure()
            colors = ['navy', 'turquoise', 'black', 'yellow', 'red']
            lw = 2

            for color, i, target_name in zip(colors, [0, 1], target_names):
                plt.scatter(X[y == i, ii], X[y == i, j], color=color, alpha=.8, lw=lw,
                            label=target_name)
            plt.legend(loc='best', shadow=False, scatterpoints=1)
            plt.title(f'PCA of MUSHROOMS dataset {ii} {j}')
            plt.savefig(f'mushrooms_{ii}_{j}')
            plt.show()