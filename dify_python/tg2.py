import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import dify_tm_1 as DifyTM
from dify_client import ChatClient # pip install python-telegram-bot --upgrade

# Initialize Chat Client
api = "app-xxxxxxxxxxxxxxxxxxxxxxxx"
base_url = "https://api.dify.ai/v1"
chat_client = ChatClient(api)
chat_client.base_url = base_url
tg_token = "7110895550:AAEUo0aFA1nGkfDw0QgHD8GoiEvFtyPi_yc"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the states
PARAM, CHAT = range(2)

# Function to start setting parameters


async def start_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    parameters = DifyTM.init_parameters()  # Retrieve the parameters dynamically
    context.user_data["parameters"] = parameters
    context.user_data["setted_parameters"] = {}
    context.user_data["index"] = 0
    context.user_data["mode"] = "set"  # Set mode to 'set'
    return await ask_next_param(update, context)


# Function to ask for the next parameter


async def ask_next_param(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    index = context.user_data["index"]
    parameters = context.user_data["parameters"]

    if index >= len(parameters):
        await update.message.reply_text("All parameters have been set.")
        logger.info("Set Parameters: %s", context.user_data["setted_parameters"])
        context.user_data["mode"] = "idle"  # Transition to idle mode
        return ConversationHandler.END

    param = parameters[index]
    input_type, details = next(iter(param.items()))
    context.user_data["current_param"] = details["variable"]

    prompt = details["label"]
    if input_type == "select":
        options_str = ", ".join(details["options"])
        prompt += f" ({options_str})"

    if "required" in details and not details["required"]:
        prompt += "\n(Optional field, press /None to skip.)"

    await update.message.reply_text(prompt, reply_markup=ReplyKeyboardRemove())
    return PARAM


# Function to set the parameter based on user input
async def set_param(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    index = context.user_data["index"]
    parameters = context.user_data["parameters"]
    param = parameters[index]
    input_type, details = next(iter(param.items()))
    user_input = update.message.text

    if "required" in details and not details["required"] and user_input == "":
        context.user_data["setted_parameters"][details["variable"]] = None
    else:
        if input_type == "select":
            if user_input not in details["options"]:
                await update.message.reply_text("Invalid option, please try again.")
                return PARAM
            context.user_data["setted_parameters"][details["variable"]] = user_input

        elif input_type in ["text-input", "paragraph"]:
            context.user_data["setted_parameters"][details["variable"]] = user_input

        elif input_type == "number":
            try:
                user_input = int(user_input)
                context.user_data["setted_parameters"][details["variable"]] = user_input
            except ValueError:
                await update.message.reply_text("Invalid number, please try again.")
                return PARAM

    context.user_data["index"] += 1
    return await ask_next_param(update, context)


# Function to handle /None command
async def none_param(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    index = context.user_data["index"]
    parameters = context.user_data["parameters"]
    param = parameters[index]
    details = next(iter(param.items()))[1]

    context.user_data["setted_parameters"][details["variable"]] = ""
    context.user_data["index"] += 1

    return await ask_next_param(update, context)


# Function to view set parameters
async def view_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    setted_parameters = context.user_data.get("setted_parameters", {})
    if not setted_parameters:
        await update.message.reply_text("No parameters have been set yet.")
    else:
        params_view = "\n".join(
            [f"{key}: {value}" for key, value in setted_parameters.items()]
        )
        await update.message.reply_text(f"Current parameters:\n{params_view}")
    return PARAM if context.user_data["mode"] == "set" else ConversationHandler.END


# Function to start the chat
async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (
        "setted_parameters" not in context.user_data
        or not context.user_data["setted_parameters"]
    ):
        await update.message.reply_text("Please set parameters first using /set.")
        return ConversationHandler.END
    context.user_data["conversation_id"] = None
    context.user_data["mode"] = "chat"  # Set mode to 'chat'
    await update.message.reply_text(
        "You can now chat with me. Type your messages directly."
    )
    return CHAT


# Function to handle chat messages
async def handle_chat_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    if context.user_data.get("mode") != "chat":
        await update.message.reply_text(
            "Please use /set to set parameters first or use /chat to start a chat session."
        )
        return ConversationHandler.END

    tg_user_id = "tg" + str(update.message.from_user.id)
    query = update.message.text
    chat_response = chat_client.create_chat_message(
        inputs=context.user_data["setted_parameters"],
        query=query,
        user=tg_user_id,
        response_mode="blocking",
        conversation_id=context.user_data.get("conversation_id"),
    )
    chat_response.raise_for_status()
    response_data = chat_response.json()
    if context.user_data["conversation_id"] is None:
        context.user_data["conversation_id"] = response_data.get(
            "conversation_id", None
        )
    await update.message.reply_text(
        "Bot: " + response_data.get("answer", "No response")
    )
    return CHAT


# Function to cancel the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Operation cancelled.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Main function
def main() -> None:
    application = Application.builder().token(tg_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("set", start_set)],
        states={
            PARAM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_param),
                CommandHandler("None", none_param),
                CommandHandler("view_set", view_set),
            ],
            CHAT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat_message)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,  # Allow users to reenter the conversation in different modes
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("chat", start_chat))  # Start chat mode
    application.add_handler(
        CommandHandler("view_set", view_set)
    )  # Ensure it can be used globally

    # To handle messages when not in conversation
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat_message)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
