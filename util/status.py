"""
Status enumeration, convenience utility

by Athreya Murali
"""


from enum import Enum


class Status(Enum):
    IDLE = 1,
    FLYING = 2,
    UNRESPONSIVE = 3
