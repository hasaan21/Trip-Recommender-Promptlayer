# AI Trip Recommender API

## 🚀 Overview
The **AI Trip Recommender API** is a Flask-based web service that generates **custom travel itineraries** using **PromptLayer** and **OpenAI's GPT models**. It allows users to request personalized travel recommendations based on their **destination, duration, and preferences**.

---

## 📌 Features
✅ **Custom travel recommendations** based on user input  
✅ **Integration with OpenAI's GPT models** via PromptLayer  
✅ **Metadata tracking & scoring** for response evaluation  
✅ **Flask-powered REST API** for easy integration  
✅ **Poetry for dependency management**  

---

## ⚡ Installation & Setup
### **1️⃣ Clone the Repository**
```bash
 git clone https://github.com/your-repo/ai-trip-recommender.git
 cd ai-trip-recommender
```

### **2️⃣ Install Poetry**
If you haven't installed Poetry, run:
```bash
pip install poetry
```

### **3️⃣ Install Dependencies**
```bash
poetry install
```

### **4️⃣ Set Up Environment Variables**
Create a **.env** file and add your API keys:
```ini
# .env
PROMPTLAYER_API_KEY=your_promptlayer_api_key
OPENAI_API_KEY=your_openai_api_key
ENV=production  # or development
```

---

## 🛠 Running the API
```bash
poetry run python app.py
```
The API will start on **http://127.0.0.1:5000**.

---

## 📡 API Usage
### **📍 GET Welcome Message**
```bash
curl -X GET http://127.0.0.1:5000/
```
📌 **Response:**
```json
{
  "message": "Welcome to the AI Trip Recommender API!"
}
```

### **📍 POST Get a Trip Recommendation**
```bash
curl -X POST http://127.0.0.1:5000/recommend_trip \
     -H "Content-Type: application/json" \
     -d '{
          "destination": "Paris",
          "duration": "5 days",
          "preferences": "art, museums, fine dining",
          "user_id": "user_123"
        }'
```
📌 **Response:**
```json
{
    "destination": "Paris",
    "trip_plan": "Here is your 5-day trip itinerary for Paris: ..."
}
```

---

## 🏗️ How It Works
1️⃣ Extracts **user input** (destination, duration, preferences).  
2️⃣ Calls **OpenAI GPT** via PromptLayer to **generate a trip itinerary**.  
3️⃣ Tracks **metadata** (user ID, preferences).  
4️⃣ Logs **API request** and scores results for evaluation.  

---

## 🚀 Next Steps
✅ Integrate **Google Maps API** for location visualization.
✅ Adding support for **A/B testing**
✅ Optimize API calls using **caching & cost control**.  

Feel free to contribute and improve this project! 😊
