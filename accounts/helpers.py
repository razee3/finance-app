def standardize_input(input_string):
    return ','.join([item.strip().capitalize() for item in input_string.split(',') if item.strip()])
