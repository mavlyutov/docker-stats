#!/usr/bin/env python

from setuptools import setup


if __name__ == '__main__':

    requirements = [
        'docker-py <= 1.10.6',
        'json'
    ]

    setup(
        name='docker-stats',
        version='0.0.3',

        license='Apache License, Version 2.0',
        author="Marat Mavlyutov",
        author_email="mavlyutov@yandex-team.ru",
        description='Docker stats wrapper which prints output in json',
        long_description=open('README.rst').read(),
        url='https://github.com/mavlyutov/docker-stats',
        install_requires=requirements,

        py_modules=['docker_stats'],
        entry_points={
            'console_scripts': [
                'docker-stats = docker_stats:main',
            ]
        }
    )
