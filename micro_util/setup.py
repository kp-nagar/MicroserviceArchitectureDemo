import setuptools


setuptools.setup(
    name="micro_util",
    version="0.3",
    install_requires=[
        "setuptools==61.0"
    ],
    author="Kumarpal Nagar",
    author_email="kumarpal.nagar@gmail.com",
    description="Micro-service library which contains Common functionality.",
    long_description="This is library which help to connect micro-services.",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)