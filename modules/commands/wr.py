#! /usr/bin/env python2.7

from modules.commands.helpers import get_category_string
from modules.commands.helpers import get_category_title
from modules.commands.helpers import time_formatter

def call(salty_inst, c_msg, **kwargs):
    msg_split = c_msg["message"].split(" ", 2)
    infer_category = True
    search_game = True

    try:
        game = msg_split[1].lower()
        search_game = False
    except IndexError:
        game = salty_inst.game
    try:
        category = msg_split[2].lower()
        infer_category = False
    except IndexError:
        category = salty_inst.title

    if search_game:
        success, response = salty_inst.sr_com_api.get_games_search(game, embeds=["categories"])
        if not success:
            return False, \
                "Error retrieving games from speedrun.com ({0}).".format(response.status_code)

        for i in response["data"]:
            if i["names"]["international"] == game:
                found_categories = {x["name"] : x["id"] for x in i["categories"]["data"] if x["type"] == "per-game"}
                game_id = i["id"]
                break
        else:
            return False, "No game found for: {0}.".format(game)
    else:
        success, response = salty_inst.sr_com_api.get_games({"abbreviation":game}, embeds=["categories"])
        if not success:
            try:
                decode = response.json()
            except ValueError:
                decode = {"message": "Game {0} could not be found".format(game), "status" : 404}
            return False, "{0} ({1})".format(decode["message"], decode["status"])

        found_categories = {x["name"] : x["id"] for x in response["data"][0]["categories"]["data"] if x["type"] == "per-game"}
        game_id = response["data"][0]["id"]

    if infer_category:
        category_finder = get_category_title.find_active_cat
    else:
        category_finder = get_category_string.find_active_cat

    cat_success, cat_response = category_finder(found_categories, category)

    if not cat_success:
        return False, cat_response

    success, response = salty_inst.sr_com_api.get_leaderboards(
        game_id,
        found_categories[cat_response],
        embeds=["game", "players"],
        params={"top" : 1},
        **kwargs
    )
    if not success:
        return False, \
            "Error retrieving leaderboard from speedrun.com ({0}).".format(response.status_code)

    msg = "The current world record for {0} {1} is {2} by {3}.".format(
        response["data"]["game"]["data"]["names"]["international"],
        cat_response,
        time_formatter.format_time(response["data"]["runs"][0]["run"]["times"]["primary_t"]),
        response["data"]["players"]["data"][0]["names"]["international"]
    )
    if response["data"]["runs"][0]["run"]["videos"]:
        msg += " Video: {0}".format(response["data"]["runs"][0]["run"]["videos"]["links"][0]["uri"])
    if response["data"]["runs"][0]["run"]["splits"]:
        msg += " Splits: {0}".format(response["data"]["runs"][0]["run"]["splits"]["uri"])

    return True, msg

def test_output():
    return 0
