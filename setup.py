from setuptools import setup

APP = ['src/main.py']
DATA_FILES = ['drawable', 'plot', 'sound', 'stats']
APP_NAME = "Meow Hero"

OPTIONS = {
    'argv_emulation': True,
    'includes': ('pygame'),
}
setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)