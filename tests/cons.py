#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

from sheep.shepherd import Shepherd


class Cons(Shepherd):
    def do_work(self):
        print "trying to be nasty"
        ctypes.string_at(1)

if __name__ == "__main__":
    Cons.run()
