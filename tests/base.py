import unittest
from nose.plugins import PluginTester
from nose_env_config import NoseEnvConfig


class PluginBaseTestCase(PluginTester, unittest.TestCase):
    activate = '--with-env-config'  # enables the plugin
    plugins = [NoseEnvConfig()]

    def makeSuite(self):
        class TC(unittest.TestCase):
            def runTest(self):
                raise ValueError("We should never get here")

        return unittest.TestSuite([TC()])


class BaseFailMixin(object):
    def setUp(self):
        # gracefully stolen from https://github.com/klrmn/nose-selenium/blob/master/tests/test_configuration.py
        self.error = None
        try:
            super(BaseFailMixin, self).setUp()
        except ValueError as e:
            self.error = e
