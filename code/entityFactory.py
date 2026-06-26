#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.player import Player
from code.enemy import Enemy


class EntityFactory:

    def __init__(self):
        pass

    def get_entity(self, entity_type):

        if entity_type == "player":
            return Player()

        if entity_type == "enemy":
            return Enemy()

        return None