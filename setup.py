import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="interpolML",
    version="1.0.0",
    python_requires=">=3.7",
    long_description=long_description,
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="MIT",
    zip_safe=True,
)