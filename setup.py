from setuptools import find_packages, setup

setup(name='pyat',
      use_vcs_version=True,
      description='Parser for a hideous yet powerful taxonomic description syntax',
      url='http://github.com/matt-hayden/PyAt',
	  maintainer="Matt Hayden",
	  maintainer_email="github.com/matt-hayden",
      license='Unlicense',
      packages=find_packages(),
	  install_requires = [
	    "dateutil >= 2.6.0",
	    "docopt >= 0.6.2",
      ],
	  entry_points = {
	    'console_scripts': [
		  'atgrep=pyat.tools:atgrep',
		],
	  },
      zip_safe=True,
	  setup_requires = [ "setuptools_git >= 1.2", ]
     )
