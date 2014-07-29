import pickle
import time

import hyperopt.pyll.stochastic
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials


def objective(x):
    return {'loss': x ** 2,
            'status': STATUS_OK,
            'eval_time': time.time(),
            'other_stuff': {'type': None, 'value': [0, 1, 2]},
            'attachments': {'time_module': pickle.dumps(time.time)}}


trials = Trials()
# space = hp.uniform('x', -10, 10)

# space = hp.choice('a',
# [
# # c1 and c2 are called conditional parameters.
# ('case 1', 1 + hp.lognormal('c1', 0, 1)),
#                       ('case 2', hp.uniform('c2', -10, 10))
#                   ])
space = hp.choice('classifier_type', [
    {
        'type': 'naive_bayes',
    },
    {
        'type': 'svm',
        'C': hp.lognormal('svm_C', 0, 1),
        'kernel': hp.choice('svm_kernel', [
            {'ktype': 'linear'},
            {'ktype': 'RBF', 'width': hp.lognormal('svm_rbf_width', 0, 1)},
        ]),
    },
    {
        'type': 'dtree',
        'criterion': hp.choice('dtree_criterion', ['gini', 'entropy']),
        'max_depth': hp.choice('dtree_max_depth',
                               [None, hp.qlognormal('dtree_max_depth_int', 3, 1, 1)]),
        'min_samples_split': hp.qlognormal('dtree_min_samples_split', 2, 1, 1),
    },
])

if __name__ == '__main__':
    best = fmin(objective,
                space=hp.uniform('x', -10, 10),
                algo=tpe.suggest,
                max_evals=100,
                trials=trials)
    print best

    msg = trials.trial_attachments(trials.trials[5])['time_module']
    time_module = pickle.loads(msg)
    print time_module

    print('=' * 80)
    for i in range(0, 30):
        print hyperopt.pyll.stochastic.sample(space)