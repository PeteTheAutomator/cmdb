import os

from setuptools import setup

setup(
    name='audit',
    version='0.1.0',
    description='RPM package auditing tool',
    url='https://github.com/PeteTheAutomator/cmdb.git',
    license='Apache 2.0',
    author='Peter Hehn',
    author_email='peter.hehn@yahoo.com',
    packages=[
        'cmdb_libs',
    ],
    include_package_data=True,
    scripts=[
        'scripts/audit',
        'scripts/query',
    ],
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Systems Administrators',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'requests',
    ],
)
