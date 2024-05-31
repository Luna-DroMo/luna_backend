def convert_dictionary(dict_list):
    result = [item["value"] + 1 for item in dict_list]
    return result


def convert_form_dictionary(dict_list):
    result = []
    if isinstance(dict_list, dict):
        dict_list = [dict_list]
    if isinstance(dict_list, list):
        for item in dict_list:
            if item is not None and isinstance(item, dict):
                temp_result = []
                for key, value in item.items():
                    if value is not None:
                        temp_result.append(int(value))
                    else:
                        print("Encountered None value for key:", key)
                if temp_result:
                    result.append(temp_result)
            else:
                print("Encountered non-dictionary item:", item)
    else:
        print("Input is not a list:", dict_list)
    return result
