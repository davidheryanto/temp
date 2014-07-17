import numpy as np
import skdata.iris.view
import hyperopt.tpe
import hpsklearn
import hpsklearn.demo_support
import time

data_view = skdata.iris.view.KfoldClassification(4)
