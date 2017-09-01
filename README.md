# Reddit-Bot-Detector
Bot detector bot for Reddit using PRAW in python 3.5

List of reddit bots taken from: https://www.reddit.com/r/autowikibot/wiki/redditbots
List of reddit human users taken randomly from r/all hot posts.

Unfortunately, not much data is available, so there are only around 620 or so data points.

The trained model (model.h5) achieved an accuracy of 90% on the test set, but it's probably overfitting.

Parameter tuning with gridsearch will be done, too.

The fitted StandardScaler object has been saved to standard_scaler.sav.
To load the StandardScaler object, use:
```python
from sklearn.externals import joblib
sc = joblib.load('standard_scaler.sav')
```
