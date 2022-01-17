import json


def read_json(filename) -> dict:
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def write_json(filename, data) -> None:
    with open(filename, 'w') as f:
        json.dump(data, f)


def check_json(filename) -> dict:
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def check_args_zero(args, arg_list) -> bool:
    return all(arg in args for arg in arg_list)


def id_check(self) -> str:
    try:
        server_id = str(self.guild.id)
    except:
        server_id = str(self.author.id)
    return server_id


def check_args_one(args) -> bool:
    return args is not type(None)
    # return False if args is type(None)


def check_dict_data(data:dict) -> bool:
    try:
        print(data)
    except KeyError:
        return False
    else:
        return True


def get_duplicate_counters(old:int, new:int) -> int:
    return new - old


def check_duplicate_data(existing_data, new_data:list) -> list:
    del_key = []
    for i in range(len(existing_data)):
        for new_datum in new_data:
            if existing_data[i] == new_datum:
                del_key.append(new_datum)
    return del_key

# TODO: time commands function
# TODO: Merging functions to main.py
