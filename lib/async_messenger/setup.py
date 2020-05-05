import re
import setuptools

with open("async_messenger/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="async_messenger",
    version=version,
    url="https://github.com/buckmaxwell/jukebox/tree/master/lib/async_messenger",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pika>=1.1.0",],
)
