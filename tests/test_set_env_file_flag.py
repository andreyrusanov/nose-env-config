import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from nose_env_config.plugin import CONFIG_DEFAULT_FILENAME, CONFIG_DEFAULT_SECTION, CONFIG_ENV_VARIABLE
from tests.base import PluginBaseTestCase

current_path = os.path.dirname(__file__)


class FileBasedEnvConfMixin(object):
    def create_env_config(self, path, values):
        config = configparser.RawConfigParser()
        config.optionxform = str

        sections = list(set([section['section'] for section in values.values()]))

        for section in sections:
            config.add_section(section)

        for key, value in values.items():
            config.set(value['section'], key, value['value'])

        with open(path, 'w') as configfile:
            config.write(configfile)


class TestEnvVariablesDefaultFileCase(FileBasedEnvConfMixin, PluginBaseTestCase):

    def setUp(self):
        current_path = os.path.dirname(__file__)
        filename = CONFIG_DEFAULT_FILENAME
        path = os.path.join(current_path, '..', filename)
        self.addCleanup(lambda file_path: os.remove(file_path), path)
        self.correct_section = CONFIG_DEFAULT_SECTION
        self.wrong_section = CONFIG_DEFAULT_SECTION[::-1]

        self.vars_to_set = dict(
            var1=dict(value='val1', section=self.correct_section),
            VAR2=dict(value='VAL2', section=self.correct_section),
        )

        self.vars_not_to_set = dict(var3=dict(value='val3', section=self.wrong_section),
                                    VAR4=dict(value='val4', section=self.wrong_section))

        data = dict()
        data.update(self.vars_to_set)
        data.update(self.vars_not_to_set)
        self.create_env_config(path, data)
        super(TestEnvVariablesDefaultFileCase, self).setUp()

    def test_success(self):
        for var, val in self.vars_to_set.items():
            self.assertIn(var, os.environ)
            self.assertEqual(os.environ[var], val['value'])

        for var in self.vars_not_to_set.keys():
            self.assertNotIn(var, os.environ)


class TestEnvVariablesCustomFileCase(FileBasedEnvConfMixin, PluginBaseTestCase):
    args = [
        '--env-vars-file={}'.format(os.path.join(current_path, CONFIG_DEFAULT_FILENAME[::-1]))
    ]

    def setUp(self):
        filename = CONFIG_DEFAULT_FILENAME[::-1]
        path = os.path.join(current_path, filename)

        self.addCleanup(lambda file_path: os.remove(file_path), path)
        self.correct_section = CONFIG_DEFAULT_SECTION
        self.wrong_section = CONFIG_DEFAULT_SECTION[::-1]

        self.vars_to_set = dict(
            var1=dict(value='val1', section=self.correct_section),
            VAR2=dict(value='VAL2', section=self.correct_section),
        )

        self.vars_not_to_set = dict(var3=dict(value='val3', section=self.wrong_section),
                                    VAR4=dict(value='val4', section=self.wrong_section))

        data = dict()
        data.update(self.vars_to_set)
        data.update(self.vars_not_to_set)
        self.create_env_config(path, data)
        super(TestEnvVariablesCustomFileCase, self).setUp()

    def test_success(self):
        for var, val in self.vars_to_set.items():
            self.assertIn(var, os.environ)
            self.assertEqual(os.environ[var], val['value'])

        for var in self.vars_not_to_set.keys():
            self.assertNotIn(var, os.environ)

#
# class TestEnvVariablesFromEnvFileCase(FileBasedEnvConfMixin, PluginBaseTestCase):
#
#     def setUp(self):
#         filename = CONFIG_DEFAULT_FILENAME[::-1]
#         path = os.path.join(current_path, filename)
#
#         self.addCleanup(lambda file_path: os.remove(file_path), path)
#         self.correct_section = CONFIG_DEFAULT_SECTION
#         self.wrong_section = CONFIG_DEFAULT_SECTION[::-1]
#
#         self.vars_to_set = dict(
#             var1=dict(value='val1', section=self.correct_section),
#             VAR2=dict(value='VAL2', section=self.correct_section),
#         )
#
#         self.vars_not_to_set = dict(var3=dict(value='val3', section=self.wrong_section),
#                                     VAR4=dict(value='val4', section=self.wrong_section))
#
#         data = dict()
#         data.update(self.vars_to_set)
#         data.update(self.vars_not_to_set)
#         self.create_env_config(path, data)
#         os.environ[CONFIG_ENV_VARIABLE] = path
#
#         super(TestEnvVariablesFromEnvFileCase, self).setUp()
#
#     def test_success(self):
#         for var, val in self.vars_to_set.items():
#             self.assertIn(var, os.environ)
#             self.assertEqual(os.environ[var], val['value'])
#
#         for var in self.vars_not_to_set.keys():
#             self.assertNotIn(var, os.environ)
