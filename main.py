#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wednesday Feb 21 13:47:48 2024

@author: hollywilson
"""

# Packages
from math import pi, cos, sin, tan, sqrt, acos, asin, atan, floor
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# Constants



"""
TLE Class:
This class provides the utility to work with the information from the TLE file as a satellite object.

"""
class TLE:

    """
    Constructor
    - satellite name
    - satellite ID
    - year launched
    - time of reading
    - mean motion
    - inclination
    - right ascension of the ascending node
    - eccentricity
    - argument of perigee
    - mean anomaly
    """
    #def __init__(): 

    """
    Functions
    
    """
    #def compute_year_launched(self): 

    def get_year_launched(self): 
        self.compute_year_launched()
        return self.year_launched
    
    #def compute_period(self):
    
    def get_period(self):
        self.compute_period()
        return self.period
    
    #def compute_a(self):
    
    def get_a(self):
        self.compute_a()
        return self.a
    
    #def compute_altitude(self)

    def get_altitude(self):
        self.compute_altitude()
        return self.altitude
        
    #def compute_orbit_type(self):   

    def get_orbit_type(self):
        self.compute_orbit_type()
        return self.orbit_type
    
    #def compute_orbits_per_day(self):
    
    def get_orbits_per_day(self):
        self.compute_orbits_per_day()
        return self.orbits_per_day
    
    #def compute_speed(self):
    
    def get_speed(self):
        self.compute_speed()
        return self.speed
    
    #def compute_theta(self):
    
    def get_theta(self):
        self.compute_theta()
        return self.theta
    
    #def compute_r(self): 

    def get_r(self):
        self.compute_r()
        return self.r

    #def compute_v(self):
    
    def get_v(self):
        self.compute_v()
        return self.v


"""
Main Functions
    
"""

#Function to convert from julian time to gregorian time and return a string
#def datestr(date_julian): 

#function to read and extract information from the TLE, (many returns)
#def readTLE(textfile):

#Function to calculate and return eccentric anomaly using Newton's method
#def kepler_E(e,M): 

#function to create and return information text for object
#def text(name, date_string, TLE): 

#function to print information on console
#def text_print(name, date_string, TLE):

#function to save information as a text file        
#def save_txt_file(name, date_string, TLE):

#Function to plot the orbit of the satellite and save as a .png file
#def orbit_plot(name, TLE):

    #Define initial values in orbit
    
    #Euler Loop
    
    #Convert into coordinates to be plotted
    
    #Create a figure with 3D axes

    #Create earth on the 3D plot
   
    # Plot orbit of the object

    # save graph as .png file


#Function to ask to save text file and then do so if yes
#def ask_save_graph(name, TLE):

#Function to ask to save text file and then do so if yes
#def ask_save_txt(name, date_string, TLE):

#Function to restart or exit program
#def exit_restart():

#Main script
#def main():
    
    #Title and instructions

    #Get file name of TLE as input    
    
    #read TLE file by calling function READtle()
    
    #instantiate class TLE by using output of readTLE()

    #print information by calling text_print() function
    text_print(name1, date_string1, TLE1) 

    print('\n')

    #ask and save graph by calling ask_save_graph() function
    ask_save_graph(name1, TLE1) 

    print('\n')

    #ask and save text file by ask_save_txt() function
    ask_save_txt(name1, date_string1, TLE1) 

    print('\n')

    #ask to exit or restart by calling exit_restart() function
    exit_restart() 


if __name__ == "__main__":
   main() 




