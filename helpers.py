def find_images(soup):
    img_tags = soup.find_all("img")
    img_urls = {}
    for img in img_tags:
        alt = img["alt"]
        src = img["src"]
        if "jpg" in alt:  # remove all non jpg images (icons etc.)
            img_urls[alt] = src[2:] # remove leading slashes
    return img_urls


def find_first_paragraph(soup):
    mw_empty_elt = soup.find("p", class_="mw-empty-elt")
    description = mw_empty_elt.find_next_sibling("p")
    return description.get_text()


def extract_table_data(soup):
    infobox = soup.find("table", class_="infobox biota")
    trs = infobox.find_all("tr")
    output_map = {}
    # find first header
    first_header = find_first_header(trs)
    if first_header == -1:
        print("hi")
        return output_map

    for table_element in trs[first_header:]:
        th = table_element.find("th")
        td = table_element.find_all("td")

        if th is not None:
            last_added_head = th.get_text().strip()
            output_map[last_added_head] = []

        if td:  # array not empty
            if len(td) > 1:  # entry has key itself
                header = td[0].get_text().strip()
                value = td[1].get_text().strip()
                output_map[last_added_head] = output_map[last_added_head] + [
                    {remove_unicode_chars(header): remove_unicode_chars(value)}
                ]
            else:
                value = td[0].get_text().strip()
                output_map[last_added_head] = output_map[last_added_head] + [
                    remove_unicode_chars(value)
                ]
    return output_map


def find_first_header(soup):
    for idx, table_element in enumerate(soup):
        th = table_element.find("th")
        if th is not None:
            return idx
    return -1


def remove_unicode_chars(str):
    string_encode = str.encode("ascii", "ignore")
    string_decode = string_encode.decode()
    return string_decode


def get_proper_json_from_raw_data(dict):
    proper_json = {}
    classification = {}

    for sub_dict in dict["table_data"]["Scientific classification"]:
        for key in sub_dict:
            sliced_key = key[:-1]
            if sliced_key in classification:
                if isinstance(classification[sliced_key], list):
                    classification[sliced_key] = classification[sliced_key] + [sub_dict[key]]
                else:
                    classification[sliced_key] = [classification[sliced_key]] + [sub_dict[key]]
            else:
                classification[sliced_key] = sub_dict[key]

    proper_json["classification"] = classification
    proper_json["images"] = dict["images"]
    proper_json["name"] = dict["table_data"]["Binomial name"][0]
    proper_json["description"] = dict["description"]

    return proper_json
