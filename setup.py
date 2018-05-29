from setuptools import setup
from strix.version import VERSION

description = "A web mircoframwork."


setup(
    name="strix",
    packages=[
        "strix",
        "strix.handlers",
        "strix.httplib",
        "strix.httputils",
        "strix.log",
        "strix.urls",
    ],
    install_requires=[
        "uvloop",
    ],
    version=VERSION,
    description=description,
    author="Youxun",
    author_email="youxun.zh@gmail.com",
    url="https://github.com/",
    download_url="https://github.com/{version}".format(version=VERSION),
    keywords=["web", "mirco", "framework"],
)
