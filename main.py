from pathlib import Path

import comment_json as cjson


class Recipe:
    def __init__(self, path: Path) -> None:
        with open(path) as f:
            self.json = cjson.load(f)

    def _find_property(self, recipe_dict, key):
        for _key, value in recipe_dict.items():
            if _key == key:
                return recipe_dict[_key]

            if not isinstance(value, dict):
                continue

            child_value = self._find_property(value, key)
            if child_value is not None:
                return child_value
        return None

    def find_property(self, key):
        return self._find_property(self.json, key)

    @property
    def tags(self) -> list[str]:
        return self.find_property("tags")

    @property
    def identifier(self) -> str:
        return self.find_property("identifier")

    @property
    def dummy_recipe(self) -> dict:
        return {
            "format_version": self.find_property("format_version"),
            "minecraft:recipe_shaped": {
                "description": { "identifier": self.identifier },
                "tags": [ "crafting_table" ],
                "pattern": [ "#" ],
                "key": { "#": { "item": "minecraft:barrier" } },
                "result": { "item": "minecraft:barrier" }
            }
        }

    def save(self, path: Path) -> None:
        with open(path, "w") as f:
            cjson.dump(self.dummy_recipe, f, ensure_ascii=False)


def create_dummy_recipes(folder_name) -> None:
    recipes = Path(folder_name)
    for recipe_path in recipes.glob("*.json"):
        recipe = Recipe(recipe_path)

        if "crafting_table" not in recipe.tags:
            continue

        recipe.save(Path("dummy") / recipe_path.name)


if __name__ == "__main__":
    create_dummy_recipes("recipes")
