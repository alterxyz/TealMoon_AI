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
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return str(obj)
        
stream = co.chat_stream(
    model='command-r-plus',
    message='How\'s weather today in Toronto?',
    temperature=0.8,
    chat_history=[{"role": "User", "message": "This is a test message. Make a simple online search for me."}, {"role": "Chatbot", "message": "Of course! I\'d be happy to assist you with an online search. Please provide the search terms or query, and I will find relevant results from the web."}],
    prompt_truncation='AUTO',
    connectors=[{"id": "web-search"}]
)

for event in stream:
    if event.event_type == "text-generation":
        print(event.text, end='')
    elif event.event_type == "search-results":
        for doc in event.documents:
            print(f"\n[{doc['title']}]({doc['url']})")
    elif event.event_type == "stream-end":
        # 1.json
        with open("1.json", "w", encoding="utf-8") as f:
            json.dump(event.__dict__, f, cls=CustomEncoder, ensure_ascii=False, indent=4)
        break

