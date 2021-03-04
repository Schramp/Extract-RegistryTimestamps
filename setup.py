# encoding=utf-8
# file used by distutils to create a distributable package and generate requirements.txt
from setuptools import setup

package_name = "Registry_FILETIME_plugin"
version_string = "0.1.0"

dependencies = [
    "extraction-plugin==0.0.31",  # the plugin SDK
    "datetime",
    "pytz",
]

setup(
    name=package_name,
    version=version_string,
    author='Netherlands Forensic Institute',
    author_email='schramp@holmes.nl',
    description='Hansken Extraction Plugin: Registry FILETIME, '
                'the plugin parses registry values with 8 byte BIN values that decode to a date between 2010 and 2022 ',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['.'],
    include_package_data=True,
    install_requires=dependencies,
)
