import pygame as pg
import random
import copy
import math
import os
import sys
from minion import Minion, Spell
from card_pool import minion_pool, spell_pool
from text import language_text, card_text, tribe_text, keywords_info_text
from datetime import datetime



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

#initialize pygame
pg.init()
pg.mixer.init()

#default music setting
current_music = None

#create a window
window = pg.display.set_mode((1200, 800))
pg.display.set_caption("Five Elements Battlegrounds")

#create a clock object
clock = pg.time.Clock()

#create fonts
font_path = resource_path("text/NotoSansCJKsc-Regular.otf")
font = pg.font.Font(font_path, 24)
title_font = pg.font.Font(font_path, 48)
button_font = pg.font.Font(font_path, 14)
text_font = pg.font.Font(font_path, 14)

# card size
CARD_WIDTH = 80
CARD_HEIGHT = 80


# gap between cards
CARD_GAP = 15

#sound effect
attack_sound = pg.mixer.Sound(resource_path("sound/attack.wav"))
lose_sound = pg.mixer.Sound(resource_path("sound/lose.mp3"))
win_sound = pg.mixer.Sound(resource_path("sound/win.wav"))

#heart image
heart_full_image = pg.image.load(
    resource_path("image/heart_full.png")
).convert_alpha()

heart_empty_image = pg.image.load(
    resource_path("image/heart_empty.png")
).convert_alpha()
heart_full_image = pg.transform.scale(
    heart_full_image,
    (40, 40)
)

heart_empty_image = pg.transform.scale(
    heart_empty_image,
    (40, 40)
)


#menu state
game_state = 'menu'
game_language = "English"

#result
result_title = ""
result_round = 0
result_board = []

#botton position in shop
refresh_button = pg.Rect(15, 150, 90, 40)
upgrade_button = pg.Rect(15, 100, 90, 40)
end_turn_button = pg.Rect(1080, 375, 70, 50)
concede_button = pg.Rect(1080, 30, 70, 50)
freeze_button = pg.Rect(15, 200, 90, 40)

#botton position in menu
start_button = pg.Rect(500, 200, 200, 60)
guide_button = pg.Rect(500, 290, 200, 60)
quit_button = pg.Rect(500, 380, 200, 60)
back_button = pg.Rect(500, 710, 200, 60)
language_button = pg.Rect(900, 640, 200, 60)

#botton position in language
english_button = pg.Rect(200, 340, 200, 60)
chinese_button = pg.Rect(800, 340, 200, 60)

#default message
message_text = ""
message_timer = 0

#keywords
keywords = ["Sprout", "Ignite", "Wall", "Slash"]

boss_pool = {
    1: [
            Minion("Eldritch Entity",1,7,6,[],"","image/Eldritch Entity.png",""                        ),

            Minion("Eldritch Entity",1,6,7,["Wall"],"","image/Eldritch Entity.png","Wall."),



        ],

    2: [
        Minion("Eldritch Entity", 1, 6, 7, [], "", "image/Eldritch Entity.png", ""),
        Minion("Eldritch Entity", 1, 8, 9, [], "", "image/Eldritch Entity.png", ""),
        Minion("Eldritch Entity", 1, 3, 14, [], "", "image/Eldritch Entity.png", ""),
    ],

    3: [
    Minion("Eldritch Entity", 3, 28, 30, ["Wall"], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 30, 24, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 26, 26, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 22, 24, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 22, 26, [], "", "image/Eldritch Entity.png", "")
],

    4: [
    Minion("Eldritch Entity", 3, 32, 50, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 36, 40, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 30, 50, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 28, 60, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 26, 60, ["Wall"], "", "image/Eldritch Entity.png", "")
],

    5: [
    Minion("Eldritch Entity", 3, 40, 100, ["Wall"], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 400, 40, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 200, 200, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 400, 40, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 100, 250, [], "", "image/Eldritch Entity.png", "")
],

    6: [
    Minion("Eldritch Entity", 3, 100, 600, ["Wall"], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 800, 40, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 400, 400, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 40, 800, [], "", "image/Eldritch Entity.png", ""),

    Minion("Eldritch Entity", 3, 500, 300, [], "", "image/Eldritch Entity.png", "")
],

}






# default setting
def reset_game():
    global boss_attack_index, player_attack_index, battle_turn, battle_state
    global attack_move_speed
    global attacker, target, attacker_rect, attacker_start_pos, attacker_attack_pos
    global shop_frozen
    global round_number, player_lives, battleground_level, upgrade_gold, gold, current_max_gold, max_gold, shop
    global shop, hand, board, saved_player_board, real_minion_pool
    global dragging_card, dragging_index, dragging_rect, dragging_source, drag_offset_x, drag_offset_y
    global max_hand_card, max_board_card, cost
    global pure_transformation_buff, sprout_count_this_turn, gold_spent_this_turn, last_cast_spell
    global run_history, last_recorded_round

    boss_attack_index = 0
    player_attack_index = 0
    battle_turn = "boss"
    battle_state = "idle"

    attack_move_speed = 3.5

    attacker = None
    target = None
    attacker_start_pos = None
    attacker_attack_pos = None
    attacker_rect = None

    shop_frozen = False

    round_number = 1
    player_lives = 3
    battleground_level = 1
    upgrade_gold = 18
    gold = 3
    current_max_gold = 3
    max_gold = 10

    shop = []
    hand = []
    board = []
    saved_player_board = []
    real_minion_pool = []

    dragging_card = None
    dragging_index = None
    dragging_rect = None
    dragging_source = None
    drag_offset_x = 0
    drag_offset_y = 0

    max_hand_card = 8
    max_board_card = 7
    cost = 3

    pure_transformation_buff = 3
    sprout_count_this_turn = 0
    gold_spent_this_turn = 0
    last_cast_spell = None

    run_history = []
    last_recorded_round = 0

    for minion in minion_pool.values():
        if minion.derivant:
            continue
        if minion.tier == 1:
            copies = 18
        elif minion.tier == 2:
            copies = 10
        else:
            copies = 2

        for i in range(copies):
            real_minion_pool.append(copy.deepcopy(minion))

    shop = generate_shop(real_minion_pool, battleground_level)

def generate_shop(real_pool, battleground_level):
    shop_size = get_number_of_cards_in_shop(battleground_level)

    available_minions = [minion for minion in real_pool if minion.tier <= battleground_level and not minion.derivant]

    draw_count = min(shop_size, len(available_minions))
    new_shop = random.sample(available_minions, draw_count)

    for minion in new_shop:
        real_pool.remove(minion)

    available_spells = [s for s in spell_pool.values() if s.tier <= battleground_level]

    spell = random.choice(available_spells)
    new_shop.append(copy.deepcopy(spell))

    random.shuffle(new_shop)

    return new_shop

