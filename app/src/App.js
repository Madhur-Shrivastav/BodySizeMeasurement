import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [gender, setGender] = useState("");
  const [formData, setFormData] = useState({
    gender: "",
    category: "",
    style: "",
    chest_size: "",
    waist_size: "",
    arm_length: "",
    neckline_size: "",
    low_hip_size: "",
    foot_length: "",
    inside_leg_length: "",
    length: "",
  });

  const [predictedSize, setPredictedSize] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [categories, setCategories] = useState([]);
  const [categoryFeatures, setCategoryFeatures] = useState({});

  useEffect(() => {
    if (gender === "men") {
      const menCats = [
        "jeans_trousers",
        "shoes",
        "jackets_coats",
        "shirts",
        "tops_tshirts",
        "sweatshirts_hoodies",
      ];
      const options = menCats.flatMap((cat) =>
        cat.split("_").map((sub) => ({ sub, full: cat }))
      );
      setCategories(options);
    } else if (gender === "women") {
      const femaleCats = [
        "dresses_pajamas_robes_pencilskirts_pleatedskirts_miniskirts",
        "shortsleeve_longsleeve_tshirt_tanktops_bodysuits_lowcuttops_turtlenecks_halternecktops_puffsleeve_cutouttops_sweatshirts_hoodies_knitwear_sweaters_cardigans_jackets_coats_anoraks_gilets_dresses_bloueses_blaizers_nighties",
        "corsets_bustiers_bandeau",
        "jumpsuits",
        "tops",
        "jeans_trousers_shorts_denimskirts",
      ];
      const options = femaleCats.flatMap((cat) =>
        cat.split("_").map((sub) => ({ sub, full: cat }))
      );
      setCategories(options);
    } else {
      setCategories([]);
    }
  }, [gender]);

  const handleGenderChange = (e) => {
    const selectedGender = e.target.value;
    setGender(selectedGender);
    setFormData({
      gender: selectedGender,
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
    setCategoryFeatures({});
    setPredictedSize(null);
  };

  const handleCategoryChange = (fullCategory) => {
    setFormData((prevData) => ({
      gender: prevData.gender,
      category: fullCategory,
      style: "",
      chest_size: "",
      waist_size: "",
      arm_length: "",
      neckline_size: "",
      low_hip_size: "",
      foot_length: "",
      inside_leg_length: "",
      length: "",
    }));

    if (gender === "men") {
      switch (fullCategory) {
        case "jeans_trousers":
          setCategoryFeatures({
            style: false,
            waist_size: true,
            low_hip_size: true,
            inside_leg_length: true,
          });
          break;
        case "shoes":
          setCategoryFeatures({
            style: false,
            foot_length: true,
          });
          break;
        case "jackets_coats":
        case "shirts":
        case "tops_tshirts":
        case "sweatshirts_hoodies":
          setCategoryFeatures({
            style: true,
            chest_size: true,
            waist_size: true,
            arm_length: true,
            neckline_size: true,
          });
          break;
        default:
          setCategoryFeatures({});
      }
    } else if (gender === "women") {
      switch (fullCategory) {
        case "dresses_pajamas_robes_pencilskirts_pleatedskirts_miniskirts":
        case "jumpsuits":
          setCategoryFeatures({
            style: true,
            chest_size: true,
            low_hip_size: true,
            inside_leg_length: true,
          });
          break;

        case "shortsleeve_longsleeve_tshirt_tanktops_bodysuits_lowcuttops_turtlenecks_halternecktops_puffsleeve_cutouttops_sweatshirts_hoodies_knitwear_sweaters_cardigans_jackets_coats_anoraks_gilets_dresses_bloueses_blaizers_nighties":
        case "corsets_bustiers_bandeau":
          setCategoryFeatures({
            style: true,
            chest_size: true,
            low_hip_size: true,
          });
          break;

        case "tops":
          setCategoryFeatures({
            style: true,
            chest_size: true,
            waist_size: true,
            low_hip_size: true,
          });
          break;
        case "jeans_trousers_shorts_denimskirts":
          setCategoryFeatures({
            style: true,
            inside_leg_length: true,
            low_hip_size: true,
          });
          break;

        default:
          setCategoryFeatures({});
      }
    }
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

        <div>
          <label>Gender:</label>
          <select
            name="gender"
            value={gender}
            onChange={handleGenderChange}
            required
          >
            <option value="">Select Gender</option>
            <option value="men">Men</option>
            <option value="women">Female</option>
          </select>
        </div>

        <form onSubmit={handleSubmit}>
          <div>
            <label>Category:</label>
            <select
              name="category"
              value={
                categories.find((c) => c.full === formData.category)?.sub || ""
              }
              onChange={(e) => {
                const sub = e.target.value;
                const full = categories.find((c) => c.sub === sub)?.full || "";
                handleCategoryChange(full);
              }}
              required
            >
              <option value="">Select Category</option>
              {categories.map((cat, index) => (
                <option key={`${cat.sub}-${cat.full}-${index}`} value={cat.sub}>
                  {cat.sub
                    .replace(/_/g, " ")
                    .replace(/\b\w/g, (l) => l.toUpperCase())}
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
                onChange={handleChange}
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
                onChange={handleChange}
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
                onChange={handleChange}
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
                onChange={handleChange}
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
                onChange={handleChange}
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
                onChange={handleChange}
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
                onChange={handleChange}
                required
              />
            </div>
          )}
          {categoryFeatures.inside_leg_length && (
            <div>
              <label>Inside Leg Length (cm):</label>
              <input
                type="number"
                value={formData.inside_leg_length}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    inside_leg_length: e.target.value,
                  })
                }
              />
            </div>
          )}

          {categoryFeatures.length && (
            <div>
              <label>Select Length:</label>
              <select
                name="length"
                value={formData.length}
                onChange={handleChange}
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
