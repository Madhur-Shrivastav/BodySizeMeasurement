import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    category: "",
    style: "",
    chest_size: "",
    waist_size: "",
    arm_length: "",
    neckline_size: "",
    low_hip_size: "",
    foot_length: "",
    length: "",
  });

  const [predictedSize, setPredictedSize] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [categories, setCategories] = useState([]);
  const [categoryFeatures, setCategoryFeatures] = useState({});

  useEffect(() => {
    setCategories([
      "jeans_trousers",
      "shoes",
      "jackets_coats",
      "shirts",
      "tops_tshirts",
      "sweatshirts_hoodies",
    ]);
  }, []);

  const handleCategoryChange = (e) => {
    const selectedCategory = e.target.value;
    setFormData({
      category: selectedCategory,
      style: "",
      chest_size: "",
      waist_size: "",
      arm_length: "",
      neckline_size: "",
      low_hip_size: "",
      foot_length: "",
      length: "",
    });

    switch (selectedCategory) {
      case "jeans_trousers":
        setCategoryFeatures({
          style: false,
          waist_size: true,
          low_hip_size: true,
          length: true,
        });
        break;
      case "shoes":
        setCategoryFeatures({
          style: false,
          foot_length: true,
          length: false, // No length field for shoes
        });
        break;
      case "jackets_coats":
        setCategoryFeatures({
          style: true,
          chest_size: true,
          waist_size: true,
          arm_length: true,
          neckline_size: true,
          length: false, // No length field for jackets_coats
        });
        break;
      case "shirts":
        setCategoryFeatures({
          style: true,
          chest_size: true,
          waist_size: true,
          arm_length: true,
          neckline_size: true,
          length: false, // No length field for shirts
        });
        break;
      case "tops_tshirts":
        setCategoryFeatures({
          style: true,
          chest_size: true,
          waist_size: true,
          arm_length: true,
          neckline_size: true,
          length: false,
        });
        break;
      case "sweatshirts_hoodies":
        setCategoryFeatures({
          style: true,
          chest_size: true,
          waist_size: true,
          arm_length: true,
          neckline_size: true,
          length: false,
        });
        break;
      default:
        setCategoryFeatures({});
        break;
    }
  };

  const handleLengthChange = (e) => {
    setFormData({
      ...formData,
      length: e.target.value,
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const cleanedData = Object.fromEntries(
      Object.entries(formData).filter(
        ([key, value]) => value !== "" && value !== null
      )
    );

    console.log(cleanedData);

    try {
      const response = await axios.post(
        "http://localhost:8000/predict/",
        cleanedData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setPredictedSize(response.data.predicted_size);
    } catch (err) {
      setError("Error predicting body size. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="form-container">
        <h1>Body Size Prediction</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Category:</label>
            <select
              name="category"
              value={formData.category}
              onChange={handleCategoryChange}
              required
            >
              <option value="">Select Category</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>

          {categoryFeatures.style && (
            <div>
              <label>Style:</label>
              <input
                type="text"
                name="style"
                value={formData.style}
                onChange={(e) =>
                  setFormData({ ...formData, style: e.target.value })
                }
                required
              />
            </div>
          )}

          {categoryFeatures.waist_size && (
            <div>
              <label>Waist Size (cm):</label>
              <input
                type="number"
                name="waist_size"
                value={formData.waist_size}
                onChange={(e) =>
                  setFormData({ ...formData, waist_size: e.target.value })
                }
                required
              />
            </div>
          )}

          {categoryFeatures.low_hip_size && (
            <div>
              <label>Low Hip Size (cm):</label>
              <input
                type="number"
                name="low_hip_size"
                value={formData.low_hip_size}
                onChange={(e) =>
                  setFormData({ ...formData, low_hip_size: e.target.value })
                }
                required
              />
            </div>
          )}

          {categoryFeatures.foot_length && (
            <div>
              <label>Foot Length (cm):</label>
              <input
                type="number"
                name="foot_length"
                value={formData.foot_length}
                onChange={(e) =>
                  setFormData({ ...formData, foot_length: e.target.value })
                }
                required
              />
            </div>
          )}

          {categoryFeatures.chest_size && (
            <div>
              <label>Chest Size (cm):</label>
              <input
                type="number"
                name="chest_size"
                value={formData.chest_size}
                onChange={(e) =>
                  setFormData({ ...formData, chest_size: e.target.value })
                }
                required
              />
            </div>
          )}

          {categoryFeatures.arm_length && (
            <div>
              <label>Arm Length (cm):</label>
              <input
                type="number"
                name="arm_length"
                value={formData.arm_length}
                onChange={(e) =>
                  setFormData({ ...formData, arm_length: e.target.value })
                }
                required
              />
            </div>
          )}

          {categoryFeatures.neckline_size && (
            <div>
              <label>Neckline Size (cm):</label>
              <input
                type="number"
                name="neckline_size"
                value={formData.neckline_size}
                onChange={(e) =>
                  setFormData({ ...formData, neckline_size: e.target.value })
                }
                required
              />
            </div>
          )}

          {categoryFeatures.length && (
            <div>
              <label>Select Length:</label>
              <select
                name="length"
                value={formData.length}
                onChange={(e) =>
                  setFormData({ ...formData, length: e.target.value })
                }
                required
              >
                <option value="">Select Length</option>
                <option value="1">30 inch</option>
                <option value="2">32 inch</option>
                <option value="3">34 inch</option>
              </select>
            </div>
          )}

          <button type="submit" disabled={loading}>
            {loading ? "Loading..." : "Predict Size"}
          </button>
        </form>

        {predictedSize && (
          <div className="prediction">
            <h3>Predicted Size: {predictedSize}</h3>
          </div>
        )}

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default App;
