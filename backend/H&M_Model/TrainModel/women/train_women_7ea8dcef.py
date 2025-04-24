import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os
import joblib
def dump_model(model):
    category_name = "dresses_pajamas_robes_pencilskirts_pleatedskirts_miniskirts"     
    os.makedirs("../../Models/women", exist_ok=True)
    joblib.dump(model, f"../../Models/women/{category_name}.pkl")
    os.makedirs("../../Encoders/women", exist_ok=True)
    joblib.dump(style_encoder, f"../../Encoders/women/{category_name}_style_encoder.pkl")
    joblib.dump(category_encoder, f"../../Encoders/women/{category_name}_category_encoder.pkl")
    joblib.dump(size_encoder, f"../../Encoders/women/{category_name}_size_encoder.pkl")
    os.makedirs("../../Scalers/women", exist_ok=True)
    joblib.dump(scaler, f"../../Scalers/women/{category_name}_scaler.pkl")
    print(f"Trained and saved model for '{category_name}'.")


df = pd.read_csv("../../Datasets/women/7ea8dcef_data.csv")

style_encoder = LabelEncoder()
category_encoder = LabelEncoder()
size_encoder = LabelEncoder()

df['style'] = style_encoder.fit_transform(df['style'])
df['category'] = category_encoder.fit_transform(df['category'])
df['size'] = size_encoder.fit_transform(df['size'])

X = df[['style', 'category', 'chest_cm', 'low_hip_cm', 'inside_leg_length_cm']]
y = df['size']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

dump_model(model)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100}%")

size_mapping = {index: label for index, label in enumerate(size_encoder.classes_)}
print("Size Mapping:", size_mapping)

valid_styles = style_encoder.classes_
valid_categories = category_encoder.classes_

print("\nValid Styles:", valid_styles)
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
        style = input(f"Style (choose from {list(valid_styles)}): ")
        if style not in valid_styles:
            raise ValueError(f"Invalid style. Choose from {list(valid_styles)}.")

        category = input(f"Category (enter full name or components): ").strip()
        matched_category = match_category_input(category, valid_categories)

        if not matched_category:
            raise ValueError(f"Invalid category. Please enter a valid full category or component.")

        chest_cm = float(input("Chest size (in cm): "))
        low_hip_cm = float(input("Low Hip size (in cm): "))
        inside_leg_length_cm: float = float(input("Inside Leg Length (in cm): "))

        style_encoded = style_encoder.transform([style])[0]
        category_encoded = category_encoder.transform([matched_category])[0]

        input_data = pd.DataFrame(
            [[style_encoded, category_encoded, chest_cm, low_hip_cm, inside_leg_length_cm]],
            columns=['style', 'category', 'chest_cm', 'low_hip_cm', 'inside_leg_length_cm']
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

