from setuptools import setup


setup(
    name='cNote',
    version='0.4.5',
    description='Simple CLI utility for managing notes with AWS',
    url='https://github.com/yetisir/cnote',
    author='M. Yetisir',
    author_email='yetisir@gmail.com',
    install_requires=[
        'boto3>=1.13',
        'click>=7.1',
        'configurator[yaml]>=2.0',
        'dateparser>=0.7',
        'nltk>=3.5',

        # Dev Dependencies here for now as well untill pip-compile
        # supports extras_require
        'coveralls>=2.0',
        'mkdocs>=1.1',
        'pip-tools>=5.1',
        'pytest>=5.4',
        'pytest-cov>=2.8',
        'pytest-flake8>=1.0',

    ],
    extras_require={
        'dev': [
            'coveralls>=2.0',
            'mkdocs>=1.1',
            'pip-tools>=5.1',
            'pytest>=5.4',
            'pytest-cov>=2.8',
            'pytest-flake8>=1.0',
        ],
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cnote = cnote.__main__:main',
        ],
    },
)
