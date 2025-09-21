import random
from collections import defaultdict

card_packs = {"Beyond The Gates" : "ALT_CORE_B_", "Trial By Frost" : "ALT_ALIZE_B_", "Whispers From The Maze" : "ALT_BISE_B_", "Skybound Odyssey" : "ALT_CYCLONE_B_"}
hero_numbers = {"Beyond The Gates" : (1,3), "Trial By Frost" : (1,3), "Whispers From The Maze" : (1,3), "Skybound Odyssey" : (65,65)}
factions = ["AX", "BR", "LY", "MU", "OR", "YZ"]

def main():
    packs = {"Beyond The Gates" : 10, "Trial By Frost" : 0, "Whispers From The Maze" : 0, "Skybound Odyssey" : 0}    
    results = defaultdict(int)
    for packType in packs.keys():
        for _ in range(packs[packType]):
            #Generate hero card
            results[get_hero_code(packType)] += 1 
            #Generate 8 common cards
            for common_cards in range(8):
                card_faction = random.choice(factions)
                common_card_code = f"{card_packs.get(packType)}{card_faction}_{get_card_number(packType, card_faction)}_C"
                results[common_card_code] += 1 
            #Generate 3 rare cards
            for rare_cards in range(3):
                card_faction = random.choice(factions)
                rare_card_code = f"{card_packs.get(packType)}{random.choice(factions)}_{get_card_number(packType, card_faction)}_R{random.choice(['1','2'])}"
                results[rare_card_code] += 1
    for entry in sorted(results.keys()):
        print(f"{results[entry]} {entry}")




def get_hero_code(expansion: str):
    hero_lo, hero_hi = hero_numbers[expansion]
    if(expansion == "Skybound Odyssey"):
        return f"{card_packs.get(expansion)}{random.choice(factions)}_{random.randint(hero_lo, hero_hi)}_C"
    elif(expansion in ("Beyond The Gates","Trial By Frost","Whispers From The Maze")):
        return f"{card_packs.get('Beyond The Gates')}{random.choice(factions)}_0{random.randint(hero_lo, hero_hi)}_C"
    return "test"

def get_card_number(expansion: str, faction: str):
    if(expansion == "Skybound Odyssey"): #For Skybound Axiom has no card 76 for some reason
        if(faction == "AX"):
            return pick_from_nonoverlapping([(66,75),(77,82)])
        else:
            return random.randint(66, 82)
    elif(expansion == "Beyond The Gates"):
        value = random.randint(4, 30)
        if(value < 10):
            value = "0" + str(value) #Only set where there are cards with 0s at the front, so this was needed
        return value
    elif(expansion == "Trial By Frost"):
        if(faction in ("MU","LY")): 
            return random.randint(32, 45)  #For Trial By Frost these two are missing card 46 for some reason
        else:
            return random.randint(32, 46)
    elif(expansion == "Whispers From The Maze"):
        return random.randint(49, 63)
 

def pick_from_nonoverlapping(ranges: list[tuple[int, int]]) -> int:
    # total count of integers across all ranges
    total = sum(hi - lo + 1 for lo, hi in ranges)
    k = random.randrange(total)

    # walk through ranges until k lands inside one
    for lo, hi in ranges:
        span = hi - lo + 1
        if k < span:
            return lo + k
        k -= span

    return 0 #should never be reached


if __name__ == "__main__":
    main()