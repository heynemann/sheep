#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sheep.shepherd import Shepherd


class Cons(Shepherd):
    def do_work(self):
        print self.config.KEY

if __name__ == "__main__":
    Cons.run()
