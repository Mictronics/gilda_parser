from enum import Enum


class ImtApexHeaderFields(Enum):
    Command = 0
    Channel = 4
    Destination = 5
    Monitor = 6
    Time_s = 7
    Time_ms = 11
    Length = 15
    Flags = 17
