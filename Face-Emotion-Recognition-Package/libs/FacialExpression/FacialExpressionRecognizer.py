from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pickle


class FacialExpressionRecognizer:
    def __init__(self, kernel='linear', C=1):
        self.model = svm.SVC(kernel=kernel, C=C)
        self.pred = None

    def feed(self, data):
        pred = self.model.predict(data)
        self.pred = pred

    def train(self, data, label):
        self.model.fit(data, label)

    def test(self, data, label):
        pred = self.model.predict(data)
        con_mat = confusion_matrix(label, pred)

        rows = len(con_mat)
        cols = len(con_mat[0])

        total = 0
        TP = 0
        for i in range(rows):
            for j in range(cols):
                total += con_mat[i][j]

                if i == j:
                    TP += con_mat[i][j]

        accuracy = TP / total

        print("Accuracy: {}".format(accuracy))

    def getPrediction(self):
        return self.pred

    def draw_SVM(self, X, Y):
        # 샘플 데이터 표현
        plt.scatter(X[:, 0], X[:, 1], c=Y, s=30, cmap=plt.cm.Paired)
        # 초평면(Hyper-Plane) 표현
        ax = plt.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        xx = np.linspace(xlim[0], xlim[1], 30)
        yy = np.linspace(ylim[0], ylim[1], 30)
        YY, XX = np.meshgrid(yy, xx)
        xy = np.vstack([XX.ravel(), YY.ravel()]).T
        Z = self.model.decision_function(xy).reshape(XX.shape)
        ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
        # 지지벡터(Support Vector) 표현
        ax.scatter(self.model.support_vectors_[:, 0], self.model.support_vectors_[:, 1], s=60, facecolors='r')
        plt.show()

    def save(self, filename):
        with open(filename + '.pkl', 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.model = pickle.load(f)



