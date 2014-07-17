from hpsklearn import HyperoptEstimator

# Load Data
# ...

# Create the estimator object
estim = HyperoptEstimator()

# Search the space of classifiers and preprocessing steps and their
# respective hyperparameters in sklearn to fit a model to the data
estim.fit( train_data, train_label )

# Make a prediction using the optimized model
prediction = estim.predict( unknown_data )

# Report the accuracy of the classifier on a given set of data
score = estim.score( test_data, test_label )

# Return instances of the classifier and preprocessing steps
model = estim.best_model()