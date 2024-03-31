# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='getSourceCode',
    version='2.0.8',
    author='Shawn Xu',
    author_email='support@hxzy.me',
    url='https://github.com/5hawnXu/getSourceCode',
    description=u'Simple way to get contract source code verified on blockchain explorer.',
    long_description=open('README.rst', encoding='utf-8').read(),
    packages=['getSourceCode'],
    install_requires=[
        "retrying",
    ],
    entry_points={
        'console_scripts': [
            'getCode=getSourceCode:main',
        ]
    }
)
