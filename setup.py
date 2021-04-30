#!/usr/bin/env python
from setuptools import setup, find_packages
from som_opendata import __version__

readme = open("README.md").read()

setup(
	name = "somenergia-opendata",
	version = __version__,
	description =
		"Som Energia API for opendata access",
	author = "Gisce SSL, Som Energia SCCL",
	author_email = "info@somenergia.coop",
	url = 'https://github.com/Som-Energia/somenergia-api',
	long_description = readme,
	long_description_content_type = 'text/markdown', 
	license = 'GNU Affero General Public License v3 or later (AGPLv3+)',
	packages=find_packages(exclude=['*[tT]est*']),
	scripts=[
		'run_api.py',
	],
	install_requires=[
		'yamlns>=0.7', # earlier are not Py2 compatible
		'Flask',
		'Flask-Cors',
		'psycopg2-binary',
		'rednose',
		'nose',
		'b2btest',
		'coverage',
		'consolemsg>=0.3.3',
		'wavefile',
		'lxml',
		'python-dateutil',
		'records',
		'tablib',
		'somutils',
		'colour',
		'babel',
		'Wand', #make gifs
		'flask-babel',
		'decorator',
		'python-slugify',
		'future', # Py2 backward compat
		'pathlib2', # Py2 backward compat
		'numpy<1.20', # 1.20 does not support Py 3.6.x
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
