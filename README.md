## Digital Logic Circuits Analyzer Server

A modern web application based on deep learning and advanced image processing techniques to analyze images of logic circuits and simulate their truth table.


#### Tech Stack

| Tool               | Use                                           |
|--------------------|-----------------------------------------------|
| NodeJs and Express | REST API                                      |
| Python             | Image Processing and Truth Table Calculations |


This is the backend of the [Digital Logic Circuits Analyzer](https://github.com/ahmedkrmn/Digital-Logic-Circuits-Analyzer) application. The main server is based on Nodejs and Express. They provide a REST API interface for interacting with the Python scripts on the server which do the actual computation and analysis.

<p align="center"> <img src="api_diagram.png"/> </p>

The backend is hosted on a Heroku server with the following build environemts:
1. Apt
2. Python
3. NodeJs

*The **Apt** buildpack is used to allow the installation of linux libraries using `apt install` on the server. OpenCV requires some Linux libraries that must be installed manually.*

The code on this repo is **deployment-ready**, all you need is to enable the buildpacks on Heroku and all the required Linux libraries, Python Pip packages, and Node npm modules will be installed from the configuration files on the repo.
