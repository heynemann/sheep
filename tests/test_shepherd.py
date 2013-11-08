#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import TestCase
from preggy import expect

from sheep import Shepherd, __version__


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
        expect(shepherd.get_description()).to_equal("Shepherd (sheep v%s)" % __version__)

    def test_parse_arguments_can_parse_number_of_workers(self):
        shepherd = Shepherd(['--workers', '10'])
        expect(shepherd.options.workers).to_equal(10)

        shepherd = Shepherd(['-w', '5'])
        expect(shepherd.options.workers).to_equal(5)

    def test_parse_arguments_can_parse_configuration(self):
        shepherd = Shepherd(['--config', './config.py'])
        expect(shepherd.options.config).to_equal('./config.py')

    #def test_parse_arguments_can_get_help_text(self):
        #shepherd = Shepherd(['--help'])
