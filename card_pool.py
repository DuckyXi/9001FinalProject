from minion import Minion, Spell

fire_mage = Minion("Fire Mage", 2, 2, 2, ["Ignite"], "Fire", "image/Fire Mage.png",
                        "Ignite: Give your minions +{buff}/+{buff}. After you play a Fire minion, this effect gains an additional +2/+2.")
fire_mage.fire_mage_ignite = 2


minion_pool = {
    "Mud Brick": Minion("Mud Brick", 1, 4, 4, ["Wall"], "Earth", "image/Mud Brick.png",
                        "Wall: Enemies must attack this minion first."),

    "Clay": Minion("Clay", 1, 2, 3, ["Sprout"], "Earth", "image/Clay.png",
                   "Sprout: Give a random friendly minion +2 Health."),

    "Flame Spark": Minion("Flame Spark", 1, 3, 1, ["Ignite"], "Fire", "image/Flame Spark.png",
                          "Ignite: Deal 4 damage to a random enemy."),

    "Forge Fire": Minion("Forge Fire", 1, 2, 2, ["Ignite"], "Fire", "image/Forge Fire.png",
                         "Ignite: Give a friendly minion +2/+2."),

    "Tender Sprout": Minion("Tender Sprout", 1, 2, 2, [], "Wood", "image/Tender Sprout.png",
                            "After you trigger Sprout, gain +2/+2."),

    "Tender Gardener": Minion("Tender Gardener", 1, 2, 2, ["Sprout"], "Wood", "image/Tender Gardener.png",
                        "Sprout: Randomly give a friendly minion +2/+2."),

    "Golden Blade": Minion("Golden Blade", 1, 1, 3, ["Slash"], "Metal", "image/Golden Blade.png",
                           "Slash: Gain +4 Attack."),

    "Broken Gold": Minion("Broken Gold", 1, 2, 1, ["Sprout"], "Metal", "image/Broken Gold.png",
                          "Sprout: Gain 1 Coin."),

    "Flowing Water": Minion("Flowing Water", 1, 2, 2, ["Sprout"], "Water", "image/Flowing Water.png",
                            "Sprout: Gain a Water Droplet."),

    "Water Bowl": Minion("Water Bowl", 1, 1, 2, ["Sprout"], "Water", "image/Water Bowl.png",
                         "Sprout: Summon a 1/1 Water Orb."),

    "Water Orb": Minion("Water Orb", 1, 1, 1, [], "Water", "image/Water Orb.png", "", True),

    "Water Mage": Minion("Water Mage", 2, 1, 1, [], "Water", "image/Water Mage.png",
                                "Whenever you cast a spell, give a random friendly minion +4/+3."),

    "Arcane Water Elemental": Minion("Arcane Water Elemental", 2, 2, 2, ["Sprout"], "Water", "image/Arcane Water Elemental.png",
                         "Sprout: Add a random spell to your hand."),

    "Wood Mage": Minion("Wood Mage", 2, 2, 2, [], "Wood", "image/Wood Mage.png",
                        "Whenever you trigger Sprout, give a random friendly minion +4/+3."),

    "Tree Guardian": Minion("Tree Guardian", 2, 3, 2, ["Wall", "Sprout"], "Wood", "image/Tree Guardian.png",
                            "Wall. Sprout: Randomly give a minion +{attack_buff}/+{health_buff}. This gains an additional +2/+3 for each Sprout triggered this turn."),

    "Fire Mage": fire_mage,

    "Fire Axe": Minion("Fire Axe", 2, 3, 2, ["Slash"], "Fire", "image/Fire Axe.png",
                       "Slash: Trigger the leftmost Ignite minion's effect twice."),

    "Split Wildfire": Minion("Split Wildfire", 10, 1, 2, ["Ignite"], "Fire", "image/Split Wildfire.png",
                         "Ignite: Summon two Fire Sparks."),

    "Gold Ingot": Minion("Gold Ingot", 2, 3, 1, ["Sprout", "Slash"], "Metal", "image/Gold Ingot.png",
                         "Sprout: Gain 1 Coin. Slash: Gain 2 Coin."),

    "Gold Mage": Minion("Gold Mage",3,3,4,["Slash"],"Metal","image/Gold Mage.png",
                        "Slash: Give your minions +{buff}/+{buff}. This increases whenever you spend gold."),

    "Golem": Minion("Golem", 2, 5, 10, ["Wall"], "Earth", "image/Golem.png",
                    "Wall. Whenever this takes damage, give your other minions +3/+4."),

    "Clay Giant": Minion("Clay Giant", 2, 5, 5, ["Wall"], "Earth", "image/Clay Giant.png",
                         "Wall. Whenever this takes damage, add a Clay or a Mud Brick to your hand."),

    "Clay Token": Minion("Clay Token",1,2,3,["Sprout"],"Earth","image/Clay.png",
                     "Sprout: Give a random friendly minion +2 Health.", True),

    "Mud Brick Token": Minion("Mud Brick", 1, 4, 4, ["Wall"], "Earth", "image/Mud Brick.png",
                        "Wall: Enemies must attack this minion first.", True),

    "Ancient Sprout Tree": Minion("Ancient Sprout Tree",3, 2, 4, [], "Wood", "image/Ancient Sprout Tree.png",
                                  "Your Sprout effects trigger twice."),

    "Blue Vine": Minion("Blue Vine",3, 3, 6, [], "Wood", "image/Blue Vine.png",
                        "After you trigger Sprout, give all friendly minions +1/+2."),

    "Death Flame": Minion("Death Flame",3, 2, 2, ["Ignite"], "Fire", "image/Death Flame.png",
                          "Ignite: Summon a Split Wildfire, give another friendly minion +2/+2, and give it this +2/+2 Ignite effect."),

    "Duke of Demon Flame": Minion("Duke of Demon Flame",3, 1, 7, [], "Fire", "image/Duke of Demon Flame.png",
                                  "Your Ignite effects trigger 2 extra time."),

    "Madam Wet": Minion("Madam Wet",3, 6, 6, [], "Water", "image/Madam Wet.png",
                        "Your targeted spells cast twice."),

    "Clone Water Lady": Minion("Clone Water Lady",3, 2, 5, ["Sprout"], "Water", "image/Clone Water Lady.png",
                               "Sprout: Add the last spell you cast to your hand."),

    "Gold Tycoon": Minion("Gold Tycoon",3, 2, 2, ["Sprout", "Slash"], "Metal", "image/Gold Tycoon.png",
                          "Whenever you sell a minion, exactly one Gold Tycoon stores 1 Coin."),

    "Diplomatic Gold Demon": Minion("Diplomatic Gold Demon", 3, 6, 1, ["Ignite"], "Metal", "image/Diplomatic Gold Demon.png",
                                    "Ignite: Add one random minion from each other element to your hand."),

    "Earth Bearer": Minion("Earth Bearer", 3, 3, 12, ["Wall"], "Earth", "image/Earth Bearer.png",
                           "After this takes damage, add the last spell you cast to your hand."),

    "Earthquake Elemental": Minion("Earthquake Elemental", 3, 4, 6, ["Wall", "Sprout"], "Earth", "image/Earthquake Elemental.png",
                                   "Wall. Sprout: Give your other minions +3/+3 and deal 1 damage to them."),

    "Raging Gargoyle": Minion("Raging Gargoyle",2,8,1,["Sprout"],"Earth","image/Raging Gargoyle.png",
                            "Sprout: Deal 1 damage to your Earth minions."),
}



