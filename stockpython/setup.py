import setuptools

setuptools.setup(
    name='stock-portfolio-generator',
    version='0.0.1',
    author='Morgan Clarke',
    description='Generates a list of stock info',
    packages=['portfolio', 'tests'],
    entry_points={
        'console_scripts': ['portfolio=portfolio.portfolio_report:main']
    },
    install_requires=[
        "requests>=2.31.0",
        "requests-mock>=1.11.0",
        "pytest>=7.4.3",
        "pylint>=3.0.3"
    ]
)
