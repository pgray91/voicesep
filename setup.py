from setuptools import setup, find_packages

setup(
    name="voicesep",
    version="1.0.0",
    description="Voice separation utility",
    url="",
    author="Patrick Gray",
    author_email="pgray9189@gmail.com",
    license="",
    packages=find_packages()
    install_requres=[
        "h5py",
        "music21",
        "numpy",
        "theano"
    ]
    test_suite="nose.collector",
    tests_require=["nose"]
)
