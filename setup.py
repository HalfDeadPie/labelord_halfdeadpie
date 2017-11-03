from setuptools import setup, find_packages


with open('README') as f:
    long_description = ''.join(f.readlines())


setup(
    name='labelord_halfdeadpie',
    version='0.3',
    description='Replicate Github Labels',
    long_description=long_description,
    author='Simon Stefunko',
    author_email='s.stefunko@gmail.com',
    keywords='labels, labelord',
    license='Public Domain',
    url='https://github.com/HalfDeadPie/labelord_halfdeadpie',
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
        'Framework :: Flask',
        'Environment :: Console',
        'Environment :: Web Environment'
        ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'labelord = labelord_halfdeadpie.unity:main',
        ],
    },
    install_requires=['Flask', 'click>=6', 'requests'],
    package_data={'labelord_halfdeadpie': ['templates/*.html']}
)
