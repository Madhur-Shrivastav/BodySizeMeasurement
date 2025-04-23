import random
import os
import pandas as pd
from menchart import men_size_charts, men_size_charts_2
from womenchart import women_size_charts
import hashlib

def generate_synthetic_data(data, num_samples):
    synthetic_data = []
    for category, styles in data.items():
        for style, sizes in styles.items():
            for size, measurements in sizes.items():
                for _ in range(num_samples):
                    data_point = {
                        'category': category,
                        'style': style,
                        'size': size
                    }
                    for measurement, value_range in measurements.items():
                        if isinstance(value_range, tuple):
                            data_point[measurement] = (random.uniform(value_range[0],value_range[1]))
                        else:
                            data_point[measurement] = value_range
                    synthetic_data.append(data_point)
    return synthetic_data

def export_data_by_category(df, output_dir):
  for category, data_subset in df.groupby('category'):
      
    if len(category) > 50:
        category_hash = hashlib.md5(category.encode()).hexdigest()[:8]
        filename = f"{category_hash}_data.csv"
    else:
        filename = f"{category}_data.csv"
        
    filepath = os.path.join(output_dir, filename)
    data_subset = data_subset.dropna(axis=1)
    data_subset.to_csv(filepath, index=False)

synthetic_data = generate_synthetic_data(men_size_charts, 100)
df = pd.DataFrame(synthetic_data)
output_dir = "../Datasets/men"  
export_data_by_category(df, output_dir)

def generate_synthetic_data2(data, num_samples):
    synthetic_data = []
    for category, sizes in data.items():
        for size, measurements in sizes.items():
            for _ in range(num_samples):
                data_point = {
                    'category': category,
                    'size': size
                }
                for measurement, value_range in measurements.items():
                    if isinstance(value_range, tuple):
                            data_point[measurement] = random.uniform(value_range[0],value_range[1])
                    else:
                        data_point[measurement] = value_range
                synthetic_data.append(data_point)
    return synthetic_data

synthetic_data2 = generate_synthetic_data2(men_size_charts_2, 100)
df = pd.DataFrame(synthetic_data2)
output_dir = "../Datasets/men"  
export_data_by_category(df, output_dir)

synthetic_data_women = generate_synthetic_data(women_size_charts, 100)
df_women = pd.DataFrame(synthetic_data_women)
output_dir_women = "../Datasets/women"
export_data_by_category(df_women, output_dir_women)