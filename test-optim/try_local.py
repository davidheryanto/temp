# Binary SGD SVM
# using random search to find the proper hyper-parameters
# these hyper-parameters do NOT include kernel settings

from operator import itemgetter

import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import make_classification
from sklearn import cross_validation
from sklearn.preprocessing import StandardScaler
from sklearn.kernel_approximation import RBFSampler
from sklearn.pipeline import Pipeline

import hyperopt.tpe
import hpsklearn
import hpsklearn.demo_support
import time


# Utility function to report best scores
def report(grid_scores, n_top=3):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
            score.mean_validation_score,
            np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


if __name__ == '__main__':
    X, y = make_classification(n_samples=10000, n_features=20)
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        X, y, test_size=0.4, random_state=1)
    scaler = StandardScaler()

    # fit only on training data
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    # apply same transformation to test data
    X_test = scaler.transform(X_test)
    # The dimension of transformed feature vectors
    #  is NOT controlled by rbf__gamma
    clf = Pipeline([('rbf', RBFSampler(random_state=1)),
                    ('svm', SGDClassifier(verbose=0, learning_rate='constant', eta0=0.01))])

    estimator = hpsklearn.HyperoptEstimator(
        preprocessing=hpsklearn.components.any_preprocessing('pp'),
        classifier=hpsklearn.components.sklearn_SGDClassifier(verbose=1),
        algo=hyperopt.tpe.suggest,
        trial_timeout=15.0, # seconds
        max_evals=100,
        )

    iterator = estimator.fit_iter(X_train, y_train)
    iterator.next()

    while len(estimator.trials.trials) < estimator.max_evals:
        iterator.send(1)  # try one more model
        # hpsklearn.demo_support.scatter_error_vs_time(estimator, len(estimator.trials.trials))
        # hpsklearn.demo_support.bar_classifier_choice(estimator)

    # specify parameters and distributions to sample from
    param_dist = dict(svm__alpha=[0.0001, 0.00001],
                  svm__loss=['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'],
                  svm__penalty=['l2', 'l1'],
                  rbf__gamma=[0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.01, 0.05]
                  # "eta0":[0.01, 0.001, 0.0001]
    )
    # run randomized search
    # n_iter_search should be BIG enough
    n_iter_search = 500
    # paralellization can be done by setting n_jobs
    random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
                                       n_iter=n_iter_search, n_jobs=4)
    random_search.fit(X_train, y_train)
    report(random_search.grid_scores_)
    # plug best hyper-parameters into the SGDClassifier
    clf_crossed = Pipeline([('rbf', RBFSampler(random_state=1,
                                             gamma=random_search.best_params_['rbf__gamma'],)),
        ('svm', SGDClassifier(learning_rate='constant', eta0=0.01,
                              alpha=random_search.best_params_['svm__alpha'],
                              loss=random_search.best_params_['svm__loss'],
                              penalty=random_search.best_params_['svm__penalty']))])
    # retrain on the whole training set
    clf_crossed.fit(X_train, y_train)
    print(clf_crossed.score(X_test,y_test))