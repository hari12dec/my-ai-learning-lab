import pandas as pd

class Univariate:
    def quanQual(self, dataset):
        quan = []
        qual = []

        for columnName in dataset.columns:
            if dataset[columnName].dtype == object:
                qual.append(columnName)
            else:
                quan.append(columnName)

        return quan, qual

    def frequency_table(self, dataset, columnName):
        
        freq = dataset[columnName].value_counts().sort_index()
        rel_freq = freq / len(dataset[columnName])
        cum_freq = freq.cumsum()

        table = pd.DataFrame({
            "Frequency": freq,
            "RelativeFrequency": rel_freq,
            "CumulativeFrequency": cum_freq
        })

        return table

    def descriptiveTable(self, dataset, quan):

        descriptive = pd.DataFrame(
            index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "Q4:100%",
                   "IQR", "1.5rule", "Lesser", "Greater", "Min", "Max",
                   "LowOutLier", "HighOutLier"],
            columns=quan
        )

        for columnName in quan:

            descriptive.loc["Mean", columnName] = dataset[columnName].mean()
            descriptive.loc["Median", columnName] = dataset[columnName].median()
            descriptive.loc["Mode", columnName] = dataset[columnName].mode()[0]

            descriptive.loc["Q1:25%", columnName] = dataset[columnName].quantile(0.25)
            descriptive.loc["Q2:50%", columnName] = dataset[columnName].quantile(0.50)
            descriptive.loc["Q3:75%", columnName] = dataset[columnName].quantile(0.75)
            descriptive.loc["Q4:100%", columnName] = dataset[columnName].quantile(1)

            descriptive.loc["IQR", columnName] = (
                descriptive.loc["Q3:75%", columnName] -
                descriptive.loc["Q1:25%", columnName]
            )

            descriptive.loc["1.5rule", columnName] = 1.5 * descriptive.loc["IQR", columnName]

            descriptive.loc["Lesser", columnName] = (
                descriptive.loc["Q1:25%", columnName] -
                descriptive.loc["1.5rule", columnName]
            )

            descriptive.loc["Greater", columnName] = (
                descriptive.loc["Q3:75%", columnName] +
                descriptive.loc["1.5rule", columnName]
            )

            descriptive.loc["Min", columnName] = dataset[columnName].min()
            descriptive.loc["Max", columnName] = dataset[columnName].max()

            descriptive.loc["LowOutLier", columnName] = (
                descriptive.loc["Min", columnName] <
                descriptive.loc["Lesser", columnName]
            )

            descriptive.loc["HighOutLier", columnName] = (
                descriptive.loc["Max", columnName] >
                descriptive.loc["Greater", columnName]
            )

        return descriptive