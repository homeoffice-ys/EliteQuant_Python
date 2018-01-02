#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import Timestamp
from enum import Enum

class EventType(Enum):
    TICK = 0
    BAR = 1
    ORDER = 2
    FILL = 3
    CANCEL = 4
    ORDERSTATUS = 5
    ACCOUNT = 6
    POSITION = 7
    TIMER = 8
    GENERAL = 9

class Event(object):
    """
    Base Event class for event-driven system
    """
    @property
    def typename(self):
        return self.type.name

class GeneralEvent(Event):
    """
    General event: TODO seperate ErrorEvent
    """
    def __init__(self):
        self.event_type = EventType.GENERAL
        self.time = Timestamp('1970-01-01', tz='UTC')
        self.content = ""