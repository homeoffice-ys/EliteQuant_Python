# encoding: UTF-8
from __future__ import print_function

from pandas import Timestamp
from enum import Enum

class EventType(Enum):
    TICK = 0
    BAR = 1
    ORDER = 2
    FILL = 3
    CANCEL = 4
    ACCOUNT = 5
    POSITION = 6
    TIMER = 7
    GENERAL = 8

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