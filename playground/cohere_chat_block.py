# python -m pip install cohere --upgrade

import cohere

co = cohere.Client(
    api_key="",
)

response = co.chat(
    chat_history=[
        {"role": "USER", "message": "This is a test message. Make a simple online search for me."},
        {
            "role": "CHATBOT",
            "message": "Of course! I'd be happy to help you with a simple online search. Please provide the search query or topic you would like me to search for, and I will find relevant information from reliable online sources and summarize it for you.",
        },
    ],
    message="This is a test message, just reply me hello world.",
    model='command-r-plus',
    temperature=0.3,
    connectors=[{"id": "web-search"}]
)

print(response.text)

for doc in response.documents:
    print(f"\n[{doc['title']}]({doc['url']})")

'''
Example:

Today in Toronto, the weather is expected to be very warm and humid, with a high of 87°F (30°C) and a low of 72°F (22°C). There is a risk of thunderstorms in the afternoon and a 30% chance of showers in the evening. The Air Quality Health Index is expected to be in the high-risk category, with high levels of air pollution. It is recommended that you stay hydrated and reduce your time spent outside if you experience any negative symptoms due to the weather conditions.

[Toronto, ON - 7 Day Forecast - Environment Canada](https://weather.gc.ca/city/pages/on-143_metric_e.html)

[Toronto, Ontario 7 Day Weather Forecast - The Weather Network](https://www.theweathernetwork.com/ca/weather/ontario/toronto?_guid_iss_=1)

[Toronto, Ontario Hourly Weather Forecast - The Weather Network](https://www.theweathernetwork.com/ca/hourly-weather-forecast/ontario/toronto?_guid_iss_=1)

[Toronto, Ontario, Canada Weather Forecast | AccuWeather](https://www.accuweather.com/en/ca/toronto/m5h/weather-forecast/55488)

---

Hello World!
'''
