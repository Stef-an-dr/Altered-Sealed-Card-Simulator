import random
from collections import defaultdict
from pathlib import Path
import json
from typing import Any  # <-- you used Any in a type hint

SCRIPT_DIR = Path(__file__).resolve().parent
DB_ROOT = SCRIPT_DIR / "Altered-TCG-Card-Database" / "SETS"

card_packs = {
    "Beyond The Gates": "CORE",
    "Trial By Frost": "ALIZE",
    "Whispers From The Maze": "BISE",
    "Skybound Odyssey": "CYCLONE",
}
hero_numbers = {
    "Beyond The Gates": (1, 3),
    "Trial By Frost": (1, 3),
    "Whispers From The Maze": (1, 3),
    "Skybound Odyssey": (65, 65),
}
factions = ["AX", "BR", "LY", "MU", "OR", "YZ"]

def main():
    packs = {
        "Beyond The Gates": 0,
        "Trial By Frost": 0,
        "Whispers From The Maze": 0,
        "Skybound Odyssey": 100,
    }
    # counts grouped by set
    results: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for set_name in packs.keys():
        for _ in range(packs[set_name]):
            # Hero
            hero_card = get_hero_code(set_name)
            if set_name in ("Beyond The Gates", "Trial By Frost", "Whispers From The Maze"):
                results["Beyond The Gates"][hero_card] += 1
            else:
                results[set_name][hero_card] += 1
            # 8 commons
            for _ in range(8):
                cf = random.choice(factions)
                common_code = f"{get_full_set_code(set_name)}{cf}_{get_card_number(set_name, cf)}_C"
                results[set_name][common_code] += 1

            # 3 rares
            for _ in range(3):
                rf = random.choice(factions)
                rare_code = f"{get_full_set_code(set_name)}{rf}_{get_card_number(set_name, rf)}_R{random.choice(['1','2'])}"
                results[set_name][rare_code] += 1


    # use_sets = [name for name, counts in results.items() if counts]

    # # Load EN JSON for only the sets used
    # files = load_english_files_for(card_packs, use_sets)

    # # Build @id -> imagePath index per set (O(total cards) once)
    # image_index = build_image_index_by_id(files)


    # Collect image URLs using @id: key is "/cards/<code>"
    images: list[tuple[int, str | None]] = []
    for set_name, codes in results.items():
        for code, n in sorted(codes.items()):
            # key = f"/cards/{code}"
            # url = image_index.get(set_name, {}).get(key)  # None if not found
            # images.append((n, url))
            # print(f"{n} {code} {url}")
            print(f"{n} {code} ")


def get_hero_code(set_name: str):
    hero_lo, hero_hi = hero_numbers[set_name]
    if set_name == "Skybound Odyssey":
        return f"{get_full_set_code(set_name)}{random.choice(factions)}_{random.randint(hero_lo, hero_hi)}_C"
    elif set_name in ("Beyond The Gates", "Trial By Frost", "Whispers From The Maze"):
        return f"{get_full_set_code('Beyond The Gates')}{random.choice(factions)}_0{random.randint(hero_lo, hero_hi)}_C"
    return "test"

def get_card_number(set_name: str, faction: str):
    if set_name == "Beyond The Gates":
        value = random.randint(4, 30)
        if value < 10:
            value = "0" + str(value)  # BTG uses 0-padded numbers for 4..9
        return value
    elif set_name == "Trial By Frost":
        if faction in ("MU", "LY"):
            return random.randint(31, 45)  # These two dont have a 
        elif faction in ("OR"):
            return random.randint(33, 47)  # Honestly no clue why this is like this
        else:
            return random.randint(32, 46)
    elif set_name == "Whispers From The Maze":
        return random.randint(49, 63) # 48 is kuroakami so it gets skipped
    elif set_name == "Skybound Odyssey":  
        if faction == "AX":
            return pick_from_nonoverlapping([(66, 75), (77, 82)]) # For Skybound Axiom has no card 76
        else:
            return random.randint(66, 82) #64 is sofia, #65 is heroes

def get_full_set_code(set_name: str):
    return f"ALT_{card_packs.get(set_name)}_B_"

def pick_from_nonoverlapping(ranges: list[tuple[int, int]]) -> int:
    total = sum(hi - lo + 1 for lo, hi in ranges)
    k = random.randrange(total)
    for lo, hi in ranges:
        span = hi - lo + 1
        if k < span:
            return lo + k
        k -= span

    return 0  # should never be reached

def load_english_files_for(card_packs: dict[str, str], use_sets: list[str]) -> dict[str, list[dict[str, Any]]]:
    """
    Load <CODE>/<CODE>_EN.json only for sets in use_sets.
    Returns: files[set_name] -> list[card dicts]
    """
    files: dict[str, list[dict[str, Any]]] = {}
    for set_name in use_sets:
        code = card_packs[set_name]
        path = DB_ROOT / code / f"{code}_EN.json"
        cards = json.loads(path.read_text(encoding="utf-8"))
        files[set_name] = cards  # your JSON is a plain list
    return files

def build_image_index_by_id(files: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, str]]:
    """
    Build image_index[set_name][@id] -> image URL
    """
    image_index: dict[str, dict[str, str]] = {}
    for set_name, cards in files.items():
        mapping: dict[str, str] = {}
        for card in cards:
            aid = card.get("@id")  # e.g. "/cards/ALT_CORE_B_AX_04_C"
            if not aid:
                continue
            img = card.get("imagePath")
            if img:
                mapping[aid] = img
        image_index[set_name] = mapping
    return image_index

if __name__ == "__main__":
    main()
