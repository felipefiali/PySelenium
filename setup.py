from setuptools import setup


try:
    from m2r import parse_from_file
    long_description = parse_from_file('README.md')
except:
    long_description = ''

setup(
    name='PySelenium',
    license='MIT License',
    packages=['pyselenium'],
    version='1.0.2',
    description='A wrapper for Selenium to allow easy development of automated tests for the web',
    author='Felipe Fiali de Sá',
    author_email='felipefiali@gmail.com',
    url='https://github.com/felipefiali/PySelenium',
    download_url='https://github.com/felipefiali/PySelenium/archive/1.0.2.tar.gz',
    keywords=['testing', 'test-automation', 'selenium', 'web-automation'],
    long_description=long_description,
    platforms=[
        'Windows',
        'Linux',
        'MacOS'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities'
    ],
    install_requires=[
        "selenium"
    ]
)
