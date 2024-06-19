# Dify chatbot through cli
# pip install dify-client

from dify_client import ChatClient


def main():
    api_key = ""  # Chatbot API Key
    chat_client = ChatClient(api_key)

    user_id = input("Enter your user ID: ")
    conversation_id = (
        None  # Optionally specify a conversation ID or create a new one each time
    )

    print("Start chatting (type 'exit' to end the conversation):")
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
                inputs={},
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


if __name__ == "__main__":
    main()
