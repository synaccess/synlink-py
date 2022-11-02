from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name="synlinkpy",
    version="0.1.0",
    packages=['synlinkpy'],
    description="A SynLink PDU API Client",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Synaccess",
    author_email="support@synaccess.com",
    url="https://synaccess.com",
    install_requires=['requests >= 2.2.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='synlink pdu api client',
)
