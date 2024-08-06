import os
import re


def update_dict(dict_name, key_name, action_type, tick, ks_length=0):
    key_name_split = key_name.split('_')
    id = key_name_split[0] + '_' + key_name_split[1]
    if key_name in dict_name:
        current_value = dict_name[key_name]
        if action_type == 'KS':
            updated_value = current_value + '_' + ks_length + action_type + '_' + tick
            dict_name[key_name] = updated_value
        if action_type == 'BM':
            updated_value = current_value + '_BM_' + tick
            dict_name[key_name] = updated_value

    else:
        if action_type == 'KS':
            dict_name[key_name] = id + '_' + ks_length + 'KS_' + tick
        if action_type == 'BM':
            dict_name[key_name] = id + '_BM_' + tick


demo_path = 'C:/Users/Christian/PycharmProjects/pythonProject/demo_test_dir'
quoted = re.compile('"[^"]*"')
kill_streak_pattern = re.compile('[A-Za-z]+\s[A-Za-z]+:[0-9]+')

demos_processed = []
naming_dict = {}

f = open(demo_path + 'KillStreaks.txt', 'r')
for line in f:
    quoted_demo_name = quoted.findall(line)
    if len(quoted_demo_name) > 0:
        demo_name = quoted_demo_name[0].strip('"')
        if os.path.exists(demo_path + demo_name + '.dem'):
            if demo_name not in demos_processed:
                demos_processed.append(demo_name)

            name_and_tick_expr = line[line.find("(") + 1:line.find(")")]
            tick = name_and_tick_expr.split()[-1]
            if len(tick) > 3:
                tick = tick[:len(tick) - 3] + 'k'

            ks = kill_streak_pattern.findall(line)
            if len(ks) > 0:
                ks_length = ks[0][-1]
                update_dict(naming_dict, demo_name, 'KS', tick, ks_length)

            if "Player bookmark" in line:
                update_dict(naming_dict, demo_name, 'BM', tick)
        else:
            print(f'Warning: {demo_name} present in log file but not in directory')


for old_demo_name, new_demo_name in naming_dict.items():
    os.rename(demo_path + old_demo_name + '.dem', demo_path + new_demo_name + '.dem')
