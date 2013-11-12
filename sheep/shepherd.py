#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import abspath, isabs
import argparse
import logging
import time
import signal

try:
    from derpconf.config import Config
except ImportError:
    print("DerpConf not available, likely during setup.py.")

try:
    from colorama import init
    init()
    from colorama import Fore, Style
except ImportError:
    print("Colorama not available, likely during setup.py.")

try:
    import psutil
except ImportError:
    print("psutil not available, likely during setup.py.")

from sheep import __version__


LOGS = {
    0: 'error',
    1: 'warning',
    2: 'info',
    3: 'debug'
}


class Shepherd(object):
    def __init__(self, arguments=None):
        if arguments is None:
            arguments = sys.argv[1:]

        self.options = self.parse_arguments(arguments)
        self.config = None
        self.children = []

        self.configure_log()
        self.load_config()
        self.initialize()

    def initialize(self):
        pass

    def get_description(self):
        return "%s%sShepherd%s (sheep v%s)" % (
            Fore.BLUE,
            Style.BRIGHT,
            Style.RESET_ALL,
            __version__
        )

    def config_parser(self, parser):
        pass

    def parse_arguments(self, arguments):
        parser = argparse.ArgumentParser(description=self.get_description())

        system_group = parser.add_argument_group('system')
        system_group.add_argument('--workers', '-w', type=int, default=1, help='Number of worker instances to start.')
        system_group.add_argument('--sleep', '-s', type=int, default=1, help='Number of seconds between jobs.')
        system_group.add_argument('--config', '-c', help='Path of configuration file to load for this worker.')
        system_group.add_argument(
            '--verbose', '-v', action='count', default=0,
            help='Log level: v=warning, vv=info, vvv=debug.'
        )
        self.config_parser(parser)

        return parser.parse_args(arguments)

    def get_config_class(self):
        return Config

    def load_config(self):
        if self.options.config is None:
            self.config = self.get_config_class()()
            return

        if not isabs(self.options.config):
            logging.debug("Configuration file {0} is not absolute. Converting to abspath".format(self.options.config))
            self.options.config = abspath(self.options.config)

        logging.info("Loading configuration file at {0}...".format(self.options.config))

        self.config = self.get_config_class().load(self.options.config)

    def should_continue_working(self):
        return True

    def do_work(self):
        pass

    def configure_log(self):
        log_level = LOGS[self.options.verbose].upper()
        logging.basicConfig(level=getattr(logging, log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Setting log-level to %s." % log_level)

    def handle_child_process(self, worker_name):
        name = self.get_description()

        def handle_sigterm(signal, frame):
            logging.info('[%s - %s] Terminating sheep with signal %s...' % (name, worker_name, signal))
            os._exit(0)

        signal.signal(signal.SIGTERM, handle_sigterm)
        signal.signal(signal.SIGINT, handle_sigterm)

        try:
            logging.info("[%s - %s] Starting to work..." % (name, worker_name))

            while self.should_continue_working():
                logging.info("[%s - %s] Doing work." % (name, worker_name))
                try:
                    self.do_work()
                except Exception:
                    err = sys.exc_info()
                    logging.error("%s%s[%s - %s] ERROR: %s" % (Fore.RED, Style.BRIGHT, name, worker_name, str(err[1])))
                    logging.exception(err)

                time.sleep(self.options.sleep)
        except KeyboardInterrupt:
            pass

    def start(self):
        name = self.get_description()

        logging.info("[%s - %s] Gathering %d sheep..." % (name, self.parent_name, self.options.workers))

        self.children = []

        for i in range(self.options.workers):
            worker_name = "%s%ssheep #%d%s" % (
                Fore.GREEN,
                Style.BRIGHT,
                i,
                Style.RESET_ALL
            )

            pid = os.fork()
            if not pid:
                self.handle_child_process(worker_name)
            else:
                self.children.append((i, pid))

        self.wait_for_children()

    @property
    def parent_name(self):
        return "%s%sShepherd%s" % (
            Fore.YELLOW,
            Style.BRIGHT,
            Style.RESET_ALL
        )

    def handle_signal(self, signal, frame):
        name = self.get_description()

        logging.info('[%s - %s] Shepherd going away after signal interrupt (Shepherd PID: %d, Signal: %d)...' % (
            name, self.parent_name, os.getpid(), signal
        ))

        self.kill_children()
        sys.exit(0)

    def wait_for_children(self):
        name = self.get_description()

        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

        try:
            while True:
                self.evaluate_children()
                time.sleep(self.options.sleep)
        except KeyboardInterrupt:
            logging.info('[%s - %s] Shepherd going away after user interrupt (Shepherd PID: %d)...' % (
                name, self.parent_name, os.getpid()
            ))

            self.kill_children()
            sys.exit(0)

    def evaluate_children(self):
        name = self.get_description()

        procs = []
        for worker_index, pid in self.children:
            worker_name = "%s%ssheep #%d%s" % (
                Fore.GREEN,
                Style.BRIGHT,
                worker_index,
                Style.RESET_ALL
            )

            proc = psutil.Process(pid)
            if proc.status not in (psutil.STATUS_ZOMBIE, ):
                procs.append((worker_index, pid))
            else:
                logging.info('[%s - %s] Reviving process for worker %s with pid %s...' % (
                    name, self.parent_name, worker_name, pid
                ))

                # killing the zombie
                proc.kill()
                proc.wait()

                pid = os.fork()
                if not pid:
                    self.handle_child_process(worker_name)
                    return
                else:
                    procs.append((worker_index, pid))

        self.children = procs

    def kill_children(self):
        name = self.get_description()
        for worker_index, pid in self.children:
            logging.info("[%s - %s] Terminating sheep number %d[%d]..." % (name, self.parent_name, worker_index, pid))
            os.kill(pid, signal.SIGTERM)
            os.waitpid(pid, 0)
            logging.info("[%s - %s] Sheep number %d[%d] terminated." % (name, self.parent_name, worker_index, pid))

    @classmethod
    def run(cls, arguments=None):
        shepherd = cls(arguments)
        shepherd.start()
