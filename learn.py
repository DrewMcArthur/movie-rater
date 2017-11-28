"""
    learn.py

    defines functions that train a model based on 
    movie data collected in scrape.py
"""
from sklearn.metrics import explained_variance_score, r2_score
                        # model performance metrics
from glob import glob   # used to create list of filenames from wildcard
import os.path          # used to check if a file exists
import pickle           # used for object serialization
import random           # used to split the data
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelBinarizer

# local imports
from scrape import json_print
from clean_data import shapeDatum

def loadData(*sections):
    """ loads data from data-stores/ dir and returns it.  lots of data  """
    data = []

    if sections == ():
        files = glob("data-stores/m_data_*.pkl")
    else: 
        files = ["data-stores/m_data_{}.pkl".format(i) for i in sections]
        files = list(filter(lambda fn: os.path.isfile(fn), files))

    print("datafiles available:", files)
    for f in files:
        with open(f, 'rb') as handle:
            data += pickle.load(handle)

    return data

def flattenListValues(data):
    # turn columns with list values into multiple binary columns
    # answered here: https://stackoverflow.com/a/47535706/3972042
    df = pd.DataFrame(data)

    # genres
    # explode the list to separate rows
    X = pd.concat(
            [pd.DataFrame(v, index=np.repeat(k,len(v)), columns=['genre']) 
                                    for k,v in df.genre.to_dict().items()])
    lb = LabelBinarizer()
    dd = pd.DataFrame(lb.fit_transform(X), index=X.index, columns=lb.classes_)
    del df['genre']
    df = pd.concat([df, dd.groupby(dd.index).max()], axis=1)

    # languages
    # explode the list to separate rows
    X = pd.concat(
            [pd.DataFrame(v, index=np.repeat(k,len(v)), columns=['language']) 
                                    for k,v in df.language.to_dict().items()])
    lb = LabelBinarizer()
    dd = pd.DataFrame(lb.fit_transform(X), index=X.index, columns=lb.classes_)
    del df['language']
    df = pd.concat([df, dd.groupby(dd.index).max()], axis=1)

    # production
    # explode the list to separate rows
    X = pd.concat(
            [pd.DataFrame(v, index=np.repeat(k,len(v)), columns=['production']) 
                                    for k,v in df.production.to_dict().items()])
    lb = LabelBinarizer()
    dd = pd.DataFrame(lb.fit_transform(X), index=X.index, columns=lb.classes_)
    del df['production']
    df = pd.concat([df, dd.groupby(dd.index).max()], axis=1)

    # countries
    # explode the list to separate rows
    X = pd.concat(
            [pd.DataFrame(v, index=np.repeat(k,len(v)), columns=['country']) 
                                    for k,v in df.country.to_dict().items()])
    lb = LabelBinarizer()
    dd = pd.DataFrame(lb.fit_transform(X), index=X.index, columns=lb.classes_)
    del df['country']
    df = pd.concat([df, dd.groupby(dd.index).max()], axis=1)

    return df

def shapeData(data):
    """ takes the data loaded from file and returns training data and labels
        that can easily be processed by machine learning """
    data, labels = zip(*list(filter((None.__ne__), 
                                    [shapeDatum(row) for row in data])))
    df = flattenListValues(list(data))

    # return a list of the data values and the label
    return (df.values.tolist(), list(labels))

def splitData(data, labels, ratio=0.5):
    """ splits the data into training and test sets returned in the format 
        ( (training data, training labels), (test data, test labels) )"""
    assert(len(data) == len(labels))

    test = []
    testlabels = []
    len_test = round(len(data) * (1 - ratio))

    # randomly select an entry from the data to be moved into the test set
    for _ in range(len_test):
        i = random.randrange(len(data))
        test.append(data.pop(i))
        testlabels.append(labels.pop(i))

    return ( (data, labels), (test, testlabels) )

def initModel():
    """ uses sklearn pipeline to initialize an AI model """
    pass

def main():
    # load and process the data
    data = loadData()
    print("Loaded", len(data), "rows of data.")
    training, labels = shapeData(data)
    print("Shaved data down to {} rows with {} labels."
                .format(len(training), len(labels)))
    train, test = splitData(training, labels)
    print("Split data into {} training rows and {} test rows."
                .format(len(train[0]), len(test[0])))

    # separate variables for different sections of data
    train_X, train_Y = train
    test_X, test_Y = test


    # create and train the model
    model = initModel()
    model.fit(train_X, train_Y)

    # test the model and report accuracy
    pred_Y = model.predict(test_X)
    deltas = [abs(p-l) for p, l in zip(pred_Y, test_Y)]
    print("     avg delta:  ", sum(deltas)/len(deltas))
    print("variance score:  ", explained_variance_score(y_test, y_pred))
    print("     r squared:  ", r2_score(y_test, y_pred))


if __name__ == "__main__":
    main()
