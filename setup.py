import setuptools

with open("README.md", "r")as fh:
    long_description = fh.read()

setuptools.setup(
    name= "covid_dashboard-pkg-jcurry",
    version= "0.0.1",
    author= "Joshua Curry",
    author_email= "jacc202@exeter.ac.uk",
    description= "A dashboard showing coivd-19 infection rates and news articles",
    long_description= long_description,
    long_description_content_type= "text/markdown",
    url= "https://github.com/Joshua-AC-Curry/Covid-19-Dashboard",
    packages= setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires= '>= 3.9'
)