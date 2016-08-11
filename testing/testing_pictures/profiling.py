#! /usr/bin/sage -python
# -*- coding: utf8 -*-

import cProfile
from phystricks import *

from phystricksBLA import BLA

def profile_me():
    cProfile.run("BLA()")
    return "ok"

profile_me()
