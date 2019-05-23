"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected

"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "columbusOH.osm"
OSMFILE_sample = "columbusOH_sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)  # Taken directly from Case Study


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]


# UPDATE THIS VARIABLE
mapping = {"St.": "Street",
           "St": "Street",
           "Ave": "Avenue",
           "Dr": "Drive",
           "Dr.": "Drive",
           "Pkwy": "Parkway",
           "RD": "Road",
           "Rd": "Road",
           "Rd.": "Road",
           "S": "South",  
           "S.": "South",
           "SW": "SouthWest",
           "rd": "Road",
           "E.": "East",
           "E": "East ",
           "W.": "West",
           "W": "West",
           "N.": "North",
           "N": "North",
           "Se": "SouthEast"
           }


def audit_street_type(street_types, street_name):  # Taken directly from Case Study
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def street_name(elem):  # Taken directly from Case Study
    return elem.attrib['k'] == "addr:street"


def string_case(s):
    return s.title()


def audit(osmfile):  # Taken directly from Case Study
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    name = name.split(' ')
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]
            name[i] = string_case(name[i])
        else:
            name[i]=string_case(name[i])

    name = ' '.join(name)

    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print(name, "=>", better_name)




if __name__ == '__main__':
    test()