#number of cards differ depending on shop lever
def get_number_of_cards_in_shop(battleground_level):
    if battleground_level == 1:
        return 3
    elif battleground_level == 2:
        return 4
    elif battleground_level == 3:
        return 5

reset_game()


#zones
buy_zone = pg.Rect(450, 650, 300, 80)
board_zone = pg.Rect(70, 300, 1000, 180)
sell_zone = pg.Rect(450, 200, 300, 80)
spell_zone = pg.Rect(500, 500, 200, 70)

def get_text(key):
    return language_text[game_language][key]

def get_card_name(card):
    return card_text[game_language][card]["name"]

def get_card_description(card_name, **kwargs):
    text = card_text[game_language][card_name]["description"]
    try:
        return text.format(**kwargs)
    except KeyError:
        return text

def get_card_tribe(keyword):
    return tribe_text[game_language][keyword]

def get_keywords_info(keyword):
    return keywords_info_text[game_language][keyword]



#main interface
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def draw_button(text, rect):
    mouse_pos = pg.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        color = (255, 182, 193)
    else:
        color = (128, 128, 128)

    pg.draw.rect(window, color, rect)
    pg.draw.rect(window, (255, 255, 255), rect, 3)

    text_surface = button_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)

def draw_menu():
    title_surface = title_font.render(get_text("game_title"), True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(600, 100))
    window.blit(title_surface, title_rect)

    draw_button(get_text("start"), start_button)
    draw_button(get_text("guide"), guide_button)
    draw_button(get_text("quit"), quit_button)
    draw_button(get_text("language"), language_button)

def draw_language():
    draw_button(get_text("english"), english_button)
    draw_button(get_text("chinese"), chinese_button)
    draw_button(get_text("back"), back_button)


def draw_guide():
    draw_text(get_text("game_guide_title"), title_font, (0, 0, 0), 520, 60)

    guide_lines = get_text("game_guide_content")

    y = 150
    for line in guide_lines:
        draw_text(line, text_font, (0, 0, 0), 120, y)
        y += 18

    draw_button(get_text("back"), back_button)

def draw_arrow(start_pos, end_pos):
    pg.draw.line(window, (255, 255, 255), start_pos, end_pos, 4)

    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])

    arrow_length = 15
    arrow_angle = 0.6

    left = (
        end_pos[0] - arrow_length * math.cos(angle - arrow_angle),
        end_pos[1] - arrow_length * math.sin(angle - arrow_angle)
    )

    right = (
        end_pos[0] - arrow_length * math.cos(angle + arrow_angle),
        end_pos[1] - arrow_length * math.sin(angle + arrow_angle)
    )

    pg.draw.polygon(window, (255, 255, 255), [end_pos, left, right])

#game_interface
def draw_game():
    # background
    window.fill((181, 136, 99))

    # player information
    draw_text(f"{get_text("gold")}: {gold}/{current_max_gold}", text_font, (0, 0, 0), 30, 720)

    # section titles
    draw_text(f"{get_text("shop")}(level:{battleground_level})", title_font, (0, 0, 0), 30, 20)
    draw_text(get_text("board"), text_font, (0, 0, 0), 30, 420)
    draw_text(f"{get_text("round")}:{round_number}", text_font, (255, 255, 255), 1090, 435)

    #draw lives
    draw_lives()


    # shop cards
    draw_shop(window, shop, text_font)

    # board cards
    for i, card in enumerate(board):
        rect = get_board_card_rect(i)
        draw_card(card, rect)

    # hand cards
    for i, card in enumerate(hand):
        rect = pg.Rect(120 + i * 120, 600, 120, 170)
        draw_card(card, rect)

    #buy zone
    if dragging_source == "shop":
        pg.draw.rect(window, (100, 120, 80), buy_zone)
        pg.draw.rect(window, (255, 255, 255), buy_zone, 3)

        draw_text(
            get_text("drag_buy"),
            text_font,
            (255, 255, 255),
            buy_zone.x + 100,
            buy_zone.y + 30
        )

    # sell zone
    if dragging_source == "board":
        pg.draw.rect(window, (120, 60, 60), sell_zone)
        pg.draw.rect(window, (255, 255, 255), sell_zone, 3)

        draw_text(
            get_text("drag_sell"),
            text_font,
            (255, 255, 255),
            sell_zone.x + 70,
            sell_zone.y + 30
        )

    if dragging_source == "hand":
        if isinstance(dragging_card, Spell):
            if not dragging_card.have_target:
                pg.draw.rect(window, (80, 80, 160), spell_zone, border_radius=10)
                pg.draw.rect(window, (255, 255, 255), spell_zone, 2, border_radius=10)
                draw_text(
                    get_text("cast_spell_here"),
                    text_font,
                    (255, 255, 255),
                    spell_zone.x + 40,
                    spell_zone.y + 22
                )
            else:
                start_pos = dragging_rect.center
                end_pos = pg.mouse.get_pos()
                draw_arrow(start_pos, end_pos)

    mouse_pos = pg.mouse.get_pos()

    if dragging_card is None:

        # shop tooltip
        for i, card in enumerate(shop):
            rect = pg.Rect(120 + i * 140, 100, 120, 170)

            if rect.collidepoint(mouse_pos):
                draw_tooltip(card, mouse_pos)

        # board tooltip
        for i, card in enumerate(board):
            rect = get_board_card_rect(i)

            if rect.collidepoint(mouse_pos):
                draw_tooltip(card, mouse_pos)

        # hand tooltip
        for i, card in enumerate(hand):
            rect = pg.Rect(120 + i * 120, 600, 120, 170)

            if rect.collidepoint(mouse_pos):
                draw_tooltip(card, mouse_pos)

    if message_timer > 0:
        draw_message(600, 400)



    # buttons
    draw_button(get_text("refresh"), refresh_button)
    draw_button(f"{get_text("upgrade")}({upgrade_gold})", upgrade_button)
    draw_button(get_text("end_turn"), end_turn_button)
    draw_button(get_text("concede"), concede_button)
    if shop_frozen:
        draw_button(get_text("unfreeze"), freeze_button)
    else:
        draw_button(get_text("freeze"), freeze_button)

    # draw dragging card on top
    if dragging_card is not None and dragging_rect is not None:
        draw_card(dragging_card, dragging_rect)

