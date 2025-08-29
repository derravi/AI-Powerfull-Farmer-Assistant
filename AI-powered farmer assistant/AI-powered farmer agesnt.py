# (1) Install required packages
!pip install google-generativeai --quiet
!pip install ipywidgets --quiet
!pip install deep-translator --quiet
!pip install pandas --quiet
!pip install requests --quiet

# (2) Import libraries
import google.generativeai as genai
import ipywidgets as widgets
from IPython.display import display, Markdown, HTML
from deep_translator import GoogleTranslator
import pandas as pd
import random
from datetime import datetime, timedelta
import requests
import json
import time

# (3) Set up Gemini API with proper error handling
API_KEY = "YOUT_GEMINY_API_KEY"  # Replace with your actual API key

try:
    genai.configure(api_key=API_KEY)
    # Updated model name to the current available model
    model = genai.GenerativeModel("gemini-1.0-pro")  # Using currently available model
    print("API connected successfully")
except Exception as e:
    print(f"API configuration error: {e}")
    model = None

# Initialize translator
translator = GoogleTranslator()

# (4) Enhanced translation function with caching
translation_cache = {}
def translate_text(text, dest_language='English'):
    """Translate text to the specified language with caching"""
    if not text or dest_language.lower() == 'english':
        return text

    cache_key = f"{text}_{dest_language}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]

    try:
        if dest_language.lower() == 'hindi':
            translated = GoogleTranslator(source='auto', target='hi').translate(text)
        elif dest_language.lower() == 'gujarati':
            translated = GoogleTranslator(source='auto', target='gu').translate(text)
        elif dest_language.lower() == 'punjabi':
            translated = GoogleTranslator(source='auto', target='pa').translate(text)
        elif dest_language.lower() == 'marathi':
            translated = GoogleTranslator(source='auto', target='mr').translate(text)
        elif dest_language.lower() == 'telugu':
            translated = GoogleTranslator(source='auto', target='te').translate(text)
        elif dest_language.lower() == 'tamil':
            translated = GoogleTranslator(source='auto', target='ta').translate(text)
        elif dest_language.lower() == 'kannada':
            translated = GoogleTranslator(source='auto', target='kn').translate(text)
        elif dest_language.lower() == 'bengali':
            translated = GoogleTranslator(source='auto', target='bn').translate(text)
        else:
            translated = text

        translation_cache[cache_key] = translated
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

# (5) Enhanced Databases with Fallback Data
# Weather Database (fallback when API fails)
weather_db = {
    'Rajkot': {
        'today': {'temp': 32, 'condition': 'Sunny', 'humidity': 45, 'wind': 12},
        'forecast': [
            {'day': 'Tomorrow', 'high': 34, 'low': 24, 'condition': 'Partly Cloudy'},
            {'day': 'Day 2', 'high': 33, 'low': 25, 'condition': 'Sunny'},
            {'day': 'Day 3', 'high': 35, 'low': 26, 'condition': 'Sunny'},
            {'day': 'Day 4', 'high': 36, 'low': 27, 'condition': 'Hot'},
            {'day': 'Day 5', 'high': 34, 'low': 26, 'condition': 'Partly Cloudy'}
        ]
    },
    'Default': {
        'today': {'temp': 30, 'condition': 'Sunny', 'humidity': 50, 'wind': 10},
        'forecast': [
            {'day': 'Tomorrow', 'high': 31, 'low': 23, 'condition': 'Partly Cloudy'},
            {'day': 'Day 2', 'high': 32, 'low': 24, 'condition': 'Sunny'},
            {'day': 'Day 3', 'high': 33, 'low': 25, 'condition': 'Sunny'},
            {'day': 'Day 4', 'high': 32, 'low': 24, 'condition': 'Partly Cloudy'},
            {'day': 'Day 5', 'high': 31, 'low': 23, 'condition': 'Cloudy'}
        ]
    }
}

# Tractor and Equipment Database
equipment_db = pd.DataFrame({
    'Equipment': ['Mahindra 575 DI', 'Sonalika DI 35', 'Swaraj 744 FE', 'John Deere 5050D', 'Eicher 380'],
    'Price (₹)': [650000, 585000, 720000, 825000, 695000],
    'GST (%)': [12, 12, 12, 12, 12],
    'Subsidy (%)': [40, 35, 30, 25, 30],
    'Govt Scheme': ['Rashtriya Krishi Vikas Yojana', 'Sub-Mission on Agricultural Mechanization',
                   'State Farm Mechanization Scheme', 'National Mission on Agricultural Extension',
                   'State Farm Mechanization Scheme'],
    'Contact': ['1800-425-1554', '1800-425-1555', '1800-425-1556', '1800-425-1557', '1800-425-1558']
})

