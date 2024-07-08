from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo

# Initialize MongoDB client
mongo_client = pymongo.MongoClient("mongodb+srv://tanjiro1564:tanjiro1564@cluster0.pp5yz4e.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["telegram_bot"]
character_collection = db["selected_characters"]

# Initialize your Pyrogram Client
app = Client(
    "fighting_bot",
    bot_token="7367261820:AAFjNjDCOczOGWLQXOmWVkwUKuvKVDuloPg",
    api_id=28122413,
    api_hash="750432c8e1b221f91fd2c93a92710093"
)

# Handle /start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    user_id = message.from_user.id
    if character_collection.find_one({"user_id": user_id}):
        message.reply_text("You have already selected a character!")
    else:
        welcome_message = "🍥 Welcome to the World of One Piece! 🍥\n\n" \
                          "🌟 Become a pirate, Fulfill Your Destiny! 🌟\n\n" \
                          "Click the button below to choose your first pirate character:"
        enter_button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Enter", callback_data="choose_character")]]
        )
        message.reply_text(welcome_message, reply_markup=enter_button)

# Handle callback from "Enter" button
@app.on_callback_query(filters.regex("^choose_character$"))
def choose_character_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if character_collection.find_one({"user_id": user_id}):
        callback_query.answer("You have already selected a character!")
    else:
        character_message = "Choose your first pirate:"
        character_buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Luffy", callback_data="select_luffy")],
                [InlineKeyboardButton("Zoro", callback_data="select_zoro")],
                [InlineKeyboardButton("Sanji", callback_data="select_sanji")],
            ]
        )
        callback_query.message.edit_text(character_message, reply_markup=character_buttons)

# Handle character selection callbacks
@app.on_callback_query(filters.regex("^select_(luffy|zoro|sanji)$"))
def select_character_callback(client, callback_query):
    selected_character = callback_query.data.split("_")[1].capitalize()  # Extract selected character
    user_id = callback_query.from_user.id
    if character_collection.find_one({"user_id": user_id}):
        callback_query.answer("You have already selected a character!")
    else:
        character_collection.insert_one({"user_id": user_id, "character": selected_character})
        confirmation_message = f"You've selected {selected_character} as your first pirate!"
        callback_query.message.edit_text(confirmation_message)

# Handle /shop command
@app.on_message(filters.command("shop"))
def shop_command(client, message):
    shop_message = "Welcome to the Pirate Shop!\n\n" \
                   "Choose what you want to buy:"
    shop_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Food", callback_data="buy_food")],
            [InlineKeyboardButton("Sword", callback_data="buy_sword")],
            [InlineKeyboardButton("Gun", callback_data="buy_gun")],
            [InlineKeyboardButton("Dress", callback_data="buy_dress")],
        ]
    )
    message.reply_text(shop_message, reply_markup=shop_buttons)

# Run the bot
if __name__ == "__main__":
    app.run()
