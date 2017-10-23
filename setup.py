from setuptools import setup

setup(
    name="http-server",
    description="Socket Echo Server",
    version=0.1,
    author="Robert Bronson, Allan Liebold",
    licence="MIT",
    py_modules=['server', 'client'],
    package_dir={'': 'src'}
)