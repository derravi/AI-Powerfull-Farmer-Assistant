# AI-Powerfull-Farmer-Assistant
🌾 Kisan Saathi AI is an intelligent assistant for farmers, offering real-time weather forecasts, crop price trends, equipment info, government schemes, and direct market access in multiple Indian languages, powered by Google Gemini AI and translation support.


🌾 Kisan Saathi AI

Kisan Saathi AI is an intelligent assistant built to empower farmers with real-time agricultural insights, market access, and decision-making support. It leverages Google Gemini AI, translation support for multiple Indian languages, and fallback databases to ensure reliability even when APIs fail.

🚀 Features

Weather Forecasting ⛅ Get current and 5-day weather forecasts (with fallback data for reliability).

Farm Equipment Information 🚜 Explore tractors and equipment details with subsidies, schemes, and contact information.

Direct Market Access 🛒 Learn how to sell produce directly without middlemen via eNAM, FPOs, and online platforms.

Price Forecasting 📈 AI-powered 3-month price predictions with fallback trends for key crops.

eNAM Digital Market Guide 🌐 Step-by-step guide to register, list produce, and sell through India’s National Agricultural Market.

Climate-Smart Farming Advice 🌦️ Location and crop-specific guidance on water conservation, pest management, and climate adaptation.

Government Schemes Information 🏛️ Details about schemes like PM Fasal Bima Yojana, FPO support, and Direct Market Access policy.

Multi-Language Support 🌐 Available in English, Hindi, Gujarati, Punjabi, Marathi, Telugu, Tamil, Kannada, Bengali.

🛠️ Tech Stack

Python 3

Google Gemini API (google-generativeai)

Deep Translator (for multilingual translation)

Pandas (for equipment and market databases)

IPyWidgets (for interactive UI in Jupyter Notebook)

📂 Project Structure 📦 kisan-saathi-ai ┣ 📜 README.md ┣ 📜 requirements.txt ┗ 📜 kisan_saathi_ai.ipynb

⚙️ Installation

Clone this repository:

git clone https://github.com/your-username/kisan-saathi-ai.git cd kisan-saathi-ai

Install dependencies:

pip install -r requirements.txt

Or manually install:

pip install google-generativeai ipywidgets deep-translator pandas requests

Run Jupyter Notebook:

jupyter notebook

Open kisan_saathi_ai.ipynb and execute cells.

🔑 Setup Google Gemini API

Get your API key from Google AI Studio .

Replace the placeholder in the code:

API_KEY = "your_api_key_here"

📸 Screenshots

Main Interface Interactive form with language selection, services, and inputs.

Weather Forecast Example

📌 Future Enhancements

Integration with real-time weather APIs (IMD, OpenWeather).

Automated price tracking from eNAM and APMC.

Voice-based assistant for rural accessibility.

Mobile app deployment for offline usage.

🤝 Contributing

Contributions are welcome!

Fork the repository

Create a new branch (feature/your-feature)

Commit changes

Open a Pull Request

📜 License

This project is licensed under the MIT License.

👨‍💻 Author

Der Ravi

💼 GitHub: your-username

🌐 Passionate about AI for Agriculture & Farmer Empowerment
