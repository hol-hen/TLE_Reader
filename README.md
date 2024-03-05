# TLE Reader

A basic CLI program that reads satellite TLE .txt files and creates orbit visualisations.

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Import TLE files](#import-tle-files)
* [Exports](#exports)

## General Info
The program converts the standard TLE file format https://en.wikipedia.org/wiki/Two-line_element_set to a more readable and informative format.\
Includes additional info including orbit type, altitude, speed, orbital period, orbits per day, using orbital calculations.\
It can also create a visualisation of the orbit.

![Example Picture](./images/example_2.png)

## Technologies
Project is created with python 3.
Imports the libraries: math, numpy, matplotlib, datetime, calendar, os

## Setup
To run this project, download the TLEreader.py file. Make sure TLE .txt file in the src/inputs folder. \
The python file can then be run in the command line.
The path to the input and output folders are hardcoded as constants, so they can easily be changed to meet your needs.

## Import TLE Files
Takes input txt file of a satellite TLE (can be downloaded from Celestrak https://celestrak.org/NORAD/elements/).\
Two sample TLE files are provided (Aerocube 12A.txt and Intelsat 5.txt), these can be found in the "src/inputs" folder\

## Exports
A visualisation and data can be downloaded as part of the program.\
These will save as a .png file, and .txt file respectivley and will be saved in the outputs folder.\
For an input file called sat.txt, the exports will be saved as sat.png and sat_orbit.txt\
(Note: if the directory was not changed in the program [setup](#setup), the export files will be saved in the default file directory.)