from setuptools import find_packages, setup

setup(name='pyat',
      use_vcs_version=True,
      description="Python wrapper for the `at` and `batch` commands",
      url='http://github.com/matt-hayden/PyAt',
	  maintainer="Matt Hayden",
	  maintainer_email="github.com/matt-hayden",
      license='Unlicense',
      packages=find_packages(),
	  install_requires = [
	    "python-dateutil >= 2.6.0",
      ],
	  entry_points = {
	    'console_scripts': [
		  'atgrep=pyat.shtools:atgrep',
		],
	  },
      zip_safe=True,
	  setup_requires = [ "setuptools_git >= 1.2", ]
     )
