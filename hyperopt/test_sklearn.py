from hyperopt import hp
from hyperopt.pyll import scope
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier as DTree

if __name__ == '__main__':
    scope.define(GaussianNB)
    scope.define(SVC)
    C = hp.lognormal('svm_C', 0, 1)
    space = hp.pchoice('estimator', [
        (0.1, scope.GaussianNB()),
        (0.2, scope.SVC(C=C, kernel='linear'))])
