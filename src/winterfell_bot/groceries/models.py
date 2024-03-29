from datetime import datetime
from settings import LIST_HEADER


class GroceryList:
    _id = None
    items = None

    def __init__(self, _id, items):
        self._id = _id
        self.items = items

    def __repr__(self):
        return f"<GroceryList _id={self._id}, items={len(self.items)}>"

    def save(self, collection):
        cleaned_items = set(self.items)
        self.items = sorted(list(cleaned_items))

        data = [item.to_json() for item in self.items]

        collection.replace_one(
            filter={"_id": self._id},
            replacement={"items": data},
            upsert=True
        )

    def check_items(self, items_to_check):
        for item in self.items:
            if item in items_to_check:
                item.set_as_checked()

    def display_list(self):
        if not self.items:
            return "Lista vazia"

        list_display = [item.display() for item in self.items]
        return LIST_HEADER + "\n".join(list_display)

    def clean_checked_items(self):
        self.items = [item for item in self.items if not item.checked]

    @staticmethod
    def get_object(collection, _id):
        obj = collection.find_one(_id)
        items = obj.get("items", [])
        if items:
            items = [GroceryItem(**item) for item in items]

        return GroceryList(_id=_id, items=items)

    @staticmethod
    def clean_all_items(collection, _id):
        collection.update_one(
            filter={"_id": _id},
            update={
                "$unset": {
                    "items": []
                }
            }
        )


class GroceryItem:
    name = None
    created_at = datetime.now()
    updated_at = None
    checked =  False

    def __init__(self, name, checked=False, created_at=None, updated_at=None):
        self.name = name.strip()
        self.checked = checked
        if created_at:
            self.created_at = created_at

        if updated_at:
            self.updated_at = updated_at

    def __repr__(self):
        return f"<GroceryItem name={self.name}, checked={self.checked}>"

    def __hash__(self):
        return hash(("name", self.name, "checked", self.checked))

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name and self.checked == other.checked


    def display(self):
        if self.checked:
            return "✅ " + self.name
        return self.name

    def set_as_checked(self):
        self.checked = True

    def to_json(self):
        return {
            "name": self.name,
            "checked": self.checked,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }
