import numpy as np


def convert_dictionary(dict_list):
    result = [item["value"] for item in dict_list]
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


def merge_survey_with_form(survey, form):
    """Merges a survey (or already concatenated matrix) with interindividual data"""
    form_extended = np.broadcast_to(form, (survey.shape[0], form.shape[0]))
    result = np.concatenate((survey, form_extended), axis=1)
    return result
