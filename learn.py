"""
    learn.py

    defines functions that train a model based on 
    movie data collected in scrape.py
"""
from sklearn.metrics import explained_variance_score, r2_score
                        # model performance metrics
from glob import glob   # used to create list of filenames from wildcard
import os.path          # used to check if a file exists
import pickle           # object serialization
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

def shapeData(data):
    """ takes the data loaded from file and returns training data and labels
        that can easily be processed by machine learning """
    [json_print(x) for x in data[:3]]
    return [shapeDatum(row) for row in data]

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
    training, labels = shapeData(data)
    exit()
    train, test = split_data(training, labels)

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
