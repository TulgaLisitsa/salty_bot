#! /usr/bin/env python2.7

import re

import modules.extensions.regexes as regexes
import modules.commands.helpers.time_formatter as time_formatter

def call(salty_inst, c_msg, **kwargs):
    beatmaps = re.findall(regexes.OSU_URL, c_msg["message"])
    final_list = []
    for i in beatmaps:
        success, response = salty_inst.osu_api.get_beatmap("{0}={1}".format(i[0], i[1]), **kwargs)
        if not success:
            continue
        final_list.append("[{0}] {1} - {2}, mapped by {3} ({4} stars".format(
            time_formatter.format(response[0]["total_length"]),
            response[0]["artist"],
            response[0]["title"],
            response[0]["creator"],
            round(response[0]["difficultyrating"], 2)
        ))

    if len(final_list) == 0:
        return False, "No valid beatmaps linked."

    return True, " | ".join(final_list)