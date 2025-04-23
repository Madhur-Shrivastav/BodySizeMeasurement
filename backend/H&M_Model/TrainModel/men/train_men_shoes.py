import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os
import joblib

def dump_model(model, category_encoder, size_encoder, scaler):
    category_name = "shoes"     
    os.makedirs("../../Models/men", exist_ok=True)
    joblib.dump(model, f"../../Models/men/{category_name}.pkl")
    os.makedirs("../../Encoders/men", exist_ok=True)
    joblib.dump(category_encoder, f"../../Encoders/men/{category_name}_category_encoder.pkl")
    joblib.dump(size_encoder, f"../../Encoders/men/{category_name}_size_encoder.pkl")
    os.makedirs("../../Scalers/men", exist_ok=True)
    joblib.dump(scaler, f"../../Scalers/men/{category_name}_scaler.pkl")
    print(f"Trained and saved model for '{category_name}'.")


df = pd.read_csv("../../Datasets/men/shoes_data.csv")

category_encoder = LabelEncoder()
size_encoder = LabelEncoder()

df['category'] = category_encoder.fit_transform(df['category'])
df['size'] = size_encoder.fit_transform(df['size'])  

X = df[[ 'category', 'foot_length_cm']]
y = df['size']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

dump_model(model,category_encoder,size_encoder,scaler)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100}%")

size_mapping = {index: label for index, label in enumerate(size_encoder.classes_)}
print("Size Mapping:", size_mapping)

valid_categories = category_encoder.classes_

print("Valid Categories:", valid_categories)


def match_category_input(user_input, categories):
    user_input = user_input.strip().lower()
    for category in categories:
        parts = category.split('_')
        if user_input in parts or user_input == category:
            return category
    return None


        
def predict_size():
    print("\n--- Enter the following details to predict your size ---")
    try:
        category = input(f"Category (choose from {list(valid_categories)}): ")
        if category not in valid_categories:
            raise ValueError(f"Invalid category. Choose from {list(valid_categories)}.")

        foot_length_cm = float(input("foot length (in cm): "))

        category_encoded = category_encoder.transform([category])[0]

        
        input_data = pd.DataFrame(
            [[category_encoded, foot_length_cm]],
            columns=['category', 'foot_length_cm']
        )
        
        input_scaled = scaler.transform(input_data)
        predicted_size_index = model.predict(input_scaled)[0]
        predicted_size = size_mapping.get(predicted_size_index, "Unknown")
        print(f"\nPredicted Size: {predicted_size}")

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Error: {e}\nPlease ensure the inputs are correct.")

predict_size()
