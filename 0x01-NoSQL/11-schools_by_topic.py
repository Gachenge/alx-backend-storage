#!/usr/bin/env python3
"""
list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """list school having specific topic"""
    return mongo_collection.find({"topics": topic})
