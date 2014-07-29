from hyperopt import hp
from hyperopt.pyll import scope
from sklearn.svm import SVC

def q(args):
    x,y = args
    return x ** 2 + y ** 2

space = hp.uniform('a',0,1)
fmin(q, space, algo=)
