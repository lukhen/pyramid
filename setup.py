from setuptools import setup

requires = []

with open("requirements.txt") as req_file:
    for req in req_file:
        requires.append(req)


setup(
    name="app",
    install_requires=requires,
    entry_points={"paste.app_factory": ["main = app:main"]},
)
