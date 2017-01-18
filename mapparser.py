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


if __name__ == "__main__":
    tags = count_tags('sample.osm')
    pprint.pprint(tags)
