import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self):
        self.datas = {}
        self.result = None
        self.feature_fn = None
        self.threshold = None

    def compile(self, feature_fn):
        self.feature_fn = feature_fn

    def feed(self, x, y, name, threshold=None, contrast=False):

        # feature_fn 적용
        _y = []

        for y_data in y:
            _y.append(self.feature_fn(y_data))

        self.result = _y

        # display
        if x is not None:
            # plot 생성
            plt.subplot()
            # 기존 값과 대조
            if contrast:
                plt.plot(x, y, '.-', linewidth=1, color='black')
            # 데이터 plot
            plt.plot(x, _y, '.-', linewidth=1, color='b')
            # 옵션 설정
            plt.title(name)
            plt.grid(True, axis='y')
        else:
            # plot 생성
            plt.subplot()
            # 기존 값과 대조
            if contrast:
                plt.plot(y, '.-', linewidth=1, color='black')
            # 데이터 plot
            plt.plot(_y, '.-', linewidth=1, color='b')
            # 옵션 설정
            plt.title(name)
            plt.grid(True, axis='y')

        if threshold is not None:
            plt.axhline(threshold, 0, 1, linestyle='solid', color='green')

        plt.show()

        # if x is not None:
        #     if len(x) != len(y):
        #         print("Error :: x축과 y축의 데이터 수가 일치하지 않습니다.")
        #         return
        #
        #     ax.plot(x, y, '.-', linewidth=1)
        #
        # else:
        #     ax.plot(y, '.-', linewidth=1)
        #
        # self.plots[name] = ax

        # ax.show()

    def getResult(self):
        return self.result

    def appendData(self, name, value):

        if self.datas.get(name):
            print("Error :: 이미 같은 이름을 가진 데이터가 존재합니다.")
            return

        self.datas[name] = value

        print("SUCCESS :: 데이터 생성이 완료되었습니다. name={}".format(name))

    def plotDatas(self, names, type='scatter'):
        for name in names:
            if not self.datas.get(name):
                print("Error :: 해당 이름 - '{}'을 가진 데이터가 존재하지 않습니다.".format(name))
                return

            x = self.datas[name][0]
            y = self.datas[name][1]

            if type == 'scatter':
                plt.scatter(x, y, linewidth=1, label=name)
            elif type == 'line':
                plt.plot(x, y, '.-', linewidth=1, label=name)

        plt.legend()
        plt.show()

    def printDatas(self):
        keys = list(self.datas.keys())

        for idx, key in enumerate(keys):
            print("No.{} :: Name - {} ".format(idx, key))

    def getData(self, name):
        if not self.datas.get(name):
            print("Error :: 해당 이름 - '{}'을 가진 데이터가 존재하지 않습니다.".format(name))
            return

        return self.datas[name]

    def clearDatas(self):
        self.datas = {}









