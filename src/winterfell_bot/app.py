from pyrogram import Client, filters
from uvloop import install
from db import db
from groceries.models import GroceryItem, GroceryList

from settings import TELEGRAM_API_HASH, TELEGRAM_API_ID, TELEGRAM_BOT_TOKEN, LIST_HEADER

install()

app = Client(
    name="winterfell_groceries_list_bot",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_TOKEN,
)


@app.on_message(filters.group & filters.command("list"))
async def list_items(client, message):
    group_id = str(message.chat.id)
    grocery_list = GroceryList.get_object(db.groceries, group_id)

    await message.reply(grocery_list.display_list())



@app.on_message(filters.group & filters.command("add"))
async def add_item(client, message):
    group_id = str(message.chat.id)

    command_args = " ".join(message.command[1:])
    item_names = command_args.split(",")

    new_items = [GroceryItem(name=name) for name in item_names]

    grocery_list = GroceryList.get_object(db.groceries, group_id)
    grocery_list.items.extend(new_items)
    grocery_list.save(db.groceries)

    await message.reply(grocery_list.display_list())

@app.on_message(filters.group & filters.command("check"))
async def check_item(client, message):
    group_id = str(message.chat.id)

    command_args = " ".join(message.command[1:])
    item_names = command_args.split(",")

    items = [GroceryItem(name=name) for name in item_names]

    grocery_list = GroceryList.get_object(db.groceries, group_id)
    grocery_list.check_items(items)
    grocery_list.save(db.groceries)

    await message.reply(grocery_list.display_list())


@app.on_message(filters.group & filters.command("cleanall"))
async def clean_all_items(client, message):
    group_id = str(message.chat.id)
    query_params = {"group": group_id}

    db.posts.update_one(query_params, {"$unset": {"items": []}})

    await message.reply("Lista excluída.")


@app.on_message(filters.group & filters.command("clean"))
async def clean_checked_items(client, message):
    group_id = str(message.chat.id)
    query_params = {"group": group_id}

    query = db.posts.find_one(query_params)
    existing_items = query.get("items", None)

    if existing_items:
        keep_items = []
        for item in existing_items:
            if "✅" not in item:
                keep_items.append(item)

        db.posts.update_one(query_params, {"$set": {"items": keep_items}})
        data = LIST_HEADER + "\n".join(keep_items)

    else:
        data = "Lista vazia"

    await message.reply(data)


app.run()
