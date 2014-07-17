from hpsklearn import HyperoptEstimator, any_classifier, svc
from sklearn.datasets import fetch_mldata
from hyperopt import tpe
import numpy as np

# Download the data and split into training and test sets
if __name__ == '__main__':
    digits = fetch_mldata('MNIST original')

    X = digits.data
    y = digits.target

    seed = 910

    test_size = int( 0.2 * len( y ) )
    np.random.seed( seed )
    indices = np.random.permutation(len(X))
    X_train = X[ indices[:-test_size]]
    y_train = y[ indices[:-test_size]]
    X_test = X[ indices[-test_size:]]
    y_test = y[ indices[-test_size:]]

    estim = HyperoptEstimator( classifier=svc('my_svc'),
                                algo=tpe.suggest, trial_timeout=300, max_evals=5)

    print('Running fit...')
    print('=' * 80)
    estim.fit( X_train, y_train )
    print('Finished fit')

    print( estim.score( X_test, y_test ) )
    # <<show score here>>
    print( estim.best_model() )
    # <<show model here>>