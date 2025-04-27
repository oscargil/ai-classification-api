# train_model.py
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

print("--- Starting Model Training ---")

# 1. Load Dataset
iris = load_iris()
X = iris.data # Features
y = iris.target # Labels (species 0, 1, 2)
target_names = iris.target_names # Names ['setosa', 'versicolor', 'virginica']

print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features.")
print(f"Classes: {target_names}")

# 2. Split Data (Training and Testing)
# We'll use 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Data split: {X_train.shape[0]} for training, {X_test.shape[0]} for testing.")

# 3. Choose and Train Model (Logistic Regression - simple to start)
# Note: Despite the name 'Regression', it's commonly used for classification.
model = LogisticRegression(max_iter=200) # Increased max_iter to ensure convergence
print("Training the Logistic Regression model...")
model.fit(X_train, y_train)
print("Model trained.")

# 4. Evaluate Model (Optional but recommended)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy on the test set: {accuracy:.4f}") # Metric seen in Module 2

# 5. Save Trained Model
model_filename = 'iris_model.joblib'
joblib.dump(model, model_filename)
print(f"Model saved as '{model_filename}'.")

# Also save class names for use in the API
class_names_filename = 'iris_class_names.joblib'
joblib.dump(target_names, class_names_filename)
print(f"Class names saved as '{class_names_filename}'.")

print("--- Training Finished ---")