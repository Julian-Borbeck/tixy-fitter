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
This script generates a .rkt file that can be imported into other racket projects using require, aswell as an optional preview

### Input
The script requires a black and white video split into frames. 

### Parameters

directory_in (string): Input directory
directory_out (string): Ouptut directory
rkt_out (string): Filename of Racket file to generate

func_name (string): Function name of the Racket function to generate (Signature t i x y )
n_images (integer): Number of Images in the Input directory, needed for the modulo operator to repeat the animation
tixy_size (integer): Size of the Tixy Grid 
render (boolean): if True, a preview of the process is rendered to the output dir for each image
maxfev_ (integer): number of iterations to fit for each function

