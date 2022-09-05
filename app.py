import imp
from os import getenv
from pyrogram import Client, filters
from db import db

from settings import TELEGRAM_API_HASH, TELEGRAM_API_ID, TELEGRAM_BOT_TOKEN

app = Client(
    name="winterfell_groceries_list_bot",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_TOKEN,
)


@app.on_message(filters.group & filters.command("list"))
def list_items(client, message):
    group_id = str(message.chat.id)

    query_params = {"group": group_id}
    query = db.posts.find_one(query_params)

    items = query.get("items", "Lista vazia")
    data = "\n".join(items)

    message.reply(data)


@app.on_message(filters.group & filters.command("add"))
def add_item(client, message):
    group_id = str(message.chat.id)

    query_params = {"group": group_id}
    new_item = " ".join(message.command[1:])

    db.posts.update_one(
        query_params,
        {"$push": {"items": new_item}},
    )

    message.reply("Adicionado ✅")


app.run()
