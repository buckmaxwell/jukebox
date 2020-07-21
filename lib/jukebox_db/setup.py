import re
import setuptools

with open("jukebox_db/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jukebox_db",
    version=version,
    url="https://github.com/buckmaxwell/jukebox/tree/master/lib/jukebox_db",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["SQLAlchemy==1.3.16", "psycopg2-binary==2.8.5"],
)
