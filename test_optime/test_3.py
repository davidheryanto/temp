from sklearn.datasets import make_classification, fetch_mldata
from sklearn.preprocessing import StandardScaler
from sklearn.kernel_approximation import *
from sklearn import cross_validation

from hpsklearn import *
from hyperopt import *


def get_training_set_classification():
    """
    Get random training set for classification
    :return: tuple of X_train, y_train, X_test, y_test
    """
    X, y = make_classification(n_samples=10000, n_features=20)
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.4, random_state=1)

    # TODO Figure out how to optimize gamma as well, treat it as preprocessing stage in hyperopt_estimator?
    rbf_feature = RBFSampler(gamma=1, random_state=1)
    X_train = rbf_feature.fit_transform(X_train)
    X_test = rbf_feature.fit_transform(X_test)  # Are we supposed to transform this as well?

    scaler = StandardScaler()
    scaler.fit(X_train)  # fit only on training data
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, y_train, X_test, y_test


def get_training_set_digit():
    """
    Get MNIST original digit training set
    :return: tuple of X_train, y_train, X_test, y_test
    """
    digits = fetch_mldata('MNIST original')

    X = digits.data
    y = digits.target

    test_size = int(0.2 * len(y))
    np.random.seed(None)  # Use system time as seed
    indices = np.random.permutation(len(X))
    X_train = X[indices[:-test_size]]
    y_train = y[indices[:-test_size]]
    X_test = X[indices[-test_size:]]
    y_test = y[indices[-test_size:]]

    return X_train, y_train, X_test, y_test


def run():
    """
    Run test
    """
    X_train, y_train, X_test, y_test = get_training_set_classification()
    estimator = hyperopt_estimator(
        # TODO Figure out learning_rate='optimal' gives ValueError underflow exception
        # TODO Figure out why epoch is always 1
        classifier=sgd(
            loss='hinge',
            name='sgd_1',
            n_jobs=5,  # Change to -1 to use all cpus
            verbose=True,
            n_iter=50
        ),
        algo=tpe.suggest,
        trial_timeout=100,
        max_evals=50
    )
    estimator.fit(X_train, y_train)
    print(estimator.score(X_test, y_test))
    print(estimator.best_model())


if __name__ == '__main__':
    run()