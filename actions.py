import webbrowser
import datetime
import requests
import re

def execute_command(intent, user_text):
    # 1. YOUTUBE
    if intent == "open_youtube":
        # Ensure we don't crash if the query is empty
        query = user_text.replace("play", "").replace("on youtube", "").replace("search for", "").strip()
        if not query: query = "trending songs"
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Opening YouTube for: {query}"

    # 2. CALCULATOR
    elif intent == "calculator":
        # Cleaning the text for math evaluation
        clean_text = user_text.replace("plus", "+").replace("minus", "-").replace("multiply", "*").replace("divide", "/")
        math_expression = re.findall(r'[\d\+\-\*\/\.]+', clean_text)
        if math_expression:
            try:
                result = eval(math_expression[0])
                return f"The result is {result}"
            except:
                return "Could not calculate that math."
        return "Please provide a valid math expression."

    # 3. WEATHER
    elif intent == "weather":
        api_key = "db56b6fa376091ef41aace5d9df38fee"
        city = "Hubballi"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            data = requests.get(url).json()
            if data.get("main"):
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"The weather in {city} is {temp}°C with {desc}."
            return "Could not find weather data for this location."
        except:
            return "Could not connect to weather service."

    # 4. MAPS
    elif intent == "maps":
        webbrowser.open("https://www.google.com/maps")
        return "Opening Google Maps."

    # 5. TIME
    elif intent == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}"

    # 6. JOKE
    elif intent == "joke":
        return "Why did the computer go to the doctor? It had a virus!"

    # 7. GOOGLE
    elif intent == "open_google":
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    return "Command not recognized. Please try again."