#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

from pymongo import MongoClient

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):

    # helper function to create and append to dict
    def append_to_dict(term, k, node):
        items = k.split(":")

        if term not in node:
            node[term] = dict()

        if len(items) == 2:
            node[term][items[1]] = v

    node = {}
    if element.tag == "node" or element.tag == "way":
        # YOUR CODE HERE
        node["type"] = element.tag
        node["created"] = {}
        node["pos"] = [0, 0]

        for k, v in element.attrib.items():
            if k in CREATED:
                node["created"][k] = v
            elif k == 'lat':
                node["pos"][0] = float(v)
            elif k == 'lon':
                node["pos"][1] = float(v)
            else:
                node[k] = v

        for child in element:
            if child.tag == 'tag':
                k = child.attrib["k"]

                if re.search(problemchars, k):
                    pass
                elif k[:4] == "addr":
                    append_to_dict("addr", k, node)
                elif k[:4] == "gnis":
                    append_to_dict("gnis", k, node)
                elif k[:6] == "source":
                    append_to_dict("source", k, node)
                elif k[:5] == "tiger":
                    append_to_dict("tiger", k, node)
                elif k[:8] == "nycdoitt":
                    append_to_dict("nycdoitt", k, node)
                elif k[:8] == "building":
                    append_to_dict("building", k, node)
                elif k[:4] == "roof":
                    append_to_dict("roof", k, node)
                else:
                    node[k] = v
            elif child.tag == "nd":

                if "node_refs" not in node:
                    node["node_refs"] = list()
                node["node_refs"].append(child.attrib["ref"])

        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def insert_data(data):
    client = MongoClient("mongodb://localhost:27017")
    db = client.osm
    # clean the collection
    db.nyc.drop()
    # insert to the collection
    db.nyc.insert(data)

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('sample.osm', True)
    # pprint.pprint(data)
    insert_data(data)


if __name__ == "__main__":
    test()