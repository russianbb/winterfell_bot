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

    await app.send_message(group_id, grocery_list.display_list())



@app.on_message(filters.group & filters.command("add"))
async def add_item(client, message):
    group_id = str(message.chat.id)

    command_args = " ".join(message.command[1:])
    item_names = command_args.split(",")

    new_items = [GroceryItem(name=name) for name in item_names]

    grocery_list = GroceryList.get_object(db.groceries, group_id)
    grocery_list.items.extend(new_items)
    grocery_list.save(db.groceries)

    await app.send_message(group_id, grocery_list.display_list())

@app.on_message(filters.group & filters.command("check"))
async def check_item(client, message):
    group_id = str(message.chat.id)

    command_args = " ".join(message.command[1:])
    item_names = command_args.split(",")

    items = [GroceryItem(name=name) for name in item_names]

    grocery_list = GroceryList.get_object(db.groceries, group_id)
    grocery_list.check_items(items)
    grocery_list.save(db.groceries)

    await app.send_message(group_id, grocery_list.display_list())


@app.on_message(filters.group & filters.command("cleanall"))
async def clean_all_items(client, message):
    group_id = str(message.chat.id)

    GroceryList.clean_all_items(db.groceries, group_id)

    await app.send_message(group_id, "Lista excluída")


@app.on_message(filters.group & filters.command("clean"))
async def clean_checked_items(client, message):
    group_id = str(message.chat.id)

    grocery_list = GroceryList.get_object(db.groceries, group_id)
    grocery_list.clean_checked_items()
    grocery_list.save(db.groceries)

    await app.send_message(group_id, grocery_list.display_list())


app.run()
