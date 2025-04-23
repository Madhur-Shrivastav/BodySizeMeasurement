import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random
import os
import joblib
def dump_model(model, category_encoder, size_encoder, scaler):
    category_name = "jeans_trousers"     
    os.makedirs("../../Models/men", exist_ok=True)
    joblib.dump(model, f"../../Models/men/{category_name}.pkl")
    os.makedirs("../../Encoders/men", exist_ok=True)
    joblib.dump(category_encoder, f"../../Encoders/men/{category_name}_category_encoder.pkl")
    joblib.dump(size_encoder, f"../../Encoders/men/{category_name}_size_encoder.pkl")
    os.makedirs("../../Scalers/men", exist_ok=True)
    joblib.dump(scaler, f"../../Scalers/men/{category_name}_scaler.pkl")
    print(f"Trained and saved model for '{category_name}'.")

df = pd.read_csv("../../Datasets/men/jeans_trousers_data.csv")

size_encoder = LabelEncoder()
category_encoder = LabelEncoder()

df['category'] = category_encoder.fit_transform(df['category'])
df['size'] = size_encoder.fit_transform(df['size'])

base_features = ['category', 'waist_cm', 'low_hip_cm']
length_columns = ['30inch_length_cm', '32inch_length_cm', '34inch_length_cm']

size_mapping = {index: label for index, label in enumerate(size_encoder.classes_)}
valid_categories = category_encoder.classes_

def train_model(length_column):
    features = base_features + [length_column]
    X = df[features]
    y = df['size']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
#-----------------------------------------------------------------------------------------------------------------------   
    import matplotlib.pyplot as plt
    import numpy as np

    feature_importance = model.feature_importances_
    feature_names = ['category', 'waist_cm', 'low_hip_cm']

    plt.figure(figsize=(6, 6))
    plt.bar(range(len(feature_importance)), feature_importance, align="center")
    plt.xticks(range(len(feature_importance)), feature_names, rotation=45)
    plt.xlabel("Feature")
    plt.ylabel("Importance Score")
    plt.title("Feature Importance in Size Prediction Model")
    plt.show()
#------------------------------------------------------------------------------------------------------------------------
    
    dump_model(model,category_encoder,size_encoder,scaler)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy (using {length_column}): {accuracy * 100:.2f}%")
    return model, scaler

def match_category_input(user_input, categories):
    user_input = user_input.strip().lower()
    for category in categories:
        parts = category.split('_')
        if user_input in parts or user_input == category:
            return category
    return None

def predict_size():
    print("\n--- Enter the following details to predict your jeans/trousers size ---")
    try:
        category = input(f"Category (enter full name or components): ").strip()
        matched_category = match_category_input(category, valid_categories)

        if not matched_category:
            raise ValueError(f"Invalid category. Please enter a valid full category or component.")
        
        waist_cm = float(input("Waist size (in cm): "))
        low_hip_cm = float(input("Low hip size (in cm): "))
        
        print("\nSelect the length option:")
        print("1. 30 inch")
        print("2. 32 inch")
        print("3. 34 inch")
        
        length_option = int(input("Enter 1, 2, or 3: "))
        
        if length_option == 1:
            selected_length = '30inch_length_cm'
        elif length_option == 2:
            selected_length = '32inch_length_cm'
        elif length_option == 3:
            selected_length = '34inch_length_cm'
        else:
            raise ValueError("Invalid option. Please choose 1, 2, or 3.")
        
        model, scaler = train_model(selected_length)
        
        random_length_value = random.choice(df[selected_length].dropna().values)
        print(f"\nRandomly selected {selected_length} value: {random_length_value} cm")
        
        input_data = pd.DataFrame(
            [[category_encoder.transform([matched_category])[0], waist_cm, low_hip_cm, random_length_value]],
            columns=base_features + [selected_length]
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

# Madhur's chest,waist,arm length,neckline,hip,inseam,foot= 95,81,56,37,94,80,25 in cm
# Mama's chest,waist,arm length,neckline,hip,inseam,foot=110,110,55,41,109,63,25 in cm
# Pranshu's chest,waist,arm length,neckline,hip,inseam,foot= 95,83,56,38,94,68,  in cm
