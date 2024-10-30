# Spatial Phenotypes of Puncta

This project analyzes the spatial phenotypes of puncta (peroxisomes) in cells by fitting a log-Gaussian Cox process (LGCP) to point patterns. Predictors related to the endoplasmic reticulum (ER) and mitochondria are included in the model.

## Table of Contents
- [Introduction](#introduction)
- [Spatial Phenotypes Quantified](#spatial-phenotypes-quantified)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Running the Analysis](#running-the-analysis)
  - [1. Preprocessing](#1-preprocessing)
  - [2. Model Fitting](#2-model-fitting)
- [Dataset](#dataset)
- [Results](#results)

## Introduction

This project aims to make spatial modeling in biology more accessible by providing step-by-step notebooks on analyzing point patterns of peroxisomes within cells. By incorporating predictors related to the ER and mitochondria, we can quantify specific spatial phenotypes.

## Spatial Phenotypes Quantified

Our LGCP model quantifies the following spatial phenotypes of peroxisomes:

- **Perinuclear Localization**: Likelihood of peroxisomes being found in the perinuclear region.
- **Proximity to Mitochondria**: Likelihood of peroxisomes being within 1 micrometer of mitochondria.
- **Overlap with ER**: Likelihood of peroxisomes overlapping with the ER.
- **Hidden Structured Effects**: Detection of underlying spatial structures affecting peroxisome distribution.

## Project Structure

- **`data/raw/`**: Contains the raw images used for analysis.
- **`data/processed/`**: Stores processed data outputs from the preprocessing notebook.
- **`data/output/`**: Stores the results from the inference of the model.
- **`notebooks/`**:
  - **`preprocessing.ipynb`**: Jupyter notebook for data preprocessing.
  - **`analysis_inlabru.Rmd`**: R Markdown notebook for model fitting with the inlabru package.
  - **`make_figures.ipynb`**: Jupyter notebook, to make nice figures of the data and infernence results
- **`docs/`**: includes html files of the notebooks which are more convinient to read the steps of the analysis
- **`figures/`**: some figures of the dataset and the results of the analysis

## Prerequisites

To run the notebooks as they are you will need:

- **Python** with Jupyter Notebook for preprocessing.
  - the packages: PIL, geopandas, shapely, rasterio, numpy, scipy, cv2, skimage, matplotlib.pyplot, and itertools

the preprocessing and can be done also differently and with other packages, it is imortant however that the output from the preprocessign is readable/compatible with the packages in R

- **R** with RStudio for model fitting.
  - the packages: INLA, inlabru, sf, fmesher, ggplot2, terra

## Running the Analysis

The main files to run the analsysis are preprocessing.ipynb and analysis_inlabru.Rmd. 

  1. Preprocessing:
    In this notebook we pinpoint the locations of peroxisomes from the fluoresence image, and we construct the predictive maps that depends on images of the nucleus, the ER and mitochondria. Last we stitch together the data from all the cells in a single spatial frame and we export them in a format compatible with the analysis that follows.
  2. Model Fitting:
    We fit a log gaussian cox process model through the inlabru package using the output of the preprocessing step. The steps of fitting invovle making a mesh of the spatial domain, constructing the model (how the mean density depends on the components) and finaly fitting with inlabru.

## Dataset

At pannel A you can see fluoresence images of some of the channels, at pannel B the constructed maps used for the model and at pannel C is the dataset used in the model

![Data](figures/data.png)

## Results

Pannel A we present the marginal posterior distributions of the parameters of the model, and at pannels B and C gaussian random field and mena density that the model predicts.

![Results](figures/results.png)