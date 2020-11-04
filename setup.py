#from setuptools import find_packages, setup
from distutils.core import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="NaptanTools",
    version="0.3",
    description="Tools to check the validate of a specified UK region of Naptan data.",
    long_description=long_description,
    author="DfT Data Unit",
    url="https://github.com/departmentfortransport/Open_NaPTAN",
    author_email="naptan.nptg@dft.gov.uk",
    package_dir={"": "src"},
    # packages=find_packages(),
    py_modules=['cons', 'geos', 'etl', 'report', 'visualise'],
    scripts=["src/main.py"],
    license='MIT',
    classifiers=["Programming Language:: Python:: 3",
                 "Operating System :: OS Independent",
                 ],
    install_requires=[
        'geopandas',
        'pandas',
        'numpy',
        'shapely',
        'matplotlib',
        'folium'],
)
