#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import abspath
import time
import signal

from preggy import expect
from derpconf.config import Config

from sheep import Shepherd, __version__
from tests import TestCase


class TestShepherd(TestCase):
    def test_can_create_shepherd(self):
        shepherd = Shepherd([])
        expect(shepherd).not_to_be_null()
        expect(shepherd.options).not_to_be_null()

    def test_config_parser_does_nothing(self):
        shepherd = Shepherd([])
        expect(shepherd.config_parser(None)).to_be_null()

    def test_get_description(self):
        shepherd = Shepherd([])
        expect(shepherd.get_description()).to_be_like("Shepherd (sheep v%s)" % __version__)

    def test_parse_arguments_can_parse_number_of_workers(self):
        shepherd = Shepherd(['--workers', '10'])
        expect(shepherd.options.workers).to_equal(10)

        shepherd = Shepherd(['-w', '5'])
        expect(shepherd.options.workers).to_equal(5)

    def test_parse_arguments_can_parse_worker_name(self):
        shepherd = Shepherd([])
        expect(shepherd.options.name).to_equal('sheep')

        shepherd = Shepherd(['--name', 'aries'])
        expect(shepherd.options.name).to_equal('aries')

        shepherd = Shepherd(['-n', 'aries'])
        expect(shepherd.options.name).to_equal('aries')

    def test_parse_arguments_can_parse_configuration(self):
        shepherd = Shepherd(['--config', './tests/cons.conf'])
        expect(shepherd.options.config).to_equal(abspath('./tests/cons.conf'))

    def test_do_work_does_nothing_by_default(self):
        shepherd = Shepherd([])
        expect(shepherd.do_work()).to_be_null()

    def test_load_config_returns_if_no_config(self):
        shepherd = Shepherd([])
        shepherd.load_config()

        expect(shepherd.config).not_to_be_null()
        expect(shepherd.config).to_be_instance_of(Config)

    def test_load_config_loads_configuration_file(self):
        shepherd = Shepherd(["-c", "./tests/cons.conf"])
        shepherd.load_config()

        expect(shepherd.config.KEY).to_equal("doing something...")

    def test_should_continue_working(self):
        shepherd = Shepherd([])

        expect(shepherd.should_continue_working()).to_be_true()

    def test_configure_log(self):
        shepherd = Shepherd(['-vvv'])
        shepherd.configure_log()
        # unfortunately this test can't assert anything because nose
        # basicConfig for logging runs before sheep's

    def test_handle_child_process(self):
        class Shep(Shepherd):
            def __init__(self, *args, **kw):
                super(Shep, self).__init__(*args, **kw)
                self.has_run = False

            def do_work(self):
                os.kill(os.getppid(), signal.SIGINFO)

        shepherd = Shep(['-vvv'])

        pid = os.fork()

        if pid:
            def handle_signal(signum, value):
                expect(signum).to_equal(29)
                os.kill(pid, signal.SIGTERM)
                os.waitpid(pid, 0)

            signal.signal(signal.SIGINFO, handle_signal)

            time.sleep(1)
        else:
            shepherd.handle_child_process("worker")
