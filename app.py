from pyrogram import Client, filters
from db import db

from settings import TELEGRAM_API_HASH, TELEGRAM_API_ID, TELEGRAM_BOT_TOKEN, LIST_HEADER

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

    items = query.get("items")
    if items:
        data = LIST_HEADER + "\n".join(items)
    else:
        data = "Lista vazia"

    message.reply(data)


@app.on_message(filters.group & filters.command("add"))
def add_item(client, message):
    command_args = " ".join(message.command[1:])
    new_items = command_args.split(",")
    new_items = [new_item.strip() for new_item in new_items]

    group_id = str(message.chat.id)
    query_params = {"group": group_id}

    db.posts.update_one(
        query_params, {"$push": {"items": {"$each": new_items, "$sort": 1}}}
    )

    query = db.posts.find_one(query_params)
    items = query.get("items")
    data = LIST_HEADER + "\n".join(items)

    message.reply(data)


@app.on_message(filters.group & filters.command("check"))
def check_item(client, message):
    command_args = " ".join(message.command[1:])
    check_items = command_args.split(",")
    check_items = [new_item.strip() for new_item in check_items]

    group_id = str(message.chat.id)
    query_params = {"group": group_id}
    query = db.posts.find_one(query_params)

    existing_items = query.get("items", None)
    if existing_items:
        for key, value in enumerate(existing_items):
            if value in check_items:
                existing_items[key] = "✅ " + value

        existing_items.sort()

        db.posts.update_one(query_params, {"$set": {"items": existing_items}})
        data = LIST_HEADER + "\n".join(existing_items)

    else:
        data = "Lista vazia"

    message.reply(data)


@app.on_message(filters.group & filters.command("clean"))
def clean_list(client, message):
    group_id = str(message.chat.id)
    query_params = {"group": group_id}

    db.posts.update_one(query_params, {"$unset": {"items": []}})

    message.reply("Lista excluída.")


app.run()
