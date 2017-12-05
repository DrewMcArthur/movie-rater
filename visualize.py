""" 
    visualize.py

    load a model from file, and visualize the nn.
    model is a pipeline object, that contains a named_step "nn"
"""
import pickle
from os.path import isfile
from learn import loadData

def load(filename):
    if isfile(filename):
        with open(filename, 'rb') as handle:
            return pickle.load(handle)
    else:
        print("Error: Model file not found. Run `python learn.py` first.")

def visualize(M):
    """ given a model M, visualize the neural network and how it predicts.
        note: M is assumed to be a pipeline containing a named step "nn"
    """
    nn = M.named_steps['nn']

    # training is a panda df
    training, label = load("cleanedData.pkl")
    print(training)

    print(len(nn.coefs_[0]))
    #[print(col) for col in zip(training.columns.values, nn.coefs_[0])]

    coefficients = [x[0] for x in nn.coefs_[0]]
    headerweights = zip(training.columns.values, coefficients)
    [print(col) for col in sorted(headerweights, key=lambda row:row[1])]

def main():
    model = load("model.pkl")
    visualize(model)

if __name__ == "__main__":
    main()
