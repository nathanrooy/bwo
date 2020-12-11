 from setuptools import setup
import bwo

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bwo',
    version=bwo.__version__,
    author=bwo.__author__,
    author_email='nathanrooy@gmail.com',
    url='https://github.com/nathanrooy/bwo',
    description='Black Widow Optimization',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['bwo'],
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
