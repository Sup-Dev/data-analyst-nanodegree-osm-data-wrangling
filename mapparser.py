#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code looks for all types of tags in the dataset
"""
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
    # YOUR CODE HERE
    tag_dict = dict()

    for event, elem in ET.iterparse(filename):
        if elem.tag not in tag_dict:
            tag_dict[elem.tag] = 1
        else:
            tag_dict[elem.tag] += 1

    return tag_dict


def test():

    tags = count_tags('sample.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                    'member': 3,
                    'nd': 4,
                    'node': 20,
                    'osm': 1,
                    'relation': 1,
                    'tag': 7,
                    'way': 1}


if __name__ == "__main__":
    test()
