# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='getsourcecode',
    version='3.0.0',
    author='Shawn Xu',
    author_email='support@hxzy.me',
    url='https://github.com/5hawnXu/getsourcecode',
    description=u'Simple way to get contract source code verified on blockchain explorer.',
    long_description=open('README.rst', encoding='utf-8').read(),
    packages=['getsourcecode'],
    install_requires=[
        "tenacity",
        "packaging",
    ],
    entry_points={
        'console_scripts': [
            'getCode=getsourcecode:main',
        ]
    }
)