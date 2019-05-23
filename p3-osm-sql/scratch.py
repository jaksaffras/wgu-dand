# holds my pieces as I move them around

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
    print('%s: %d' % (k, v))


def update_name(name, mapping, regex):
    m = regex.search(name)
    if m:
        st_type = m.group()
        if st_type in mapping:
            name = re.sub(regex, mapping[st_type], name)
return name

def test():
    st_types = audit(OSMFILE_sample )
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"

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



def update_name(name, mapping):   # modified from Case Study
    m = street_type_re.search(name)
    compass = compass_re.search(name)
    new_name = name
    if m:
        # fork off street names that end in a word, Cardinal directions will skip to next
        if m.group() in mapping.keys():
            new_st_type = mapping[m.group()]
            new_name = street_type_re.sub(new_st_type, name)

        if compass:
            if compass.group() in mapping.keys():
                new_st_type = mapping[compass.group()]
                new_name = compass_re.sub(new_st_type, name)

            street_list = new_name.split()
            old_tail = street_list[-1]
            del street_list[-1]
            street_list.insert(0, old_tail)
            temp_name = ' '.join(street_list)
            d = street_type_re.search(temp_name)
            if d:
                if d.group() in mapping.keys():
                    new_st_type = mapping[d.group()]
                    new_name = street_type_re.sub(new_st_type, new_name)
    return new_name

Copeland Mill Rd #2D <-- Remove
8906
Us 42
8877
8897
4 North Vine
South Hamilton Road #210
