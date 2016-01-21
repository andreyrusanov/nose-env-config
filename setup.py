from distutils.core import setup

setup(
    name='nose_env_config',
    version='0.1.3',
    packages=['nose_env_config'],
    url='https://github.com/andreyrusanov/nose-env-config',
    license='MIT',
    author='Andrey Rusanov',
    author_email='rusanov.andrey.maiL@gmail.com',
    install_requires=['nose>=1.0.0'],
    entry_points={
        'nose.plugins.0.10': [
            'nose_env_config = nose_env_config:NoseEnvConfig',
        ]
    },
    test_suite='nose.collector',
    include_package_data=True,
    description='Plugin for Nose, which provides easy and flexible interface for environment variables configuration',
    long_description=open('README.md').read(),
    
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Topic :: Software Development :: Testing'
    ],
)
