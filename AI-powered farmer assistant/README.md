Steps to Setup in Google Colab
1️⃣ Open Google Colab

Go to Google Colab
.

Click File → New Notebook.

2️⃣ Copy Your Full Code

Copy the entire code you shared.

Paste it into a new Colab notebook cell.

3️⃣ Install Required Libraries

The first section of your code already installs the dependencies:

!pip install google-generativeai --quiet
!pip install ipywidgets --quiet
!pip install deep-translator --quiet
!pip install pandas --quiet
!pip install requests --quiet


Run that cell. ✅

4️⃣ Enable ipywidgets in Colab

Colab sometimes needs an extension to render widgets properly.
Run this once:

!jupyter nbextension enable --py widgetsnbextension
!jupyter nbextension install --py widgetsnbextension


⚠️ If widgets still don’t show properly, you can use Colab’s built-in widget manager (it usually works automatically).

5️⃣ Add Your Gemini API Key

Inside the code:

API_KEY = "your_api_key_here"


Replace with your actual Gemini API key from Google AI Studio
.

6️⃣ Run All Cells in Order

Go to Runtime → Run all (or press Ctrl + F9).

Wait until all cells execute.

7️⃣ Use the App

You’ll see a nice form-based UI with:

Language selection 🌐

Service selection 🛠️

Location 📍

Product/Crop 🌱

Schemes 🏛️

After filling inputs → click “Get Solutions” ✅.

The output appears in the styled box with weather, schemes, guidance, etc.