# pip install cohere

import cohere
import json
from datetime import datetime

co = cohere.Client(
    api_key="",  # This is your trial API key
)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return str(obj)

current_time = datetime.now()
print(current_time.strftime('%Y-%m-%d %H:%M:%S'))
preamble = (
    f"You are Command R Plus, a large language model trained to have polite, helpful, inclusive conversations with people. People are looking for information that may need you to search online. Make an accurate and fast response. You must reply with user's original language."
    f"The current time in Toronto is {current_time}."
)
stream = co.chat_stream(
    model="command-r",
    message="现在多伦多是几点? 天气怎么样?",
    temperature=0.8,
    chat_history=[
        {
            "role": "User",
            "message": "This is a test message. Make a simple online search for me.",
        },
        {
            "role": "Chatbot",
            "message": "Of course! I'd be happy to assist you with an online search. Please provide the search terms or query, and I will find relevant results from the web.",
        },
    ],
    prompt_truncation="AUTO",
    connectors=[{"id": "web-search"}],
    preamble=preamble,
)

for event in stream:
    if event.event_type == "text-generation":
        print(event.text, end="")
    elif event.event_type == "search-results":
        for doc in event.documents:
            print(f"\n[{doc['title']}]({doc['url']})")
    elif event.event_type == "stream-end":
        # 1.json
        with open("1.json", "w", encoding="utf-8") as f:
            json.dump(
                event.__dict__, f, cls=CustomEncoder, ensure_ascii=False, indent=4
            )
        break
