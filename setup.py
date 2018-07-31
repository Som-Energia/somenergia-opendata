#!/usr/bin/env python
from setuptools import setup, find_packages

readme = open("README.md").read()

setup(
	name = "somenergia_api",
	version = "1.0.0",
	description =
		"Som Energia API for opendata access",
	author = "Gisce SSL, Som Energia SCCL",
	author_email = "info@somenergia.coop",
	url = 'https://github.com/Som-Energia/somenergia-api',
	long_description = readme,
	license = 'GNU Affero General Public License v3 or later (AGPLv3+)',
	packages=find_packages(exclude=['*[tT]est*']),
	scripts=[
		'run_api.py',
	],
	install_requires=[
		'yamlns>=0.3', # earlier are not Py2 compatible
		'Flask',
		'psycopg2',
		'rednose',
		'nose',
		'b2btest',
		'coverage',
		'consolemsg',
		'wavefile',
		'lxml',
		'python-dateutil',
		'records',
		# somenergia-utils
	],
	include_package_data = True,
	test_suite = 'som_opendata',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Development Status :: 2 - Pre-Alpha',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Operating System :: OS Independent',
	],
)
# vim: noet ts=4 sw=4
