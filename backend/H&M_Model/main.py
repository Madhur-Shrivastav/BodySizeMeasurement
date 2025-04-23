from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from sklearn.preprocessing import StandardScaler
import os
import joblib
from typing import Union


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_assets(base_path: str = "./"):
    assets = {
        'models': {},
        'scalers': {},
        'encoders': {}
    }

    models_dir = os.path.join(base_path, "Models/men")
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith(".pkl"):
                category = file.replace(".pkl", "")
                assets['models'][category] = joblib.load(os.path.join(models_dir, file))
                
    scalers_dir = os.path.join(base_path, "Scalers/men")
    if os.path.exists(scalers_dir):
        for file in os.listdir(scalers_dir):
            if file.endswith(".pkl"):
                category = file.replace("_scaler.pkl", "")
                assets['scalers'][category] = joblib.load(os.path.join(scalers_dir, file))
               
    encoders_dir = os.path.join(base_path, "Encoders/men")
    if os.path.exists(encoders_dir):
        for file in os.listdir(encoders_dir):
            if file.endswith(".pkl"):
                parts = file.split("_")  
                category = "_".join(parts[:-2])  
                encoder_type = parts[-2]  

                if category not in assets['encoders']:
                    assets['encoders'][category] = {}

                assets['encoders'][category][encoder_type] = joblib.load(os.path.join(encoders_dir, file))

    return assets

assets = load_assets(base_path="./")

print("models:",assets['models'])
print("encoders:",assets['encoders'])
print("scalers:",assets['scalers'])
    
def match_category_input(user_input, categories):
    user_input = user_input.strip().lower()
    for category in categories:
        parts = category.split('_')
        if user_input in parts or user_input == category:
            return category
    return None

class BodySizeInput(BaseModel):
    category: str
    style: Union[str, None] = None
    chest_size: Union[float, None] = None
    waist_size: Union[float, None] = None
    arm_length: Union[float, None] = None
    neckline_size: Union[float, None] = None
    low_hip_size: Union[float, None] = None
    foot_length: Union[float, None] = None
    length: Union[int, None] = None

@app.post("/predict/")
def predict_body_size(input_data: BodySizeInput):
    
    print(input_data)
    model = assets['models'][input_data.category]
    
    style_encoder = assets['encoders'][input_data.category].get('style', None)
    
    if style_encoder:
        if input_data.style.lower() not in style_encoder.classes_:
            raise HTTPException(status_code=400, detail="Invalid style input. Please check available styles.")
        style_encoded = style_encoder.transform([input_data.style.lower()])[0]
    else:
        style_encoded = None  
        
    category_encoder = assets['encoders'][input_data.category]['category']
    if input_data.category.lower() not in category_encoder.classes_:
        raise HTTPException(status_code=400, detail="Invalid category input. Please check available categories.")
    
    category_encoded = category_encoder.transform([input_data.category.lower()])[0]
    
    size_encoder = assets['encoders'][input_data.category]['size']
    scaler = assets['scalers'][input_data.category]
    
    try:
        category_encoded = category_encoder.transform([input_data.category.lower()])[0]
        input_array = []
    
        if style_encoded is not None:
            input_array.append(style_encoded)
        if category_encoded is not None:
            input_array.append(category_encoded)
        if input_data.chest_size is not None:
            input_array.append(input_data.chest_size)
        if input_data.waist_size is not None:
            input_array.append(input_data.waist_size)
        if input_data.arm_length is not None:
            input_array.append(input_data.arm_length)
        if input_data.neckline_size is not None:
            input_array.append(input_data.neckline_size)
        if input_data.low_hip_size is not None:
            input_array.append(input_data.low_hip_size)
        if input_data.foot_length is not None:
            input_array.append(input_data.foot_length)
        if input_data.length is not None:
            input_array.append(input_data.length)
            
        print(input_array)
        input_array = np.array([input_array])
        input_scaled = scaler.transform(input_array)
        
        prediction = model.predict(input_scaled)
        predicted_size = size_encoder.inverse_transform(prediction)[0]
        
        print("predicted_size:", predicted_size)
        return {"predicted_size": predicted_size}
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
