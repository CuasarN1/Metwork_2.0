from setuptools import setup

APP = ['App.py']
OPTION = {
    'argv_emulation': True
}

setup(
    app=APP,
    options={'py2app': OPTION},
    setup_requires=['py2app']
)
