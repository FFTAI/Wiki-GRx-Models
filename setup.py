from setuptools import find_packages
from distutils.core import setup

setup(
    name="Wiki-GRx-URDF",
    version="1.0.0",
    description="URDF files of Fourier robot",
    author="Jason Chen",
    author_email="xin.chen@fftai.com",
    license="Apache-2.0",
    packages=find_packages(),
    package_dir={},
    python_requires='>=3.7',
    scripts=[],
    install_requires=[]
)
