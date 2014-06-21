from hyperopt import hp, fmin, rand, tpe, space_eval
from hyperopt.pyll.stochastic import sample


def q(args):
    x, y = args
    return x ** 2 + y ** 2


if __name__ == '__main__':
    space = [hp.uniform('x', 0, 1), hp.normal('y', 0, 1)]
    for i in range(0, 100):
        print sample(space)