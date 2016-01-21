import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import nose
import nose.plugins

CONFIG_DEFAULT_SECTION = 'env'
CONFIG_DEFAULT_FILENAME = '.nose-env'
CONFIG_ENV_VARIABLE = 'NOSE_ENV_FILE'


class NoseEnvConfig(nose.plugins.Plugin):
    name = 'env-config'

    def options(self, parser, env):
        super(NoseEnvConfig, self).options(parser, env=env)
        parser.add_option(
            '--env-vars',
            dest='env_variables',
            default=None,
            help='List of env variables should be set',
        )

        parser.add_option(
            '--env-vars-file',
            dest='env_variables_file',
            default=None,
            help='Path to file with env variables',
        )

        parser.add_option(
            '--skip-env-vars-file',
            dest='skip_env_variables_file',
            action="store_true",
            help='Do not read from default env conf file',
        )

    def configure(self, options, conf):
        super(NoseEnvConfig, self).configure(options, conf)

        vars_from_file = self.read_from_file(options)
        if vars_from_file:
            for env_key, env_val in vars_from_file.items():
                os.environ[env_key] = env_val

        if options.env_variables:
            env_variables_to_override = self.parse_vars_from_cl(options.env_variables)
            if not isinstance(env_variables_to_override, dict):
                raise ValueError('Variables should be a dict')

            for env_key, env_val in env_variables_to_override.items():
                os.environ[env_key] = env_val

    def read_from_file(self, options):
        result = dict()
        env_file = None

        if options.env_variables_file:
            env_file = options.env_variables_file
        elif not options.skip_env_variables_file:
            if os.environ.get(CONFIG_ENV_VARIABLE):
                env_file = os.environ.get(CONFIG_ENV_VARIABLE)
            else:
                env_file = self.default_env_file

        if not env_file:
            return result

        env_file = os.path.abspath(env_file)
        parser = configparser.ConfigParser()
        parser.optionxform = str
        try:
            if env_file in parser.read(env_file):
                try:
                    parser.readfp(open(env_file))
                except AttributeError:
                    parser.read_file(open(env_file))
                result = dict(parser.items(CONFIG_DEFAULT_SECTION))
        except configparser.Error as exc:
            raise ValueError('{}'.format(str(exc)))
        else:
            return result

    def parse_vars_from_cl(self, params_string):
        try:
            not_filtered_params = filter(None, params_string.split(','))
            filtered_params = dict(map(lambda param: (param[0].strip(), param[1].strip()),
                                       [param.split('=') for param in not_filtered_params]))
        except IndexError:
            raise ValueError('Malformed string passed')
        return filtered_params

    @property
    def default_env_file(self):
        return os.path.join(os.getcwd(), CONFIG_DEFAULT_FILENAME)


if __name__ == '__main__':
    nose.main(addplugins=[NoseEnvConfig()])
