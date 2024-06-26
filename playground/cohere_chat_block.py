# python -m pip install cohere --upgrade

import cohere
import datetime
import chardet

co = cohere.Client(
    api_key="",
)


def cohere_chat_block(usermessage):

    response = co.chat(
        chat_history=[
            {
                "role": "USER",
                "message": "This is a test message. Make a simple online search for me.",
            },
            {
                "role": "CHATBOT",
                "message": "Of course! I'd be happy to help you with a simple online search. Please provide the search query or topic you would like me to search for, and I will find relevant information from reliable online sources and summarize it for you.",
            },
        ],
        message=usermessage,
        model="command-r",
        temperature=0.3,
        connectors=[{"id": "web-search"}],
    )

    # print(response.text)

    for doc in response.documents:
        print(f"\n[{doc['title']}]({doc['url']})")

    return response.text


def r(usermessage):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    preamble = (
        f"You are Command R, a large language model trained to have polite, helpful, inclusive conversations with people. People are looking for information that may need you to search online. Make an accurate and fast response. You must reply with user's original language."
        f"The current time in Toronto is {current_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')}, "
        f"in California is {current_time.astimezone(datetime.timezone(datetime.timedelta(hours=-7))).strftime('%Y-%m-%d %H:%M:%S')}, "
        f"and in China is {current_time.astimezone(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')}."
    )
    r = co.chat(
        model="command-r-plus",
        message=usermessage,
        temperature=0.4,
        chat_history=[
            {
                "role": "USER",
                "message": "This is a test message. Make a simple online search for me.",
            },
            {
                "role": "CHATBOT",
                "message": "Of course! I'd be happy to help you with a simple online search. Please provide the search query or topic you would like me to search for, and I will find relevant information from reliable online sources and summarize it for you.",
            },
        ],
        prompt_truncation="AUTO",
        connectors=[{"id": "web-search"}],
        citation_quality="fast",
        preamble=preamble,
    )

    s = r.text
    # 查看字符串的类型
    print("类型:", type(s))

    # 查看字符串的具体内容及其编码（repr() 用于显示字符串的原始表示）
    print("内容:", repr(s))
    byte_data = s.encode()
    print("原始编码:", byte_data)

    # 检测编码
    result = chardet.detect(byte_data)
    encoding = result['encoding']
    confidence = result['confidence']

    print(f"检测到的编码: {encoding}")
    print(f"置信度: {confidence}")
    # source = "\n".join(f"[{doc['title']}]({doc['url']})" for doc in r.documents)
    # full_response = f"{s}\n{source}\n"
    # print(full_response.encode("utf-8").decode("utf-8"))


def clean_text(text):
    """Clean up the garbled code in the UTF-8 encoded Chinese string.

    Args:
      text: String that needs to be cleaned.

    Returns:
      The cleaned string, if garbled code is detected, a prompt message is added at the end.
    """
    if "�" in text:
        # Use re.sub to clean up garbled code
        cleaned_text = re.sub(r"�.*?([，。！？；：]|$)", r"\1", text)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
        print(f"\n---------\nOriginal text:\n{text}\n---------")
        return cleaned_text + "\n\n~~(乱码已去除，可能存在错误，请注意)~~"
    else:
        return text


if __name__ == "__main__":
    usermessage = input("Enter your message: ")
    m = cohere_chat_block(usermessage)
    # print(r(usermessage))
    print(clean_text(m))
