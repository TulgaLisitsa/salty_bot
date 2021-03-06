#! /usr/bin/env python3.7

from modules.commands.helpers import get_category_string
from modules.commands.helpers import get_category_title
from modules.commands.helpers import time_formatter

HELP_TEXT = [
    "!splits <user?> <game?> <category?>",
    "Retrive pb splits from splits.io.  Will try and user game and category from title and streamer if live, else all are required."
]


def call(salty_inst, c_msg, **kwargs):
    msg_split = c_msg["message"].split(" ", 3)

    infer_category = False
    try:
        username = msg_split[1]
    except IndexError:
        username = salty_inst.channel
    try:
        game = msg_split[2]
    except IndexError:
        game = salty_inst.game
    try:
        category = msg_split[3]
    except IndexError:
        category = salty_inst.title
        infer_category = True

    success, response = salty_inst.splits_io_api.get_user_pbs(username, **kwargs)
    if not success:
        return False, \
            "Error retrieving info from splits.io ({0}).".format(response.status_code)
    game_pbs = []
    for i in response["pbs"]:
        if not i["game"]:
            continue
        if (i["game"]["name"] or "").lower() == game.lower():
            game_pbs.append(i)
        if (i["game"]["shortname"] or "").lower() == game.lower():
            game_pbs.append(i)
    game_categories = {x["category"]["name"]: x["category"]["name"] for x in game_pbs if x["category"]}

    if infer_category:
        category_finder = get_category_title.find_active_cat
    else:
        category_finder = get_category_string.find_active_cat

    cat_success, cat_response = category_finder(game_categories, category)
    if not cat_success:
        return False, cat_response

    pb_splits = [x for x in game_pbs if x["category"]["name"].lower() == cat_response.lower()][0]
    output_game = pb_splits["game"]["name"]
    msg = "{0}'s best splits for {1} {2} is {3} https://splits.io{4}".format(
        username.capitalize(),
        output_game,
        cat_response,
        time_formatter.format_time(pb_splits["time"]),
        pb_splits["path"]
    )
    return True, msg


def test(salty_inst, c_msg, **kwargs):
    assert True
