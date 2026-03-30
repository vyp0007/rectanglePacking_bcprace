def sort_with_keys(data, keys):

    sorted_data = [x for _, x in sorted(zip(keys, data))]
    return sorted_data
