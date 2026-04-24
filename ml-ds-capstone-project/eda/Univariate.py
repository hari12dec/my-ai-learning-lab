import pandas as pd

class Univariate:

    def quanQual(self, dataset):
        quan = []
        qual = []

        for columnName in dataset.columns:
            if pd.api.types.is_numeric_dtype(dataset[columnName]):
                quan.append(columnName)
            else:
                qual.append(columnName)

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

    def findingOutlier(quan, descriptive):
        lesser = []
        greater = []
        for columnName in quan:
            if(descriptive[columnName]["Min"] <  descriptive[columnName]["Lesser"]):
                print("Lesser Outlier present in ", columnName)
                lesser.append(columnName)
            if(descriptive[columnName]["Max"] >  descriptive[columnName]["Greater"]):
                print("Greater Outlier present in ", columnName)
                greater.append(columnName)
        return lesser, greater
        
    def replacingOutlier(dataset, descriptive, lesser, greater):
        for columnName in lesser:
            dataset[columnName][dataset[columnName] < descriptive[columnName]["Lesser"]] =  descriptive[columnName]["Lesser"]
                    
        for columnName in greater:
            dataset[columnName][dataset[columnName] > descriptive[columnName]["Greater"]] =  descriptive[columnName]["Greater"]
        return dataset

    def get_pdf_probability(dataset, startrange, endrange):
        ax = sns.distplot(dataset,kde=True,kde_kws={'color':'blue'},color='Green')
        pyplot.axvline(startrange,color='Red')
        pyplot.axvline(endrange,color='Red')
        # generate a sample
        sample = dataset
        # calculate parameters
        sample_mean =sample.mean()
        sample_std = sample.std()
        print('Mean=%.3f, Standard Deviation=%.3f' % (sample_mean, sample_std))
        # define the distribution
        dist = norm(sample_mean, sample_std)
        
        # sample probabilities for a range of outcomes
        values = [value for value in range(startrange, endrange)]
        probabilities = [dist.pdf(value) for value in values]    
        prob=sum(probabilities)
        print("The area between range({},{}):{}".format(startrange,endrange,sum(probabilities)))
        return prob