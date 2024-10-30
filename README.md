# Spatial Phenotypes of Puncta

This project analyzes the spatial phenotypes of puncta (peroxisomes) in cells by fitting a log-Gaussian Cox process (LGCP) to point patterns. Predictors related to the endoplasmic reticulum (ER) and mitochondria are included in the model.

## Table of Contents
- [Introduction](#introduction)
- [Spatial Phenotypes Quantified](#spatial-phenotypes-quantified)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Analysis](#running-the-analysis)
  - [1. Preprocessing](#1-preprocessing)
  - [2. Model Fitting](#2-model-fitting)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

This project aims to make spatial modeling in biology more accessible by providing step-by-step tutorials on analyzing point patterns of peroxisomes within cells. By incorporating predictors related to the ER and mitochondria, we can quantify specific spatial phenotypes.

## Spatial Phenotypes Quantified

Our LGCP model quantifies the following spatial phenotypes of peroxisomes:

- **Perinuclear Localization**: Likelihood of peroxisomes being found in the perinuclear region.
- **Proximity to Mitochondria**: Likelihood of peroxisomes being within 1 micrometer of mitochondria.
- **Overlap with ER**: Likelihood of peroxisomes overlapping with the ER.
- **Hidden Structured Effects**: Detection of underlying spatial structures affecting peroxisome distribution.

## Project Structure

- **`data/raw/`**: Contains the raw images used for analysis.
- **`data/processed/`**: Stores processed data outputs from the preprocessing notebook.
- **`notebooks/`**:
  - **`preprocess.ipynb`**: Jupyter notebook for data preprocessing.
  - **`analysis.Rmd`**: R Markdown notebook for model fitting and analysis.

## Getting Started

### Prerequisites

- **Python 3.x** with Jupyter Notebook for preprocessing.
- **R** with RStudio for model fitting.
- Necessary Python and R packages (listed below).