def draw_result():
    window.fill((50, 40, 40))

    draw_text(result_title, title_font, (255, 255, 255), 50, 80)
    draw_text(f"{get_text("survive_round")}: {result_round}", text_font, (255, 255, 255), 50, 160)

    draw_text("Final Team", text_font, (255, 255, 255), 50, 240)

    for i, card in enumerate(result_board):
        rect = pg.Rect(100 + i * 140, 320, 120, 170)
        draw_card(card, rect)

    mouse_pos = pg.mouse.get_pos()

    for i, card in enumerate(result_board):
        rect = pg.Rect(100 + i * 140, 320, 120, 170)

        if rect.collidepoint(mouse_pos):
            draw_tooltip(card, mouse_pos)

    draw_button(get_text("back"), back_button)

def get_buff_text(minion):
    buffs = getattr(minion, "buffs", {})

    if len(buffs) == 0:
        return "None"

    parts = []
    for source, buff in buffs.items():
        parts.append(f"{source}: +{buff['attack']}/+{buff['health']}")

    return ", ".join(parts)

def record_current_round_team():
    global run_history, last_recorded_round
    if last_recorded_round == round_number:
        return

    round_record = {
        "round": round_number,
        "team": []
    }

    for minion in board:
        round_record["team"].append({
            "name": get_card_name(minion.name),
            "attack": minion.attack,
            "health": minion.health,
            "buffs": get_buff_text(minion)
        })

    run_history.append(round_record)
    last_recorded_round = round_number

