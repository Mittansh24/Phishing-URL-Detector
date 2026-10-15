import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

print("RUNNING TRAIN.PY...")

# Load dataset
df = pd.read_csv("phishing.csv")

print("Dataset loaded successfully")

# Features & labels
# Remove 'class' (target) and 'Index' (useless column)
X = df.drop(["class", "Index"], axis=1)
y = df["class"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("Data split done")

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

print("Model training complete")

# Predictions
y_pred = model.predict(X_test)

# Accuracy
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# Report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("\nModel saved as model.pkl ✅")