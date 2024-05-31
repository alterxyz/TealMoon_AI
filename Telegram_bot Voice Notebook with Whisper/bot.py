import os
from telegram import Update, ReplyKeyboardRemove, MessageEntity
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime
from audio_whisper import transcribe_audio  # Import the transcribe_audio function

USER_DIRECTORY = "user_data"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Send me an audio file or a voice message, and I will transcribe it for you.")

async def save_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_folder = os.path.join(USER_DIRECTORY, str(user_id))
    audio_folder = os.path.join(user_folder, "audio_files")
    transcript_folder = os.path.join(user_folder, "tg_transcript")
    audio_message_id = update.message.message_id

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
    if not os.path.exists(transcript_folder):
        os.makedirs(transcript_folder)

    if update.message.audio:
        audio_file = update.message.audio
        file_type = "audio"
        file_id = audio_file.file_id
        file_extension = os.path.splitext(audio_file.file_name)[1] if audio_file.file_name else ".mp3"
        file_name = audio_file.file_name if audio_file.file_name else f"{file_id}{file_extension}"
    elif update.message.voice:
        audio_file = update.message.voice
        file_type = "voice"
        file_id = audio_file.file_id
        file_extension = ".ogg"
        timestamp = datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
        file_name = f"{timestamp}{file_extension}"
    else:
        await update.message.reply_text('Please send an audio file or a voice message.')
        return

    audio_file = await audio_file.get_file()
    audio_file_path = os.path.join(audio_folder, file_name)
    await audio_file.download_to_drive(audio_file_path)

    

    send_message = await update.message.reply_text(f"Transcribing the {file_name}.\n\nPlease wait...", reply_to_message_id=audio_message_id)
    context.user_data["send_message_id"] = send_message.message_id # Save the message ID for deletion later


    # Call the transcribe_audio function and get the path to the TXT file
    txt_file_path = transcribe_audio(audio_file_path)

    if txt_file_path:
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            transcription = txt_file.read()
        # await update.message.reply_text(f"{file_name}:\n\n{transcription}", parse_mode="MarkdownV2", reply_to_message_id=audio_message_id)
        # Instead, we update the send_message with the transcription
        spoiler_entity = MessageEntity(
            type=MessageEntity.SPOILER,
            offset=0,  # 剧透文本在消息中的起始位置
            length=len(txt_file_path)  # 剧透文本的长度
        )
        await send_message.edit_text(f"{txt_file_path}\nTranscribed.\nReply to this message with your new text to update the transcription.", entities=[spoiler_entity])
        transcribe_text = await update.message.reply_text(f"{transcription}", parse_mode="MarkdownV2", reply_to_message_id=audio_message_id)
        context.user_data["transcribe_text_id"] = transcribe_text.message_id
        context.user_data["txt_file_path"] = txt_file_path # Store the txt_file_path
    else:
        await send_message.edit_text("Transcription failed. Please try {file_name} again.", reply_to_message_id=audio_message_id)

async def update_transcription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("txt_file_path"):
        new_transcription = update.message.text
        txt_file_path = context.user_data["txt_file_path"]
        
        try:
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(new_transcription)
            # await update.message.reply_text("Transcription updated successfully!")
            await update.message.delete()  # Delete the user's message
            # Optionally update the displayed transcription:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=context.user_data["transcribe_text_id"],
                text=new_transcription
            )
        except Exception as e:
            await update.message.reply_text(f"Error updating transcription: {str(e)}")
    else:
        await update.message.reply_text("Please transcribe an audio first.")




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    tg_token = "YOUR_BOT_TOKEN"
    application = Application.builder().token(tg_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, save_audio))
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY, update_transcription))

    application.add_handler(CommandHandler("cancel", cancel))

    application.run_polling()

if __name__ == "__main__":
    main()