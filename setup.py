#!/usr/bin/env python

from setuptools import setup


if __name__ == '__main__':
    setup(
        name='docker-stats',
        version='0.0.3',

        license='Apache License, Version 2.0',
        author="Marat Mavlyutov",
        author_email="mavlyutov@yandex-team.ru",
        description='docker stats, json way',
        long_description=open('README.rst').read(),
        url='https://github.com/mavlyutov/docker-stats',

        py_modules=['docker_stats'],
        entry_points={
            'console_scripts': [
                'docker-stats = docker_stats:main',
            ]
        }
    )