# Direct Market Access Database
direct_market_db = pd.DataFrame({
    'Market Type': ['Company Direct', 'eNAM', 'FPO Collective', 'Local Mandi', 'Online Marketplace'],
    'Name': ['ITC Agri Business', 'eNAM National Market', 'Nav Maharashtra FPO', 'APMC Mumbai', 'Ninjacart'],
    'Products': ['All crops', 'All agricultural produce', 'Regional crops', 'All produce', 'Vegetables/Fruits'],
    'Contact': ['agri@itc.in', 'support@enam.gov.in', 'info@navmahafpo.in', 'apmc@mumbai.gov.in', 'farmers@ninjacart.in'],
    'Process': ['Contract farming', 'Online bidding', 'Collective selling', 'Auction system', 'Direct procurement'],
    'Language Support': ['English, Hindi', 'Multi-lingual', 'Marathi, Hindi', 'Local language', 'English']
})

# (6) Core Functions with Robust Error Handling
def safe_generate_content(prompt, max_retries=2):
    """Generate content with comprehensive error handling"""
    if not model:
        return None  # Will trigger fallback data

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e) or "404" in str(e):
                wait_time = (attempt + 1) * 3  # Exponential backoff
                print(f"API limit reached. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            print(f"Generation error: {str(e)}")
            return None
    return None

def get_weather_details(location):
    """Get weather details with API fallback"""
    # Try Gemini API first
    prompt = f"""
    Provide a concise 5-day weather forecast for {location} specifically for agricultural planning.
    Include temperature (min/max), rainfall probability, humidity, and wind speed.
    Format as a bulleted list with emojis.
    """

    api_response = safe_generate_content(prompt)
    if api_response:
        return api_response

    # Fallback to local database
    location_data = weather_db.get(location, weather_db['Default'])
    today = location_data['today']
    forecast = location_data['forecast']

    result = f"""
    **Current Weather in {location}** ⛅
    - Temperature: {today['temp']}°C
    - Conditions: {today['condition']}
    - Humidity: {today['humidity']}%
    - Wind Speed: {today['wind']} km/h

    **5-Day Forecast** 📅
    """

    for day in forecast:
        result += f"\n- {day['day']}: {day['high']}°C/{day['low']}°C, {day['condition']}"

    result += "\n\n(Note: Using fallback weather data)"
    return result

def get_equipment_info():
    """Get tractor and equipment information"""
    info = "### Agricultural Equipment Details 🚜\n"
    for _, row in equipment_db.iterrows():
        discounted_price = row['Price (₹)'] * (1 - row['Subsidy (%)']/100)
        info += f"""
        **{row['Equipment']}**
        - Base Price: ₹{row['Price (₹)']:,.2f}
        - GST: {row['GST (%)']}%
        - Govt Subsidy: {row['Subsidy (%)']}%
        - After Subsidy: ₹{discounted_price:,.2f}
        - Scheme: {row['Govt Scheme']}
        - Contact: {row['Contact']}
        """
    return info

def get_direct_market_options(product):
    """Get options to sell directly without middlemen"""
    matching_markets = direct_market_db[
        direct_market_db['Products'].str.contains(product, case=False) |
        (direct_market_db['Products'] == 'All crops') |
        (direct_market_db['Products'] == 'All produce')
    ]

    result = "### Direct Selling Options (No Middlemen) 🛒\n"

    if not matching_markets.empty:
        for _, row in matching_markets.iterrows():
            result += f"""
            **{row['Market Type']} - {row['Name']}**
            - Products: {row['Products']}
            - Process: {row['Process']}
            - Contact: {row['Contact']}
            - Languages: {row['Language Support']}
            """

    # Try to get AI-generated guidance
    prompt = f"""
    Provide 5 key steps for farmers to sell {product} directly to markets without middlemen.
    Include tips on quality standards and transportation.
    """
    guidance = safe_generate_content(prompt)

    if guidance:
        result += f"\n### Selling Guidance 💡\n{guidance}"
    else:
        result += f"""
        \n### Selling Guidance 💡
        1. Contact the buyers listed above to understand their requirements
        2. Ensure your {product} meets quality standards
        3. Arrange transportation to the market
        4. Complete necessary documentation
        5. Negotiate fair prices directly with buyers
        """

    return result

def get_price_forecast(product):
    """Get price forecasting with fallback"""
    # Try Gemini API first
    prompt = f"""
    Generate a 3-month price forecast for {product} in Indian markets.
    Include current trends, seasonal factors, and best selling times.
    Present in 5 clear bullet points.
    """

    api_response = safe_generate_content(prompt)
    if api_response:
        return api_response

    # Fallback data
    trends = {
        'Wheat': "Prices typically rise during winter months (Nov-Jan)",
        'Rice': "Prices stable post-harvest season (Oct-Dec)",
        'Tomato': "Prices volatile with frequent spikes during monsoon",
        'Potato': "Prices drop during peak harvest season (Jan-Mar)",
        'Cotton': "Prices influenced by international market trends",
        'Sugarcane': "Prices stable due to government MSP"
    }

    forecast = trends.get(product,
        f"Market trends for {product} vary seasonally. Check local mandi prices regularly.")

    return f"""
    ### Price Forecast for {product} 📈
    - {forecast}
    - Check eNAM portal for daily prices: https://enam.gov.in
    - Contact local agriculture office for MSP details
    - Consider storage options if prices are low
    - Explore alternative markets for better prices
    """

def get_enam_guidance():
    """Get eNAM guidance with fallback"""
    prompt = """
    Explain how to use eNAM platform in 5 simple steps for farmers.
    Include registration, listing products, and receiving payments.
    """

    api_response = safe_generate_content(prompt)
    if api_response:
        return api_response

    return """
    ### eNAM Guide 🌐
    1. Register on https://enam.gov.in with your Aadhaar and bank details
    2. Get your farm produce quality certified
    3. List your products on the platform
    4. Participate in online auctions
    5. Receive payment directly to your bank account

    For assistance, call eNAM helpline: 1800-425-1556
    """

def get_climate_advice(product, location):
    """Get climate advice with fallback"""
    prompt = f"""
    Provide 5 climate-smart farming tips for {product} in {location}.
    Include water conservation and pest management advice.
    """

    api_response = safe_generate_content(prompt)
    if api_response:
        return api_response

    return f"""
    ### Climate Advice for {product} in {location} 🌦️
    1. Monitor weather forecasts regularly
    2. Implement drip irrigation for water conservation
    3. Use organic mulch to retain soil moisture
    4. Rotate crops to maintain soil health
    5. Consult local KVK for region-specific advice
    """

def get_govt_scheme_info(scheme_name):
    """Get scheme info with fallback"""
    schemes = {
        'Direct Market Access Policy': """
        - Allows farmers to sell directly to consumers/businesses
        - Bypasses APMC mandis to avoid middlemen
        - Register on eNAM or with FPOs
        """,
        'Krishi Vigyan Kendras': """
        - Agricultural extension centers across India
        - Provide training and technology demonstrations
        - Contact local KVK for crop-specific advice
        """,
        'PM Fasal Bima Yojana': """
        - Crop insurance against natural calamities
        - Premium as low as 2% for food crops
        - Apply through Common Service Centers
        """,
        'Weather-based advisory apps': """
        - Meghdoot: IMD's weather app for farmers
        - Kisan Suvidha: Multi-lingual farming app
        - Download from Google Play Store
        """,
        'Farmer Producer Organizations': """
        - Collective farming for better bargaining
        - Government provides ₹15 lakh per FPO
        - Contact NABARD for registration
        """
    }

    return f"""
    ### {scheme_name} ℹ️
    {schemes.get(scheme_name, "Scheme details not available. Contact local agriculture office.")}
    """

# (7) Enhanced UI Components
# Language Selection
language_input = widgets.Dropdown(
    options=['English', 'Hindi', 'Gujarati', 'Punjabi', 'Marathi', 'Telugu', 'Tamil', 'Kannada', 'Bengali'],
    value='English',
    description="🌐 Language:",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='100%')
)

