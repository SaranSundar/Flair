import os
from sys import platform as _platform


from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
REQUIRES_PYTHON = '>=3.0.0'
REQUIRED_DEP = ['flask', 'flask_sockets', 'flask_cors']
about = {}

NAME = 'Flair'

with open('README.md') as readme_file:
    readme = readme_file.read()

# OS specific settings
SET_REQUIRES = []
if _platform == "linux" or _platform == "linux2":
    # linux
    print('linux')
elif _platform == "darwin":
    # MAC OS X
    SET_REQUIRES.append('py2app')

APP = ['flair.py']

OPTIONS = {
    'argv_emulation': False,
    'strip': True,
    'packages': ['flask', 'werkzeug', 'jinja2', 'gevent', 'geventwebsocket', 'flask_cors'],
    'includes': ['WebKit', 'Foundation', 'webview', 'sys', 'subprocess', 'os'],
    'resources': ['./templates', './static'],
}

setup(
    app=APP,
    name=NAME,
    version='1.0',
    description="Flair - Build cross platform desktop apps with JavaScript (ReactJS), Python, HTML, and CSS",
    long_description=readme,
    author="Saran Sundararajan",
    author_email='saransszg@gmail.com',
    url='https://github.com/SaranSundar/Flair',
    python_requires=REQUIRES_PYTHON,
    package_dir={'Flair': '.'},
    include_package_data=True,
    install_requires=REQUIRED_DEP,
    license="MIT license",
    zip_safe=False,
    keywords='Flair - Cross Platform Desktop Apps, JavaScript, ReactJS, Python, HTML, CSS',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    options={'py2app': OPTIONS},
    setup_requires=SET_REQUIRES,
)
