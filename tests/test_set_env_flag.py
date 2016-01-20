import os

from tests.base import PluginBaseTestCase, BaseFailMixin


class TestEnvVariablesCase(PluginBaseTestCase):
    args = [
        "--env-vars=blah=foo, blah2 = val1"
    ]

    def test_correct_string_passed(self):
        self.assertIn('blah', os.environ)
        self.assertIn('blah2', os.environ)
        self.assertEqual(os.environ['blah'], 'foo')
        self.assertEqual(os.environ['blah2'], 'val1')


class TestEnvVariablesFailCase(BaseFailMixin, PluginBaseTestCase):
    args = [
        "--env-vars=blah"
    ]

    def test_malformed_string(self):
        self.assertIn('Malformed string', self.error.message)
