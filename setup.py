from setuptools import setup, find_packages


with open('README') as f:
    long_description = ''.join(f.readlines())


setup(
    name='labelord',
    version='0.3',
    description='Replicate Github Labels',
    long_description=long_description,
    author='Simon Stefunko',
    author_email='s.stefunko@gmail.com',
    keywords='labels, labelord',
    license='Public Domain',
    #url='https://gist.github.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: PyCharm',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'labelord = labelord.labelord:main',
        ],
    },
    install_requires=['Flask', 'click>=6', 'requests']
)
