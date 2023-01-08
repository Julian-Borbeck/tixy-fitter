# tixy-fitter
Python script to fit sets of polynomials to images to turn the images into tixy compatible functions

## Overview
This repository contains a script written for the course Praktische Informatik 1: Deklarative Programmierung.
The script takes a set of images, rescales them and fits a set of polynomial functions to the image to turn 
each image into a Racket function that is compatible with a Racket implementation of https://tixy.land/

## Issues and Bug Reports

Please open an issue if you find any errors or unexpected behavior. Please make sure to document:

1. What you tried
2. What the result was
3. What you expected the result to be
4. Steps (if any) which you took to resolve the issue and their outcomes.


## Requirements
The following packages are required
- pillow
- numpy
- scipy
- matplotlib (optional, used for visualization)

## Usage

### Input
The script requires a black and white video split into frames.
