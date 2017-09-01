# Detects Reddit Bots

# Import libraries
import pandas as pd

# Import dataset
dataset = pd.read_csv('data.csv')

# Get inputs and outputs
x = dataset.iloc[:,1:-1]
y = dataset.iloc[:, -1]

# Split into train set and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Scale data
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Save standard scaler
from sklearn.externals import joblib
joblib.dump(sc, 'standard_scaler.sav')

# Import Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense

# Assemble ANN
classifier = Sequential()

classifier.add(Dense(input_dim=17, units = 12, kernel_initializer='uniform', activation='relu'))

classifier.add(Dense(units=12, kernel_initializer='uniform', activation='relu'))

classifier.add(Dense(units=12, kernel_initializer='uniform', activation='relu'))

classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fit to train set
classifier.fit(x_train, y_train, batch_size=16, epochs=100)

# Test on test set
y_pred = classifier.predict(x_test)
y_pred = (y_pred > 0.5)

# Create confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)