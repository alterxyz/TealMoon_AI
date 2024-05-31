import dify_client as dify
from dify_client import ChatClient
import json
from datetime import datetime

api = "app-xxxxxxxxxxxxxxxxxxx"
api_info = api + ".json"
base_url = "https://api.dify.ai/v1"
mine = dify.DifyClient(api)
mine.base_url = base_url


def init_api(api_key, base_url):
    response = mine.get_application_parameters("user").json()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "api_key": api_key,
        "base_url": base_url,
        "timestamp": timestamp,
        "response": response,
    }
    try:
        with open(api_info, "r") as file:
            summary_data = json.load(file)
    except FileNotFoundError:
        summary_data = []
    summary_data.append(result)
    with open(api_info, "w") as file:
        json.dump(summary_data, file, indent=4)


def init_parameters():
    # Get the parameters need from the api_info, only load "user_input_form", just load the last one
    init_api(api, base_url)
    with open(api_info, "r") as file:
        summary_data = json.load(file)
        parameters = summary_data[-1]["response"]["user_input_form"]
        # Access the first element of the list
        return parameters


def cli_set_application_parameters():
    # 初始化参数
    parameters = init_parameters()
    # 用于存储用户设置的参数
    setted_parameters = {}

    # 遍历所有参数
    for param in parameters:
        # 获取输入类型和详情
        input_type, details = next(iter(param.items()))
        # 构造基本提示信息
        prompt = f"{details['label']}"

        # 如果输入类型为选择题（下拉菜单）
        if input_type == "select":
            # 构造选项字符串
            options_str = ", ".join(details["options"])
            # 更新提示信息，包括所有选项
            prompt += f" ({options_str})"

        # 持续请求用户输入直到有效
        while True:

            # 获取输入. 如果可选, 则提醒"可选"
            if "required" in details and not details["required"]:
                print("\nOptional field, press Enter to skip.")
            user_input = input(f"\n{prompt}\n> Your choice: ")
            if "required" in details and not details["required"] and user_input == "":
                setted_parameters[details["variable"]] = None
                break

            # 验证并处理不同类型的输入
            if input_type == "select" and user_input in details["options"]:
                # 对于选择题，验证用户输入是否为提供的选项之一
                setted_parameters[details["variable"]] = user_input
                break

            elif input_type == "text-input" or input_type == "paragraph":
                # 对于文本输入，直接保存
                setted_parameters[details["variable"]] = user_input
                break

            elif input_type == "number":
                # 对于数字输入，尝试转换为整数
                try:
                    user_input = int(user_input)
                    setted_parameters[details["variable"]] = user_input
                    break
                except ValueError:
                    # 如果转换失败，提示错误信息
                    print("Error, try again")
            else:
                # 如果输入不符合任何预期，提示错误
                print("Error, try again")
    return setted_parameters


def cli_chat(setted_parameters):
    conversation_id = None
    chat_client = ChatClient(api)
    chat_client.base_url = base_url
    user_id = input("Enter your user ID: ")
    print("Start chatting (type 'exit' to end the conversation):\n")
    try:
        while True:
            query = input("You: ")
            if query.lower() == "exit":
                print("Chat ended.")
                break
            elif query.lower() == "clear":
                conversation_id = None
                print("Conversation reset. Starting a new conversation.")

                continue

            # Send chat message. If conversation_id is None, it's a new conversation
            chat_response = chat_client.create_chat_message(
                inputs=setted_parameters,
                query=query,
                user=user_id,
                response_mode="blocking",
                conversation_id=conversation_id,
            )
            chat_response.raise_for_status()
            response_data = chat_response.json()

            # Update conversation_id for subsequent messages
            if conversation_id is None:
                conversation_id = response_data.get("conversation_id", None)

            print("Bot:", response_data.get("answer", "No response"))

    except KeyboardInterrupt:
        print("\nConversation interrupted by user.")
    except Exception as e:
        print("An error occurred:", e)


def dify_select_param(detail):
    options = []
    options.append(detail["label"])
    for option in detail["options"]:
        options.append(option)
    return options


if __name__ == "__main__":
    print(init_parameters())
    setted_parameters = cli_set_application_parameters()
    print(setted_parameters)
    cli_chat(setted_parameters)
