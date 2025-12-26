import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


def train_model(csv_path):
    df = pd.read_csv(csv_path).dropna()

    le = LabelEncoder()
    df["gender"] = le.fit_transform(df["gender"])
    df["smoking_status"] = le.fit_transform(df["smoking_status"])

    X = df[
        ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi"]
    ]
    y = df["stroke"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    return model, accuracy
