from setuptools import setup

APP = ['myip_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': '', # We don't have an icon file yet, relying on default
    'plist': {
        'LSUIElement': True, # This hides the app from the Dock (Menu bar only)
        'CFBundleName': 'MyIP',
        'CFBundleDisplayName': 'MyIP',
        'CFBundleIdentifier': 'com.user.myip',
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
    },
    'packages': ['rumps', 'requests', 'idna', 'urllib3', 'certifi', 'charset_normalizer'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
