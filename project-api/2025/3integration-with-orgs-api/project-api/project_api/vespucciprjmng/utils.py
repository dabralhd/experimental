


def read_json_attribute(json_obj, key):
    if key in json_obj:
        return json_obj[key]
    else:
        return None