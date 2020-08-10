def get_sheet_name(casc):
    """Return sheet name for provided CASC.

    Arguments:
        casc -- (string) The string name of a CASC
    Returns:
        sheet_name -- (string) the name of the corresponding sheet.

    """
    if casc.lower() == "Northwest CASC".lower():
        sheet_name = "NW"
    elif casc.lower() == "Southwest CASC".lower():
        sheet_name = "SW"
    elif casc.lower() == "Pacific Islands CASC".lower():
        sheet_name = "PI"
    else:
        return None
    return sheet_name


def parse_values(values):
    """Create a new dictionary version from the sheet values passed in.

    Arguments:
        values -- (list) a 2d list of values from the google sheet
    Returns:
        new_sheet -- (dictionary) a dictionary representation of 'values'

    """

    new_sheet = {}
    header = values[0]
    values = values[1:]  # Shave off the first item (header)

    for i in values:
        proj_id = '' if i[2] is None else i[2]

        folder_url = "https://www.sciencebase.gov/catalog/folder/"
        item_url = "https://www.sciencebase.gov/catalog/item/"

        if folder_url in proj_id:
            proj_id = proj_id.replace(folder_url, '')
        if item_url in proj_id:
            proj_id = proj_id.replace(item_url, '')
        if '/' in proj_id:
            # in case there is a trailing slash
            proj_id = proj_id.replace('/', '')

        if proj_id != '':
            new_sheet[proj_id] = {}
            for n in range(0, len(header)):
                headerVal = header[n]
                try:
                    val_val = i[n]
                except IndexError:
                    val_val = "No Info Provided"
                new_sheet[proj_id][headerVal] = val_val

    return new_sheet
