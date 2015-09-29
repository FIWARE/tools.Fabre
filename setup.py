from setuptools import setup
import setuptools
import os
from os import mkdir, umask
from shutil import rmtree
import errno


def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(name='fiware_api_blueprint_renderer',
      version='0.3.1',
      description='Python module to aid with parsing FIWARE API specification files and rendering them to HTML pages.',
      url='https://github.com/FiwareULPGC/fiware-api-blueprint-renderer',
      author='FIWARE ULPGC',
      author_email='fiware@ulpgc.es',
      license='',
      packages=setuptools.find_packages(),
      include_package_data=True,
      data_files=[('/usr/share/man/man1', ['fiware_api_blueprint_renderer/man/fabre.1'])],
      install_requires=[
        'jinja2>=2.7.3',
        'markdown>=2.6.2',
        'mdx-linkify>=0.6'
      ],
      entry_points={
        'console_scripts': [
          'fabre = fiware_api_blueprint_renderer.src.renderer:main',
        ],
        'fiware_api_blueprint_renderer.themes': [
            'default = fiware_api_blueprint_renderer.themes.default_theme'
        ]
      },
      classifiers=[ 
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Documentation',
        'Topic :: Text Processing',
      ],
      zip_safe=False)

