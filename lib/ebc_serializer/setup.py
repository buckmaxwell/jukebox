import re
import setuptools

with open("ebc_serializer/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ebc_serializer",
    version=version,
    url="https://github.com/buckmaxwell/jukebox/tree/master/lib/ebc_serialzer",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pika>=1.1.0",],
)
