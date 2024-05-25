from setuptools import setup, find_packages

setup(
    name="mpanalyze",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pyecharts',
    ],
    entry_points={
        'console_scripts': [
            'params_analyze=params_analyze.analyze:calculate_parameters',
        ],
    },
    author="Jiajun Li",
    author_email="2366876022@qq.com",
    description="A package for analyzing model parameters",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JJLi0427/Model_Params_Analyze",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)