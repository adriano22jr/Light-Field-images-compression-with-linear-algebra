# Data compression algorithms evaluation and comparison with Linear Algebra approaches

## Introduction
> This repository contains software and datasets for a project  developed for the master degree course of Data Compression at [University of Salerno](https://www.unisa.it/).

The primary goal of this project is to perform a comparative analysis between traditional data compression techniques and **Principal Component Analysis** (PCA) and **Singular Value Decomposition** (SVD) applied in the context of LightField Images. All the traditional techniques that will be used for the analysis are already evaluated on the datasets of this repository by previous works made from other master students of the Data Compression course. Our mission is to expand this research field in order to find new and competitive approaches for image compression and see if they can be compared with traditional and well estabilished algorithms.

## Repository Structure
- **datasets**, the datasets folder contains all the data used for the evaluation of the algorithms.
- **src**, the src folder contains all the code written for the project.


## Installation
Step 1: create and install the docker image with the following commands
> docker build -t IMAGE_NAME . <br />
> docker run -d -v "$(pwd):/workspace" IMAGE_NAME <br />
> docker exec -it CONTAINER_ID /bin/bash <br />
> cd workspace

Step 2: create and activate the python virtual environment
> python3 -m venv data_compression <br />
> source data_compression/bin/activate <br />

Step 3: install pip dependencies
> pip3 install -r requirements.txt