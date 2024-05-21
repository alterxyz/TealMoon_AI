# Get gemini supported models with the API key
# pip install google-generativeai

import google.generativeai as genai
import pprint

# 直接设置 API 密钥
API_KEY = ""
genai.configure(api_key=API_KEY)

# 列出可用模型
print("Available models:")
for model in genai.list_models():
    pprint.pprint(model)
