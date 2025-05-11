# train_model.py

import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

with open("data/X_train.pkl", "rb") as f:
    X_train = pickle.load(f)
with open("data/X_test.pkl", "rb") as f:
    X_test = pickle.load(f)
with open("data/y_train.pkl", "rb") as f:
    y_train = pickle.load(f)
with open("data/y_test.pkl", "rb") as f:
    y_test = pickle.load(f)

model = RandomForestClassifier(
    n_estimators=100,  # number of trees
    max_depth=5,       # prevent overfitting
    random_state=42    # reproducibility
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {acc:.2f}")

print("\nClassification report:")
print(classification_report(y_test, y_pred, target_names=["Loss", "Draw", "Win"]))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Loss", "Draw", "Win"], yticklabels=["Loss", "Draw", "Win"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

with open("data/model.pkl", "wb") as f:
    pickle.dump(model, f)