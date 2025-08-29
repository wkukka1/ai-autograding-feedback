import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)

# Create a binary target variable by selecting only two species (Setosa and Versicolor)
df['species'] = iris.target
df = df[df['species'] != 2]  # Remove the Virginica species (category 2)
df['species'] = df['species'].apply(lambda x: 1 if x == 1 else 0)  # Setosa = 0, Versicolor = 1


def calculate_statistics(df):
    sepal_length = df['sepal length (cm)']
    sepal_width = df['sepal width (cm)']
    statistics = {
        'sepal_length_mean': np.mean(sepal_length),
        'sepal_length_median': np.median(sepal_length),
        'sepal_length_std': np.std(sepal_length),
        'sepal_length_var': np.var(sepal_length),
        'sepal_width_mean': np.mean(sepal_width),
        'sepal_width_median': np.median(sepal_width),
        'sepal_width_std': np.std(sepal_width),
        'sepal_width_var': np.var(sepal_width),
    }
    return statistics


X = df[['sepal length (cm)', 'sepal width (cm)']] 
y = df['species']
X_train, _, y_train, _ = train_test_split(X,
                y, test_size=0.3, random_state=42)
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

def classify_single_species(sample):  
    X = sample[['sepal length (cm)', 'sepal width (cm)']]
    prediction = model.predict(X)[0]
    
    return prediction