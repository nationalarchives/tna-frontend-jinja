import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tna-frontend-jinja",
    version="0.2.18",
    author="Andrew Hosgood",
    author_email="andrew.hosgood@nationalarchives.gov.uk",
    description="TNA Frontend Jinja templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nationalarchives/tna-frontend-jinja",
    project_urls={
        "Bug Tracker": "https://github.com/nationalarchives/tna-frontend-jinja/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    packages=["tna_frontend_jinja"],
    package_data={
        "": ["**/*.html"],
    },
    python_requires=">=3.8",
    install_requires=["flask>=2"],
)