# Main Service Selection
service_input = widgets.Dropdown(
    options=[
        'Weather Forecast',
        'Farm Equipment Info',
        'Direct Market Access',
        'Price Forecasting',
        'eNAM Market Access',
        'Climate Impact Advice',
        'Government Schemes'
    ],
    value='Weather Forecast',
    description="🛠️ Service Needed:",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='100%')
)

# Location Input
location_input = widgets.Text(
    value='Rajkot',
    description="📍 Location:",
    placeholder="Enter city/village",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='100%')
)

# Product Input
product_input = widgets.Text(
    value='Tomato',
    description="🌱 Crop/Product:",
    placeholder="e.g., Wheat, Tomato",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='100%')
)

# Scheme Selection (visible only when government schemes selected)
scheme_input = widgets.Dropdown(
    options=[
        'Direct Market Access Policy',
        'Krishi Vigyan Kendras',
        'PM Fasal Bima Yojana',
        'Weather-based advisory apps',
        'Farmer Producer Organizations'
    ],
    value='Direct Market Access Policy',
    description="🏛️ Select Scheme:",
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='100%', display='none')
)

# Submit Button
submit_button = widgets.Button(
    description="Get Solutions",
    button_style='success',
    style={'button_color': '#2e7d32'},
    layout=widgets.Layout(width='100%', height='45px')
)

