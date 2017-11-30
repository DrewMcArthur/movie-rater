import numpy as np, bisect

class CategoricalEncoder(TransformerMixin):
    """ categorical encoder for use in a sklearn pipeline.  
	OneHotEncoder but for strings. """

    def __init__(self, cat_feats):
        self.mask = cat_feats

    def fit(self, Xs, Ys=None):
        # convert the list of dicts to a list of lists
        listXs = [[item for key, item in row.items()] for row in Xs]
        # convert 2d list to 2d numpy array
        nArray = np.array(listXs)
        # create a list of labelencoders, one for each column
        self.mapper= []
        # for each column, fit a labelencoder to that column
        for i in range(len(Xs[0])):
            if self.mask[i]:
                self.mapper.append(LabelEncoder())
                col = nArray[:,i]
                self.mapper[i].fit(col)
                le_classes = self.mapper[i].classes_.tolist()
                bisect.insort_left(le_classes, 'other')
                self.mapper[i].classes_ = le_classes
            else:
                self.mapper.append(False)

    def transform(self, Xs, Ys=None):
        # convert the list of dicts to a list of lists
        listXs = [[item for key, item in row.items()] for row in Xs]
        nArray = np.array(listXs)
        for i in range(len(Xs[0])):
            if self.mask[i]:
                col = nArray[:,i]
                col = list(map(lambda s: 'other' if s not in self.mapper[i].classes_
                                                 else s, col.tolist()))

                # transform the columns
                nArray[:,i] = self.mapper[i].transform(col)
        nArray = list(map(lambda x: "NaN" if x == '' else x, nArray))
        return nArray
        
    def fit_transform(self, Xs, Ys=None):
        """ applies labelencoder to each column, if the column is determined
            to be continuous variables """
        # convert the list of dicts to a list of lists
        listXs = [[item for key, item in row.items()] for row in Xs]
        # convert 2d list to 2d numpy array
        nArray = np.array(listXs)
        # create a list of labelencoders, one for each column
        self.mapper= []
        # get first row, which is all headers
        headers = nArray[0]

        # for each column, fit and transform using its respective labelencoder
        for i in range(len(headers)):
            col = nArray[:,i]
            if self.mask[i]:
                self.mapper.append(LabelEncoder())
                self.mapper[i].fit(col)

                le_classes = self.mapper[i].classes_.tolist()
                bisect.insort_left(le_classes, 'other')
                self.mapper[i].classes_ = le_classes
                
                nArray[:,i] = self.mapper[i].transform(col)
            else:
                self.mapper.append(False)

        nArray = list(map(lambda x: "NaN" if x == '' else x, nArray))
        return nArray
