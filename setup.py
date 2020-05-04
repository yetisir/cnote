from setuptools import setup


setup(
    name='dNote',
    version='0.0.2',
    description='Simple CLI utility for managing notes with AWS',
    url='https://github.com/yetisir/dnote',
    author='M. Yetisir',
    author_email='yetisir@gmail.com',
    install_requires=[
        'boto3>=1.13',
        'nltk>=3.5',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'dnote = dnote.__main__:main',
        ],
    },
)