# Output Area
output = widgets.Output(layout={'border': '1px solid #81c784', 'margin-top': '10px'})

# (8) UI Interaction Logic
def on_service_change(change):
    """Show/hide relevant fields based on service selection"""
    if change['new'] == 'Government Schemes':
        scheme_input.layout.display = 'flex'
        product_input.layout.display = 'none'
    else:
        scheme_input.layout.display = 'none'
        product_input.layout.display = 'flex'

    if change['new'] in ['Weather Forecast', 'Farm Equipment Info']:
        product_input.layout.display = 'none'
    else:
        product_input.layout.display = 'flex'

service_input.observe(on_service_change, names='value')

# (9) Main Processing Function
def handle_request(b):
    output.clear_output()
    with output:
        language = language_input.value
        service = service_input.value
        location = location_input.value
        product = product_input.value
        scheme = scheme_input.value

        display(Markdown(f"### {translate_text('Processing your request...', language)}"))

        try:
            if service == 'Weather Forecast':
                display(Markdown(translate_text(f"### Weather Forecast for {location}", language)))
                weather_info = get_weather_details(location)
                display(Markdown(translate_text(weather_info, language)))

            elif service == 'Farm Equipment Info':
                display(Markdown(translate_text("### Agricultural Equipment with Subsidies", language)))
                equipment_info = get_equipment_info()
                display(Markdown(translate_text(equipment_info, language)))

            elif service == 'Direct Market Access':
                display(Markdown(translate_text(f"### Direct Selling Options for {product}", language)))
                market_info = get_direct_market_options(product)
                display(Markdown(translate_text(market_info, language)))

            elif service == 'Price Forecasting':
                display(Markdown(translate_text(f"### Price Forecast for {product}", language)))
                forecast = get_price_forecast(product)
                display(Markdown(translate_text(forecast, language)))

            elif service == 'eNAM Market Access':
                display(Markdown(translate_text("### eNAM Digital Market Guide", language)))
                enam_info = get_enam_guidance()
                display(Markdown(translate_text(enam_info, language)))

            elif service == 'Climate Impact Advice':
                display(Markdown(translate_text(f"### Climate Advice for {product} in {location}", language)))
                climate_info = get_climate_advice(product, location)
                display(Markdown(translate_text(climate_info, language)))

            elif service == 'Government Schemes':
                display(Markdown(translate_text(f"### {scheme} Details", language)))
                scheme_info = get_govt_scheme_info(scheme)
                display(Markdown(translate_text(scheme_info, language)))

            # Add additional resources
            display(Markdown(translate_text("""
            ### Additional Resources
            - [National Agricultural Market (eNAM)](https://enam.gov.in)
            - [Farmer Helpline](tel:18001801551)
            - [Weather Portal](https://mausam.imd.gov.in)
            - [Subsidy Portal](https://agricoop.gov.in)
            """, language)))

        except Exception as e:
            display(Markdown(translate_text("### Error Processing Request", language)))
            display(Markdown(translate_text(f"Please try again later. Error: {str(e)}", language)))

# (10) Display the UI
submit_button.on_click(handle_request)

# Create form with beautiful styling
form_title = widgets.HTML(
    value="""
    <div style="
        background: linear-gradient(135deg, #2e7d32, #81c784);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    ">
        <h1 style="margin:0; font-size:28px;">🌾 Kisan Saathi AI</h1>
        <p style="margin:5px 0 0; font-size:16px;">
            Your Complete Farming Companion - Market Access • Weather • Equipment • Schemes
        </p>
    </div>
    """
)

input_form = widgets.VBox([
    form_title,
    widgets.VBox([
        language_input,
        service_input,
        location_input,
        product_input,
        scheme_input,
        submit_button
    ], layout=widgets.Layout(
        padding='20px',
        width='100%'
    )),
    output
], layout=widgets.Layout(
    width='80%',
    margin='0 auto',
    border='1px solid #e0e0e0',
    border_radius='10px',
    box_shadow='0 4px 8px rgba(0,0,0,0.1)'
))

display(input_form)