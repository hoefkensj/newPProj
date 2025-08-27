#!/usr/bin/env python

from dataclasses import dataclass,field


@dataclass()
class myclass:
	some: object=field(default=object())
	thing: object=field(default=object())


b=myclass(thing=6)
b.some='a'

print(b.__dict__())