spell_pool = {
    "Water Droplet": Spell(
        "Water Droplet",
        1,
        1,
        "image/Water Droplet.png",
        "Give a minion +1/+1.",
        True
    ),

    "Coin": Spell(
        "Coin",
        1,
        1,
        "image/Coin.png",
        "Gain 1 Coin.",
        False
    ),

    "Lucky Draw": Spell(
        "Lucky Draw",
        1,
        2,
        "image/Lucky Draw.png",
        "Obtain a random Tier 1 minion.",
        False
    ),

    "Condense": Spell(
        "Condense",
        1,
        3,
        "image/Condense.png",
        "Give all friendly minions +1/+1.",
        False
    ),

    "Earth Shield": Spell(
        "Earth Shield",
        2,
        1,
        "image/Earth Shield.png",
        "Give a minion +5 Health and Wall.",
        True),

    "Mining": Spell(
    "Mining",
    2,
    3,
    "image/Mining.png",
    "Increase your maximum gold by 1.",
    False
),

    "Element Extraction": Spell(
        "Element Extraction",
        2,
        3,
        "image/Element Extraction.png",
        "Obtain a random minion of a chosen element.",
        True
    ),

    "Thrive": Spell(
        "Thrive",
        2,
        3,
        "image/Thrive.png",
        "Obtain a random Sprout minion.",
        False
    ),

    "Pure Transformation": Spell(
        "Pure Transformation",
        3,
        1,
        "image/Pure Transformation.png",
        "Give a minion +3/+3. Future Pure Transformation effects gain an additional +3/+3.",
        True
    ),

    "Three Flowers Gather": Spell(
        "Three Flowers Gather",
        3,
        6,
        "image/Three Flowers Gather.png",
        "Obtain three random minions of different elements.",
        False
    ),

    "Refinement": Spell(
        "Refinement",
        3,
        4,
        "image/Refinement.png",
        "Give all minions +3/+4 twice.",
        False
    ),
}
