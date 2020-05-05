from setuptools import setup


setup(
    name='dNote',
    version='0.1.0',
    description='Simple CLI utility for managing notes with AWS',
    url='https://github.com/yetisir/dnote',
    author='M. Yetisir',
    author_email='yetisir@gmail.com',
    install_requires=[
        'boto3>=1.13',
        'nltk>=3.5',
        'configurator[yaml]>=2.0',
    ],
    extras_require={
        'dev': [
            'coveralls>=2.0',
            'mkdocs>=1.1',
            'pytest>=5.4',
            'pytest-cov>=2.8',
            'pytest-flake8>=1.0',
            'sphinx>=3.0',
        ],
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'dnote = dnote.__main__:main',
        ],
    },
)
