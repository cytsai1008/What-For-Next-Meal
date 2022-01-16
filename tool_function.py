import json


def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)


def check_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def check_args_zero(args, arg_list):
    return all(arg in args for arg in arg_list)


def id_check(message):
    try:
        server_id = str(message.guild.id)
    except:
        server_id = str(message.author.id)
    return server_id


def check_args_one(args):
    return args is not type(None)


def check_dict_data(data):
    try:
        print(data)
    except KeyError:
        return False
    else:
        return True


def get_duplicate_counters(old, new):
    return new - old


def check_duplicate_data(existing_data, new_data):
    del_key = []
    for i in range(len(existing_data)):
        for j in range(len(new_data)):
            if existing_data[i] == new_data[j]:
                del_key.append(new_data[j])
    return del_key

# TODO: time commands function
# TODO: Merging functions to main.py
