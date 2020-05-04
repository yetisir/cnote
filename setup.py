from setuptools import setup


setup(
    name='dNote',
    version='0.0.1',
    description='Simple CLI utility for managing notes on the cloud',
    url='https://github.com/yetisir/dnote',
    author='M. Yetisir',
    author_email='yetisir@gmail.com',
    install_requires=[
        'boto2==1.13'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'dnote = dnote.__main__:main',
        ],
    },
)
