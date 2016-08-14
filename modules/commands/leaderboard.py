#! /usr/bin/env python2.7

from modules.commands.helpers import get_diff_ratio

def call(salty_inst, c_msg, **kwargs):
    msg_split = c_msg["message"].split(" ", 1)
    try:
        game = msg_split[1]
        twitch_game = False
    except IndexError:
        game = salty_inst.game
        twitch_game = True
    if not game:
        return
    success, response = salty_inst.sr_com_api.get_games({"name" : game}, **kwargs)

    if not success:
        return False, \
            "Error retrieving info from speedrun.com ({0})".format(response.status_code)

    for i in response["data"]:
        if twitch_game:
            if i["name"]["international"].lower() == game.lower():
                game_record = i
                break
        else:
            if get_diff_ratio.diff_ratio(game.lower(), i["names"]["international"].lower()) > .8:
                game_record = i
                break
            elif i["abbreviation"].lower() == game.lower():
                game_record = i
                break
    else:
        return False, "Could not find a suitable game match for {0}.".format(game)

    return True, game_record["weblink"]
