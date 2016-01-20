import os

from nose_env_config.plugin import CONFIG_DEFAULT_FILENAME, \
    CONFIG_DEFAULT_SECTION, \
    CONFIG_ENV_VARIABLE
from .base import PluginBaseTestCase
from .test_set_env_file_flag import FileBasedEnvConfMixin


class CreateFilesMixin(FileBasedEnvConfMixin):
    def create_random_file(self, data):
        filename = CONFIG_DEFAULT_FILENAME[::-1]
        self.__create_file(filename, data)
        return filename

    def create_file_for_env(self, data):
        filename = '.env_{}'.format(CONFIG_DEFAULT_FILENAME[::-1])
        self.__create_file(filename, data)
        return filename

    def create_default_file(self, data):
        filename = CONFIG_DEFAULT_FILENAME
        self.__create_file(filename, data)
        return filename

    def __create_file(self, filename, data):
        current_path = os.path.dirname(__file__)
        path = os.path.join(current_path, '..', filename)
        self.addCleanup(lambda file_path: os.remove(file_path), path)
        self.create_env_config(path, data)


class TestFullPriorities(PluginBaseTestCase):
    args = [
        '--env-vars-file={}'.format(os.path.join(current_path, CONFIG_DEFAULT_FILENAME[::-1])),
    ]
    def setUp(self):
        os.environ[CONFIG_ENV_VARIABLE] = ''
        super(TestFullPriorities, self).setUp()
