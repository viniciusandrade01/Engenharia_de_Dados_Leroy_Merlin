import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class GeneralCharts:
    def __init__(self):
        pass

    def createBoxChart(self, df: pd.DataFrame, column: str, size: list, title: str, colors: str):
    
        plt.figure(figsize=(size[0], size[1]))
        sns.boxplot(y=column, data=df, color=colors)
        plt.title(title)
        plt.show()