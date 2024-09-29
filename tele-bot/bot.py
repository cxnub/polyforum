import os

import dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

dotenv.load_dotenv()

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.getenv("subscribe_key")
pnconfig.publish_key = os.getenv("publish_key")
pnconfig.user_id = "server"
pubnub = PubNub(pnconfig)


TOKEN = os.getenv("TOKEN")


# Global variable to store the user count
user_count = 0


def here_now_callback(result, status):
    global user_count  # Use global to store the value in an external variable
    if status.is_error():
        print("here_now error: %s" % status)
        return

    user_count = 0  # Reset user count before updating

    for channel_data in result.channels:
        print(f"Channel: {channel_data.channel_name}, User Count: {channel_data.occupancy}")
        # Update the user_count by summing the occupancy of all channels
        user_count += channel_data.occupancy


async def letsgophishing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != int(837462990):
        await update.message.reply_text("Peasants are not allowed to use this command!")
        return

    pubnub.signal().channel("polyforum").message("phish").sync()

    # PubNub call
    pubnub.here_now().channels(["polyforum"]).include_state(
        True
    ).pn_async(here_now_callback)

    await update.message.reply_text(f"sent! User count: {user_count}")


async def gethackedlist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # PubNub call
    pubnub.here_now().channels(["polyforum"]).include_state(True).pn_async(
        here_now_callback
    )

    await update.message.reply_text(f"User count: {user_count}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("letsgophishing", letsgophishing))
app.add_handler(CommandHandler("gethackedlist", gethackedlist))

app.run_polling()