def export_run_history(final_status):
    with open("run_history.txt", "a", encoding="utf-8") as f:
        f.write("\n")
        f.write("=" * 40 + "\n")
        f.write("New Run\n")
        f.write("=" * 40 + "\n")
        f.write(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Final Result: {final_status}\n")
        f.write(f"Ended Round: {round_number}\n\n")

        for round_record in run_history:
            f.write(f"Round {round_record['round']}\n")
            f.write("--------------------\n")

            if len(round_record["team"]) == 0:
                f.write("No minions\n")
            else:
                for i, minion in enumerate(round_record["team"], start=1):
                    f.write(f"{i}. {minion['name']} {minion['attack']}/{minion['health']}\n")
                    f.write(f"   Buffs: {minion['buffs']}\n")

            f.write("\n")

def return_shop_to_pool():
    global shop, real_minion_pool

    for card in shop:
        if isinstance(card, Minion):
            real_minion_pool.append(copy.deepcopy(minion_pool[card.name]))

    shop = []


def draw_card(card, rect):

    # background
    if isinstance(card, Minion):
        pg.draw.rect(window, (90, 60, 40), rect)

    elif isinstance(card, Spell):
        pg.draw.rect(window, (50, 80, 120), rect)

    pg.draw.rect(window, (255, 255, 255), rect, 2)

    # image
    try:
        image = pg.image.load(resource_path(card.image_path)).convert()
        image = pg.transform.scale(image, (100, 80))

        window.blit(image, (rect.x + 10, rect.y + 10))

    except pg.error:

        pg.draw.rect(
            window,
            (120, 120, 120),
            (rect.x + 10, rect.y + 10, 100, 80)
        )

        draw_text(
            "Image Error",
            text_font,
            (255,255,255),
            rect.x + 10,
            rect.y + 35
        )


    # name
    draw_text(
        get_card_name(card.name),
        text_font,
        (255,255,255),
        rect.x + 8,
        rect.y + 95
    )

    # minion stats
    if isinstance(card, Minion):

        draw_text(
            f"{card.attack}",
            text_font,
            (255,255,255),
            rect.x + 8,
            rect.y + 145
        )

        draw_text(
            f"{card.health}",
            text_font,
            (255,255,255),
            rect.x + 108,
            rect.y + 145
        )

        draw_text(
            f"{get_card_tribe(card.tribe)}",
            pg.font.Font(font_path, 8),
            (0, 0, 0),
            rect.x + 50,
            rect.y + 150
        )

    # spell stats
    elif isinstance(card, Spell):

        draw_text(
            get_text("spell"),
            pg.font.Font(font_path, 8),
            (0, 0, 0),
            rect.x + 48,
            rect.y + 150
        )

        pg.draw.rect(window, (200, 200, 200), (rect.x, rect.y, 28, 28))

        draw_text(
            f"{card.cost}",
            pg.font.Font(font_path, 16),
            (0, 0, 139),
            rect.x + 8,
            rect.y + 8
        )

def draw_shop(window, shop, font):
    for i, card in enumerate(shop):
        rect = pg.Rect(120 + i * 140, 100, 120, 170)
        draw_card(card, rect)
        if shop_frozen:
            ice_surface = pg.Surface((120, 170), pg.SRCALPHA)
            ice_surface.fill((120, 180, 255, 80))
            window.blit(ice_surface, rect.topleft)

            pg.draw.rect(window, (180, 220, 255), rect, 3)

def draw_lives():
    start_x = 1140
    y = 700
    for i in range(3):
        if i < player_lives:
            window.blit(
                heart_full_image,
                (start_x - i * 45, y)
            )
        else:
            window.blit(
                heart_empty_image,
                (start_x - i * 45, y)
            )


def summon_minion(minion, target_board):
    global max_board_card
    if len(target_board) < max_board_card:
        target_board.append(minion)



def play_minion_from_hand(index):
    if len(board) < max_board_card:
        card = hand.pop(index)
        has_tree = any(
            m.name == "Ancient Sprout Tree"
            for m in board
        )
        if has_tree:
            for i in range(2):
                trigger_play_effect(card)
        else:
            trigger_play_effect(card)
        board.append(card)
        trigger_after_play_effect(card)
    else:
        show_message(get_text("board_is_full"))

def get_random_minion(tier):
    available_minions = [minion for minion in real_minion_pool if minion.derivant == False and minion.tier <= tier]
    minion = random.choice(available_minions)
    if len(hand) < max_hand_card:
        hand.append(minion)
        real_minion_pool.remove(minion)
    return

def cast_spell(spell, target=None):
    global gold, current_max_gold, max_gold
    global last_cast_spell
    global pure_transformation_buff

    if spell.name == "Water Droplet":
        add_buff(target, 1, 1, spell.name)

    elif spell.name == "Coin":
        gold += 1

    elif spell.name == "Lucky Draw":
        get_random_minion(1)

    elif spell.name == "Condense":
        for minion in board:
            add_buff(minion, 1, 1, spell.name)

    elif spell.name == "Earth Shield":
        add_buff(target, 0, 5, spell.name)
        if not "Wall" in target.keywords:
            target.keywords.append("Wall")

    elif spell.name == "Mining":
        current_max_gold += 1
        max_gold += 1

    elif spell.name == "Element Extraction":
        specific_tribe_minions = [minion for minion in real_minion_pool if minion.tribe == target.tribe and minion.tier <= battleground_level]
        minion = random.choice(specific_tribe_minions)
        if len(hand) < max_hand_card:
            hand.append(minion)
            real_minion_pool.remove(minion)

    elif spell.name == "Thrive":
        sprout_minions = [m for m in real_minion_pool if "Sprout" in m.keywords and m.tier <= battleground_level]
        m = random.choice(sprout_minions)
        if len(hand) < max_hand_card:
            hand.append(m)
            real_minion_pool.remove(m)

    elif spell.name == "Pure Transformation":
        add_buff(target, pure_transformation_buff, pure_transformation_buff, spell.name)
        pure_transformation_buff += 3

    elif spell.name == "Three Flowers Gather":
        tribes = ["Fire", "Water", "Wood", "Metal", "Earth"]
        random.shuffle(tribes)
        selected_tribes = tribes[:3]
        for tribe in selected_tribes:
            available_minions = [
                m for m in real_minion_pool
                if m.tribe == tribe
                   and m.tier <= battleground_level
                   and not m.derivant
            ]

            if len(available_minions) == 0:
                continue
            random_minion = random.choice(available_minions)
            if len(hand) < max_hand_card:
                hand.append(random_minion)

                real_minion_pool.remove(random_minion)

    elif spell.name == "Refinement":
        for i in range(2):
            for m in board:
                add_buff(m, 3, 4, spell.name)

    for m in board:
        if m.name == "Water Mage":
            water_mage_buff_m = random.choice(board)
            add_buff(water_mage_buff_m, 4, 3, m.name)

    last_cast_spell = spell

def cast_target_spell(spell, target):
    cast_spell(spell, target)
    has_madam_wet = any(
        m.name == "Madam Wet"
        for m in board
    )
    if has_madam_wet:
        cast_spell(spell, target)



def trigger_play_effect(minion):
    global gold, current_max_gold, max_gold
    global sprout_count_this_turn
    if "Sprout" in minion.keywords:

        if minion.name == "Flowing Water":
            if len(hand) < max_hand_card:
                hand.append(copy.deepcopy(spell_pool["Water Droplet"]))

        elif minion.name == "Clay":
            if len(board) > 0:
                m = random.choice(board)
                add_buff(m, 0, 3, minion.name)
                add_buff(m, 0, -1, minion.name)
                trigger_on_damage_effect(m)

        elif minion.name == "Broken Gold":
            if len(hand) < max_hand_card:
                hand.append(copy.deepcopy(spell_pool["Coin"]))

        elif minion.name == "Water Bowl":
            if len(board) < max_board_card-1:
                summon_minion(copy.deepcopy(minion_pool["Water Orb"]), board)

        elif minion.name == "Arcane Water Elemental":
            random_spells = [s for s in spell_pool.values() if s.tier <= battleground_level]
            s = random.choice(random_spells)
            if len(hand) < max_hand_card:
                hand.append(copy.deepcopy(s))


        elif minion.name == "Tree Guardian":
            if len(board) > 0:
                buff = 2 * (sprout_count_this_turn + 1)
                target = random.choice(board)
                add_buff(target, buff, buff + sprout_count_this_turn + 1, minion.name)


        elif minion.name == "Gold Ingot":
            if len(hand) < max_hand_card:
                hand.append(copy.deepcopy(spell_pool["Coin"]))

        elif minion.name == "Clone Water Lady":
            if last_cast_spell is not None:
                if len(hand) < max_hand_card:
                    hand.append(
                        copy.deepcopy(last_cast_spell)
                    )

        elif minion.name == "Gold Tycoon":
            for i in range(2):
                if len(hand) < max_hand_card:
                    hand.append(copy.deepcopy(spell_pool["Coin"]))


        elif minion.name == "Earthquake Elemental":
            for m in board:
                if m != minion:
                    add_buff(m, 3, 3, minion.name)
                    add_buff(m, 0, -1, m.name)

                    trigger_on_damage_effect(m)
        elif minion.name == "Raging Gargoyle":
            for m in board:
                if m.tribe == "Earth" and m != minion:
                    add_buff(m, 0, -1, minion.name)
                    trigger_on_damage_effect(m)

        elif minion.name == "Tender Gardener":
            if len(board) != 0:
                random_minions = [m for m in board]
                buff_minion = random.choice(random_minions)
                add_buff(buff_minion, 2, 2, minion.name)



        for m in board:
            if m.name == "Wood Mage":
                wood_mage_buff_m = random.choice(board)
                add_buff(wood_mage_buff_m, 4, 3, m.name)

            elif m.name == "Blue Vine":
                buff_minions = [minion for minion in board if minion.tribe == "Wood"]
                for minion in buff_minions:
                    add_buff(minion, 1, 2, m.name)

            elif m.name == "Tender Sprout":
                add_buff(m, 2, 2, m.name)


        sprout_count_this_turn += 1

def trigger_after_play_effect(played_minion):
    if played_minion.tribe == "Fire":
        for minion in board:
            if minion.name == "Fire Mage":
                minion.fire_mage_ignite += 2



def trigger_on_attack_effect(minion):
    global current_max_gold, max_gold
    global enemy_board
    if "Slash" in minion.keywords:
        if minion.name == "Golden Blade":
            add_buff(minion, 4, 0, minion.name)


        elif minion.name == "Fire Axe":
            for i in range(2):
                for m in board:
                    if "Ignite" in m.keywords:
                        trigger_on_death_effect(m, board, boss_board)
                        break

        elif minion.name == "Gold Mage":
            buff = gold_spent_this_turn * 2
            for m in board:
                add_buff(m, buff, buff, minion.name)


        elif minion.name == "Gold Ingot":
            for i in range(2):
                if len(hand) < max_hand_card:
                    hand.append(copy.deepcopy(spell_pool["Coin"]))

        elif minion.name == "Gold Tycoon":
            current_max_gold += 1
            max_gold += 1




def get_ignite_trigger_times(friendly_board):
    trigger_times = 1
    for minion in friendly_board:
        if minion.name == "Duke of Demon Flame":
            trigger_times += 2

    return trigger_times

def trigger_on_death_effect(dead_minion, friendly_board, enemy_board):
    if "Ignite" not in dead_minion.keywords:
        return
    trigger_times = get_ignite_trigger_times(friendly_board)
    for time in range(trigger_times):
        trigger_single_death_effect(dead_minion, friendly_board, enemy_board)


def trigger_single_death_effect(dead_minion, friendly_board, enemy_board):
    if "Ignite" in dead_minion.keywords:
        if dead_minion.name == "Flame Spark":
            alive_enemies = []

            for enemy in enemy_board:
                if enemy.health > 0:
                    alive_enemies.append(enemy)

            if len(alive_enemies) > 0:
                target = random.choice(alive_enemies)
                target.health -= 4

        elif dead_minion.name == "Forge Fire":
            alive_minions = []

            for minion in friendly_board:
                if minion.health > 0 and minion != dead_minion:
                    alive_minions.append(minion)

            if len(alive_minions) > 0:
                target = random.choice(alive_minions)
                add_buff(target, 2, 2, dead_minion.name)


        elif dead_minion.name == "Fire Mage":
            for m in friendly_board:
                add_buff(m, dead_minion.fire_mage_ignite, dead_minion.fire_mage_ignite, dead_minion.name)


        elif dead_minion.name == "Split Wildfire":
            for i in range(2):
                if len(friendly_board) < max_board_card:
                    summon_minion(copy.deepcopy(minion_pool["Flame Spark"]), friendly_board)


        elif dead_minion.name == "Death Flame":

            summon_minion(
                copy.deepcopy(minion_pool["Split Wildfire"]),
                friendly_board
            )

            give_death_flame_effect(
                friendly_board,
                dead_minion,
                1
            )

        elif dead_minion.name == "Diplomatic Gold Demon":
            other_tribes = ["Fire", "Water", "Wood", "Earth"]
            for tribe in other_tribes:
                available_minions = [
                    m for m in real_minion_pool
                    if m.tribe == tribe
                       and m.tier <= battleground_level
                       and not m.derivant
                ]
                if len(available_minions) == 0:
                    continue
                if len(hand) >= max_hand_card:
                    break
                random_minion = random.choice(available_minions)
                hand.append(random_minion)
                real_minion_pool.remove(random_minion)


        death_flame_count = getattr(
            dead_minion,
            "death_flame_count",
            0
        )


        if death_flame_count > 0:
            give_death_flame_effect(
                friendly_board,
                dead_minion,
                death_flame_count
            )

def trigger_on_damage_effect(damaged_minion):
    global last_cast_spell
    if damaged_minion.name == "Golem":
        if damaged_minion in board:
            friendly_board = board
        else:
            friendly_board = boss_board

        for minion in friendly_board:
            if minion != damaged_minion:
                add_buff(minion, 3, 4, damaged_minion.name)


    elif damaged_minion.name == "Clay Giant":
        if len(hand) < max_hand_card:
            random_token = random.choice([
                "Clay Token",
                "Mud Brick Token"
            ])
            hand.append(copy.deepcopy(minion_pool[random_token]))

    elif damaged_minion.name == "Earth Bearer":
        if last_cast_spell is not None:
            if len(hand) < max_hand_card:
                hand.append(
                    copy.deepcopy(last_cast_spell)
                )

def give_death_flame_effect(friendly_board, dead_minion, count):

    available_minions = [
        m for m in friendly_board
        if m.health > 0 and m != dead_minion
    ]

    if len(available_minions) == 0:
        return

    buff_target = random.choice(available_minions)

    # buff count times
    add_buff(buff_target, 2 * count, 2 * count, "Death Flame")


    if "Ignite" not in buff_target.keywords:
        buff_target.keywords.append("Ignite")

    # inherit full stacks
    buff_target.death_flame_count = (
        getattr(buff_target, "death_flame_count", 0)
        + count
    )

def trigger_gold_tycoon_sell_effect():
    gold_tycoons = [
        m for m in board
        if m.name == "Gold Tycoon"
    ]
    if len(gold_tycoons) == 0:
        return

    chosen_tycoon = random.choice(gold_tycoons)
    chosen_tycoon.gold_tycoon_sold_count = (
        getattr(chosen_tycoon, "gold_tycoon_sold_count", 0)
        + 1
    )

def resolve_gold_tycoon_income():
    global gold
    for m in board:
        if m.name == "Gold Tycoon":
            bonus_gold = getattr(
                m,
                "gold_tycoon_sold_count",
                0
            )

            gold += bonus_gold
            m.gold_tycoon_sold_count = 0

def get_original_minion(name):
    return minion_pool.get(name)

def get_dynamic_description(card):
    if card.name == "Pure Transformation":
        return get_card_description(card.name, buff=pure_transformation_buff)

    elif card.name == "Fire Mage":
        return get_card_description(card.name, buff=card.fire_mage_ignite)

    elif card.name == "Tree Guardian":
        attack_buff = 2 * (sprout_count_this_turn + 1)
        health_buff = 3 * (sprout_count_this_turn + 1)
        return get_card_description(card.name, attack_buff=attack_buff, health_buff=health_buff)

    elif card.name == "Gold Mage":
        return get_card_description(card.name, buff=gold_spent_this_turn * 2)

    elif card.name == "Gold Tycoon":
        return get_card_description(card.name, stored_gold=getattr(card, "gold_tycoon_sold_count", 0))

    return get_card_description(card.name)


def draw_tooltip(card, mouse_pos):
    mouse_x, mouse_y = mouse_pos


    padding = 10
    title_line_height = 25
    normal_line_height = 20

    title_color = (255, 240, 200)
    text_color = (245, 245, 245)

    lines = []

    def add_line(text, color=text_color, line_height=normal_line_height):
        lines.append((text, color, line_height))

    # name
    add_line(get_card_name(card.name), title_color, title_line_height)

    if isinstance(card, Minion):
        add_line(f"{get_text('cost')}: 3")
        add_line(f"{get_text('tier')}: {card.tier}")
        add_line(f"{get_text('attack')}: {card.attack}")
        add_line(f"{get_text('health')}: {card.health}")
        add_line(f"{get_text('tribe')}: {get_card_tribe(card.tribe)}")

        for keyword in card.keywords:
            if keyword in keywords:
                add_line(get_keywords_info(keyword))

        description = get_dynamic_description(card)
        for line in description.split("\n"):
            if line != "":
                add_line(line)

        buffs = getattr(card, "buffs", {})
        if len(buffs) > 0:
            add_line("Buffs:")
            for source, buff in buffs.items():
                add_line(f"{source}: +{buff['attack']}/+{buff['health']}")

    elif isinstance(card, Spell):
        add_line(f"{get_text('cost')}: {card.cost}")
        add_line(f"{get_text('tier')}: {card.tier}")
        add_line(f"{get_text('type')}: {get_text('spell')}")

        description = get_dynamic_description(card)
        for line in description.split("\n"):
            if line != "":
                add_line(line)

    max_text_width = 0
    for text, _, _ in lines:
        text_width = text_font.size(text)[0]
        if text_width > max_text_width:
            max_text_width = text_width

    tooltip_width = max(180, max_text_width + padding * 2)
    tooltip_height = padding * 2 + sum(line_height for _, _, line_height in lines)

    # decide the direction
    if mouse_x < 600:
        tooltip_x = mouse_x + 15
    else:
        tooltip_x = mouse_x - tooltip_width - 15

    # vertical
    if mouse_y < 400:
        tooltip_y = mouse_y + 15
    else:
        tooltip_y = mouse_y - tooltip_height - 15

    tooltip_x = max(0, min(tooltip_x, window.get_width() - tooltip_width))
    tooltip_y = max(0, min(tooltip_y, window.get_height() - tooltip_height))

    tooltip_surface = pg.Surface((tooltip_width, tooltip_height), pg.SRCALPHA)

    pg.draw.rect(
        tooltip_surface,
        (20, 20, 20, 190),
        (0, 0, tooltip_width, tooltip_height),
        border_radius=10
    )

    pg.draw.rect(
        tooltip_surface,
        (255, 255, 255, 220),
        (0, 0, tooltip_width, tooltip_height),
        2,
        border_radius=10
    )

    window.blit(tooltip_surface, (tooltip_x, tooltip_y))

    y = tooltip_y + padding
    for text, color, line_height in lines:
        draw_text(text, text_font, color, tooltip_x + padding, y)
        y += line_height


def upgrade_shop():
    global gold, battleground_level, upgrade_gold, gold_spent_this_turn

    if battleground_level < 3 and gold >= upgrade_gold:
        gold -= upgrade_gold
        gold_spent_this_turn += upgrade_gold
        battleground_level += 1
        upgrade_gold = 18

    elif battleground_level == 3:
        show_message(get_text("already_3_level"))

    else:
        show_message(get_text("not_enough_gold_to_up_grade"))

def start_new_shop_turn(need_round_message):
    global round_number, sprout_count_this_turn, gold_spent_this_turn
    global upgrade_gold, current_max_gold, max_gold, gold
    global shop, shop_frozen, battle_state, game_state

    round_number += 1
    sprout_count_this_turn = 0
    gold_spent_this_turn = 0

    if upgrade_gold > 1:
        upgrade_gold -= 1

    if shop_frozen:
        shop_frozen = False
    else:
        return_shop_to_pool()
        shop = generate_shop(real_minion_pool, battleground_level)

    if current_max_gold < max_gold:
        current_max_gold += 1
    gold = current_max_gold
    resolve_gold_tycoon_income()

    battle_state = "idle"
    game_state = "game"

    if need_round_message:
        show_message(f"{get_text('round')} {round_number}")

def add_buff(minion, attack_buff, health_buff, source):
    minion.attack += attack_buff
    minion.health += health_buff
    source = get_card_name(source)
    if source not in minion.buffs:
        minion.buffs[source] = {
            "attack": 0,
            "health": 0
        }
    minion.buffs[source]["attack"] += attack_buff
    minion.buffs[source]["health"] += health_buff

def is_boss_round(round_number):
    return round_number % 3 == 0

def prepare_boss_battle():
    global saved_player_board, boss_board
    global battle_turn, boss_attack_index, player_attack_index
    global battle_round, battle_state, game_state

    saved_player_board = copy.deepcopy(board)
    boss_board = create_boss_board(round_number)

    battle_turn = "boss"
    boss_attack_index = 0
    player_attack_index = 0
    battle_round = 1
    battle_state = "idle"
    game_state = "battle"

def create_boss_board(round_number):
    boss_number = round_number // 3

    if boss_number in boss_pool:
        return copy.deepcopy(boss_pool[boss_number])

    return copy.deepcopy(boss_pool[max(boss_pool.keys())])
def choose_target(enemy_board):
    alive_enemies = []

    for minion in enemy_board:
        if minion.health > 0:
            alive_enemies.append(minion)

    wall_enemies = []

    for minion in alive_enemies:
        if "Wall" in minion.keywords:
            wall_enemies.append(minion)

    if len(wall_enemies) > 0:
        return random.choice(wall_enemies)
    if len(alive_enemies) == 0:
        return None
    return random.choice(alive_enemies)

def get_boss_card_rect(index):
    return pg.Rect(120 + index * 140, 180, 120, 170)


def get_player_card_rect(index):
    return pg.Rect(120 + index * 140, 460, 120, 170)

def get_board_card_rect(index):
    return pg.Rect(70 + index * 140, 320, 120, 170)

def find_minion_index(board_list, minion):
    for i, m in enumerate(board_list):
        if m == minion:
            return i

    return -1

def calculate_attack_speed(start_pos, attack_pos):
    base_start = get_player_card_rect(0).topleft
    base_target_rect = get_boss_card_rect(0)
    base_attack_pos = (base_target_rect.x, base_target_rect.y + 120)

    base_dx = base_attack_pos[0] - base_start[0]
    base_dy = base_attack_pos[1] - base_start[1]
    base_distance = math.sqrt(base_dx * base_dx + base_dy * base_dy)

    fixed_frames = math.ceil(base_distance / 3.5)

    dx = attack_pos[0] - start_pos[0]
    dy = attack_pos[1] - start_pos[1]
    distance = math.sqrt(dx * dx + dy * dy)

    return distance / fixed_frames

def start_next_attack():
    global battle_turn
    global boss_attack_index, player_attack_index
    global attack_move_speed
    global attacker, target
    global attacker_start_pos, attacker_attack_pos, attacker_rect
    global battle_state, battle_round
    # clear dead minion
    remove_dead_minions()

    if len(board) == 0 or len(boss_board) == 0:
        battle_state = "finished"
        return

    # boss 先手
    if battle_turn == "boss":
        attacker_index = boss_attack_index % len(boss_board)
        attacker = boss_board[attacker_index]

        target = choose_target(board)

        if target is None:
            battle_state = "finished"
            return
        trigger_on_attack_effect(attacker)

        attacker_start_pos = get_boss_card_rect(attacker_index).topleft

        target_index = find_minion_index(board, target)
        target_rect = get_player_card_rect(target_index)

        attacker_attack_pos = (target_rect.x, target_rect.y - 120)

        attack_move_speed = calculate_attack_speed(
            attacker_start_pos,
            attacker_attack_pos
        )

    else:
        attacker_index = player_attack_index % len(board)
        attacker = board[attacker_index]

        target = choose_target(boss_board)

        if target is None:
            battle_state = "finished"
            return
        trigger_on_attack_effect(attacker)

        attacker_start_pos = get_player_card_rect(attacker_index).topleft
        target_index = find_minion_index(boss_board, target)
        target_rect = get_boss_card_rect(target_index)
        attacker_attack_pos = (target_rect.x, target_rect.y + 120)

        attack_move_speed = calculate_attack_speed(
            attacker_start_pos,
            attacker_attack_pos
        )

    attacker_rect = pg.Rect(
        attacker_start_pos[0],
        attacker_start_pos[1],
        120,
        170
    )

    battle_state = "moving_to_target"

def move_rect_towards(rect, target_pos, speed):
    target_x, target_y = target_pos

    dx = target_x - rect.x
    dy = target_y - rect.y

    distance = math.sqrt(dx * dx + dy * dy)

    if distance <= speed:
        rect.x = target_x
        rect.y = target_y
        return True

    move_x = dx / distance
    move_y = dy / distance

    rect.x += move_x * speed
    rect.y += move_y * speed

    return False


def resolve_attack():
    target.health -= attacker.attack
    attacker.health -= target.attack

    # Ignite: death trigger
    if attacker.health <= 0:
        friendly_board = boss_board if attacker in boss_board else board
        enemy_board = board if attacker in boss_board else boss_board
        trigger_on_death_effect(attacker, friendly_board, enemy_board)

    if target.health <= 0:
        friendly_board = boss_board if target in boss_board else board
        enemy_board = board if target in boss_board else boss_board
        trigger_on_death_effect(target,friendly_board, enemy_board)

    if attacker.attack > 0:
        trigger_on_damage_effect(target)

    if target.attack > 0:
        trigger_on_damage_effect(attacker)


def remove_dead_minions():
    global board, boss_board

    board = [m for m in board if m.health > 0]
    boss_board = [m for m in boss_board if m.health > 0]

def update_battle():
    global battle_state, battle_index, battle_turn
    global boss_attack_index, player_attack_index
    global attacker_rect


    if battle_state == "idle":
        start_next_attack()

    elif battle_state == "moving_to_target":
        arrived = move_rect_towards(attacker_rect, attacker_attack_pos, attack_move_speed)

        if arrived:
            attack_sound.play()
            resolve_attack()
            battle_state = "moving_back"

    elif battle_state == "moving_back":
        arrived = move_rect_towards(attacker_rect, attacker_start_pos, attack_move_speed)

        if arrived:
            dead_boss_indexes = [i for i, m in enumerate(boss_board) if m.health <= 0]
            dead_player_indexes = [i for i, m in enumerate(board) if m.health <= 0]

            for i in dead_boss_indexes:
                if i < boss_attack_index:
                    boss_attack_index -= 1

            for i in dead_player_indexes:
                if i < player_attack_index:
                    player_attack_index -= 1

            remove_dead_minions()

            if battle_turn == "boss":
                if attacker.health > 0:
                    boss_attack_index += 1
                battle_turn = "player"
            else:
                if attacker.health > 0:
                    player_attack_index += 1
                battle_turn = "boss"



            if len(board) == 0 or len(boss_board) == 0:
                battle_state = "finished"
            else:
                battle_state = "idle"

    elif battle_state == "finished":
        finish_battle()

def finish_battle():
    global game_state, battle_state, gold, upgrade_gold, gold_spent_this_turn, shop
    global board, saved_player_board
    global round_number, player_lives
    global result_title, result_round, result_board
    global shop_frozen
    global sprout_count_this_turn

    player_alive = len(board) > 0
    boss_alive = len(boss_board) > 0

    # last boss: win or draw means final victory
    if round_number == 18:
        # must kill the boss to win
        if not boss_alive:
            export_run_history("Cleared")

            result_title = "Final Victory!"
            result_round = round_number
            result_board = copy.deepcopy(saved_player_board)

            game_state = "result"
            play_music("music/victory.mp3")
            battle_state = "idle"
            return

        else:
            export_run_history("Defeat")

            result_title = "Game Over"
            result_round = round_number
            result_board = copy.deepcopy(saved_player_board)

            play_music("music/failure.mp3")
            game_state = "result"
            battle_state = "idle"
            return


    # first 5 bosses
    if boss_alive and not player_alive:
        player_lives -= 1
        lose_sound.play()
        show_message(f"{get_text("you_lose_lives_left")}: {player_lives}")

        if player_lives <= 0:
            export_run_history("Defeat")

            result_title = "Game Over"
            result_round = round_number
            result_board = copy.deepcopy(saved_player_board)

            game_state = "result"
            play_music("music/failure.mp3")
            battle_state = "idle"
            return

    else:
        win_sound.play()
        show_message(get_text("boss_cleared"))

    # restore board after battle
    board = copy.deepcopy(saved_player_board)


    start_new_shop_turn(False)

def draw_battle():
    window.fill((80, 50, 40))

    draw_text(get_text("battle_phase"), title_font, (255, 255, 255), 420, 40)
    draw_text(f"{get_text("round")} {battle_round}", text_font, (255, 255, 255), 520, 100)

    draw_text(get_text("boss_board"), text_font, (255, 255, 255), 30, 150)

    for i, card in enumerate(boss_board):
        if card == attacker and battle_state in ["moving_to_target", "moving_back"]:
            continue

        rect = get_boss_card_rect(i)
        draw_card(card, rect)

    draw_text(get_text("your_board"), text_font, (255, 255, 255), 30, 430)

    for i, card in enumerate(board):
        if card == attacker and battle_state in ["moving_to_target", "moving_back"]:
            continue

        rect = get_player_card_rect(i)
        draw_card(card, rect)

    if attacker is not None and attacker_rect is not None:
        if battle_state in ["moving_to_target", "moving_back"]:
            draw_card(attacker, attacker_rect)

    mouse_pos = pg.mouse.get_pos()

    if dragging_card is None:
        # boss tooltip
        for i, card in enumerate(boss_board):
            rect = get_boss_card_rect(i)

            if rect.collidepoint(mouse_pos):
                draw_tooltip(card, mouse_pos)

        # player tooltip
        for i, card in enumerate(board):
            rect = get_player_card_rect(i)

            if rect.collidepoint(mouse_pos):
                draw_tooltip(card, mouse_pos)

    if message_timer > 0:
        draw_message(600, 400)


def show_message(text, duration=120):
    global message_text, message_timer

    message_text = text
    message_timer = duration

def draw_message(x=600, y=400):
    if message_timer <= 0:
        return

    message_surface = title_font.render(
        message_text,
        True,
        (255, 255, 255)
    )

    message_rect = message_surface.get_rect(center=(x, y))

    bg_rect = message_rect.inflate(20, 20)
    pg.draw.rect(window, (0, 0, 0), bg_rect)
    pg.draw.rect(
        window,
        (255, 255, 255),
        bg_rect,
        2
    )

    window.blit(message_surface, message_rect)

def play_music(path, volume=1):
    global current_music

    if current_music != path:
        pg.mixer.music.stop()
        pg.mixer.music.load(resource_path(path))
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.play(-1)  # -1 means loop forever
        current_music = path

def stop_music():
    global current_music

    pg.mixer.music.stop()
    current_music = None

#main game loop
isRunning = True

while isRunning == True:
    # change the background colour of the window
    window.fill((181, 136, 99))

    if game_state == "menu":
        play_music("music/menu.mp3")
        draw_menu()

    elif game_state == "guide":
        play_music("music/guide.mp3", 0.7)
        draw_guide()

    elif game_state == "language":
        draw_language()

    elif game_state == "game":
        play_music("music/game.mp3", 0.25)
        draw_game()

    elif game_state == "battle":
        play_music("music/fire.mp3")
        draw_battle()
        update_battle()

    elif game_state == "result":
        draw_result()

    #events loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False
            break

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if game_state == "menu":
                    if start_button.collidepoint(mouse_pos):
                        game_state = "game"
                        reset_game()

                    elif guide_button.collidepoint(mouse_pos):
                        game_state = "guide"

                    elif quit_button.collidepoint(mouse_pos):
                        isRunning = False

                    elif language_button.collidepoint(mouse_pos):
                        game_state = "language"

                elif game_state == "guide":
                    if back_button.collidepoint(mouse_pos):
                        game_state = "menu"

                elif game_state == "language":
                    if english_button.collidepoint(mouse_pos):
                        game_language = "English"
                    elif chinese_button.collidepoint(mouse_pos):
                        game_language = "Chinese"
                    elif back_button.collidepoint(mouse_pos):
                        game_state = "menu"


                elif game_state == "game":

                    # refresh shop
                    if refresh_button.collidepoint(mouse_pos):
                        if gold >= 1:
                            gold -= 1
                            gold_spent_this_turn += 1
                            return_shop_to_pool()
                            shop = generate_shop(real_minion_pool, battleground_level)
                        else:
                            show_message(get_text("not_enough_gold"))

                    # upgrade tavern
                    elif upgrade_button.collidepoint(mouse_pos):
                        upgrade_shop()

                    # end turn
                    elif end_turn_button.collidepoint(mouse_pos):
                        record_current_round_team()

                        if is_boss_round(round_number):
                            prepare_boss_battle()
                        else:
                            start_new_shop_turn(True)

                    #freeze
                    elif freeze_button.collidepoint(mouse_pos):
                        shop_frozen = not shop_frozen

                    # concede
                    elif concede_button.collidepoint(mouse_pos):
                        record_current_round_team()
                        export_run_history("Conceded")
                        game_state = "menu"
                        reset_game()

                    # buy minion

                    for i, minion in enumerate(shop):
                        card_rect = pg.Rect(120 + i * 140, 100, 120, 170)

                        if card_rect.collidepoint(mouse_pos):
                            dragging_card = minion
                            dragging_index = i
                            dragging_source = "shop"
                            dragging_rect = card_rect.copy()
                            drag_offset_x = card_rect.x - mouse_pos[0]
                            drag_offset_y = card_rect.y - mouse_pos[1]
                            break

                    for i, card in enumerate(hand):
                        hand_rect = pg.Rect(120 + i * 120, 600, 120, 170)

                        if hand_rect.collidepoint(mouse_pos):
                            dragging_card = card
                            dragging_index = i
                            dragging_source = "hand"
                            dragging_rect = hand_rect.copy()

                            drag_offset_x = hand_rect.x - mouse_pos[0]
                            drag_offset_y = hand_rect.y - mouse_pos[1]
                            break

                    for i, card in enumerate(board):
                        board_rect = get_board_card_rect(i)

                        if board_rect.collidepoint(mouse_pos):
                            dragging_card = card
                            dragging_index = i
                            dragging_source = "board"
                            dragging_rect = board_rect.copy()

                            drag_offset_x = board_rect.x - mouse_pos[0]
                            drag_offset_y = board_rect.y - mouse_pos[1]

                            break
                elif game_state == "result":
                    if back_button.collidepoint(mouse_pos):
                        game_state = "menu"
                        reset_game()

        elif event.type == pg.MOUSEMOTION:
            if game_state == "game" and dragging_card is not None:
                mouse_pos = event.pos
                if isinstance(dragging_card, Spell):
                    if dragging_source == "hand" and dragging_card.have_target:
                        pass
                    else:
                        dragging_rect.x = mouse_pos[0] + drag_offset_x
                        dragging_rect.y = mouse_pos[1] + drag_offset_y
                else:
                    dragging_rect.x = mouse_pos[0] + drag_offset_x
                    dragging_rect.y = mouse_pos[1] + drag_offset_y

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and game_state == "game" and dragging_card is not None:

                # SHOP → BUY
                if dragging_source == "shop":

                    if dragging_rect.colliderect(buy_zone):
                        if len(hand) < max_hand_card:
                            if isinstance(dragging_card, Minion):
                                cost = 3
                            elif isinstance(dragging_card, Spell):
                                cost = dragging_card.cost
                            if gold >= cost:

                                gold -= cost
                                gold_spent_this_turn += cost

                                hand.append(dragging_card)
                                shop.pop(dragging_index)



                            else:
                                show_message(get_text("not_enough_gold"))
                        else:
                            show_message(get_text("hand_is_full"))

                # HAND → BOARD / SPELL
                elif dragging_source == "hand":
                    # minion to board
                    if isinstance(dragging_card, Minion):
                        if dragging_rect.colliderect(board_zone):
                            play_minion_from_hand(dragging_index)

                    # spell to minion
                    elif isinstance(dragging_card, Spell):
                        if not dragging_card.have_target:
                            if dragging_rect.colliderect(spell_zone):
                                hand.pop(dragging_index)
                                cast_spell(dragging_card)

                        else:
                            mouse_pos = pg.mouse.get_pos()
                            for i, target in enumerate(board):
                                target_rect = get_board_card_rect(i)
                                if target_rect.collidepoint(mouse_pos):
                                    hand.pop(dragging_index)
                                    cast_target_spell(dragging_card, target)
                                    break

                elif dragging_source == "board":
                    if dragging_rect.colliderect(sell_zone):
                        sold_minion = board.pop(dragging_index)
                        if not sold_minion.derivant:
                            original_minion = get_original_minion(sold_minion.name)
                            if original_minion is not None:
                                real_minion_pool.append(copy.deepcopy(original_minion))

                        gold += 1
                        trigger_gold_tycoon_sell_effect()


                    else:
                        for i, target in enumerate(board):
                            target_rect = get_board_card_rect(i)
                            if dragging_rect.colliderect(target_rect):
                                board[dragging_index], board[i] = board[i], board[dragging_index]
                                break


                dragging_card = None
                dragging_index = None
                dragging_rect = None
                dragging_source = None

    pg.display.update()

    #set the frame rate
    if message_timer > 0:
        message_timer -= 1
    clock.tick(60)


#quit pygame
pg.quit()
