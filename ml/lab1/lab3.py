import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import matplotlib.pyplot as plt

if __name__ == "__main__":
    DataFrame = pd.read_csv("dataset/mushrooms.csv")
    target_names = DataFrame.target_class.values
    DataFrame = DataFrame.apply(LabelEncoder().fit_transform)
    y = DataFrame.target_class.values
    DataFrame.drop(["target_class"], axis=1, inplace=True)
    X = DataFrame.values
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # X = scaler.fit_transform(features)
    components = 5
    pca = decomposition.PCA(n_components=components)
    X = pca.fit(X).transform(X)
    colors = ['navy', 'turquoise', 'black', 'yellow', 'red']
    for ii in range(components):
        for j in range(ii+1, components):
            plt.figure()
            lw = 2

            for color, i, target_name in zip(colors, [0, 1], target_names):
                plt.scatter(X[y == i, ii], X[y == i, j], color=color, alpha=.8, lw=lw,
                            label=target_name)
            plt.legend(loc='best', shadow=False, scatterpoints=1)
            plt.title(f'PCA of MUSHROOMS dataset {ii} {j}')
            plt.show()
    # for ii in range(components):
    #     for jj in range(ii+1, components):
    #         for kk in range(jj+1, components):
    #             fig = plt.figure()
    #             plt.clf()
    #             ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    #
    #             plt.cla()
    #
    #             for name, label, color in [(target_names[0], 0, colors[0]), (target_names[1], 1, colors[0])]:
    #                 ax.text3D(X[y == label, ii].mean(),
    #                           X[y == label, jj].mean() + 1.5,
    #                           X[y == label, kk].mean(), name,
    #                           horizontalalignment='center',
    #                           bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))
    #             # Reorder the labels to have colors matching the cluster results
    #             y = np.choose(y, [1, 2, 0]).astype(np.int)
    #             # for color, i, target_name in zip(colors, [0, 1], target_names):
    #             #     plt.scatter(X[y == i, ii], X[y == i, jj], X[y == i, kk], color=color, alpha=.8, lw=lw,
    #             #                 label=target_name)
    #             ax.scatter(X[:, ii], X[:, jj], X[:, kk], c=y, cmap=plt.cm.nipy_spectral,
    #                        edgecolor='k')
    #
    #             ax.w_xaxis.set_ticklabels([])
    #             ax.w_yaxis.set_ticklabels([])
    #             ax.w_zaxis.set_ticklabels([])
    #             plt.title(f'PCA of MUSHROOMS dataset {ii} {jj} {kk}')
    #             plt.show()
