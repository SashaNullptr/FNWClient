from setuptools import setup, find_packages

setup(
    name='fnw_client',
    version='0.1.0',
    packages=find_packages(exclude=[ 'docs' ]),
    install_requires=['numpy',
                      'scipy',
                      'pandas',
                      'textblob',
                      'telethon'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Linux',
        'Topic :: Natural Language Processing',
    ),
    author='Sasha E. Fox'
)
