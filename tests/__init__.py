# -*- coding: utf-8 -*-

"""
tests
=====

Unit tests for flask_via.Via class.
"""

import mock
import unittest

from flask_via import Via


class TestVia(unittest.TestCase):

    def setUp(self):
        self.app = mock.MagicMock(config={})

    def test_init_app_raises_not_implemented(self):
        via = Via()

        with self.assertRaises(NotImplementedError) as e:
            via.init_app(self.app)

        self.assertEqual(
            str(e.exception),
            'VIA_ROUTES_MODULE is not defined in application configuration.')

    def test_init_app_raises_import_error(self):
        via = Via()
        self.app.config['VIA_ROUTES_MODULE'] = 'foo.bar'

        with self.assertRaises(ImportError):
            via.init_app(self.app)

    @mock.patch('flask_via.import_module')
    def test_init_app_raises_attribute_error(self, import_module):

        class Module(object):
            pass

        import_module.return_value = Module()

        via = Via()

        with self.assertRaises(AttributeError) as e:
            via.init_app(self.app, routes_module='foo.bar')

        self.assertEqual(
            str(e.exception),
            "'Module' object has no attribute 'routes'")

    @mock.patch('flask_via.import_module')
    def test_init_app_iterates_over_routes(self, import_module):
        routes = [
            mock.MagicMock(),
            mock.MagicMock()
        ]
        import_module.return_value = mock.MagicMock(routes=routes)

        via = Via()
        via.init_app(self.app, routes_module='foo.bar')

        for instance in routes:
            instance.add_to_app.assert_called_once_with(self.app)
