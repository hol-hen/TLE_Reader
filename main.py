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
    - satellite ID
    - year launched
    - time of reading (julian date fraction)
    - mean motion (n) in rad/s
    - inclination in radians
    - right ascension of the ascending node (RAAN) in radians
    - eccentricity
    - argument of perigee (w) in radians
    - mean anomaly (M) in radians
    """
    def __init__(self, i, RAAN, e, w, n, M, juliandate, year, sat_id): 
        self.sat_id = sat_id 
        self._year = year 
        self.juliandate = juliandate 
        self.n =  n * 2*pi/86400 
        self.i = i * pi/180 
        self.RAAN = RAAN * pi/180 
        self.e = e 
        self.w = w * pi/180 
        self.M = M * pi/180 
        

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
def readTLE(textfile):
    #open TLE file and read lines
    file = open(textfile, 'r')
    lines = file.readlines() #read lines and store as lines list
    file.close()
    
    #remove any blank spaces and rejoin to get satellite object name
    objectname = " ".join(lines[0][:-1].split())  

    #store TLE as list (exclude name)
    data = lines[1][:-1].split() + lines[2][:-1].split() 
    
    #extract info from the data list - angle units in degrees
    ideg = float(data[11])
    RAANdeg = float(data[12])
    e = float('0.{}'.format(data[13]))
    wdeg = float(data[14])
    ndeg =  float(data[16])
    Mdeg = float(data[15])
    julian_date = float(data[3])
    date_string = datestr(julian_date)
    year = float(data[2][:2])
    sat_id = float(data[10]) 
    
    return objectname, ideg, RAANdeg, e, wdeg, ndeg, Mdeg, julian_date, date_string, year, sat_id


#Function to calculate and return eccentric anomaly using Newton's method
#def kepler_E(e,M): 

#function to create and return information text for object
def text(name, date_string, TLE): 
    text = [
    #General info  
    '------------------------------ {} ------------------------------'.format(name),
    'NORAD ID:                  {:0.0f}'.format(TLE.sat_id),
    'Year Launched:             {}'.format(int(TLE.get_year_launched())),
    'Orbit Type:                {}'.format(TLE.get_orbit_type()),
    
    '\n',
    
    #TLE observation info
    'TLE observation time:      {}'.format(date_string),
    'Altitude at time:          {:0.2f} km'. format(TLE.get_altitude()),
    'Speed at time:             {:0.2f} km/s'. format(TLE.get_speed()),
    
    '\n',
    
    #Orbit info
    'Orbital Period:            {:0.2f} mins'. format(TLE.get_period()/60),
    'Number of orbits per day:  {:0.2f}'. format(TLE.get_orbits_per_day()),
    'Orbit inclination:         {:0.2f} degrees'. format(TLE.i*180/pi),
    'Orbit eccentricity:        {:0.5f}'. format(TLE.e),
    'Orbit RAAN:                {:0.2f} degrees'.format(TLE.RAAN*180/pi),
    'Orbit AOP:                 {:0.2f} degrees'.format(TLE.w*180/pi)]
    return text

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
def main():
    
    #Title and instructions
    print('\n')
    print('- - - - - - - - - - TLE Reader - - - - - - - - - -')
    print("This program analyses the TLE of an object")
    print('\n')

    #Get file name of TLE as input 
    objectfile = input('Enter TLE text file of object: ')   
    
    #read TLE file by calling function READtle()
    name1, ideg1, RAANdeg1, e1, wdeg1, ndeg1, Mdeg1, juliandate1, date_string1, year1, sat_id1 = readTLE(objectfile) 
    
    #instantiate class TLE by using output of readTLE()
    TLE1 = TLE(i = ideg1, RAAN = RAANdeg1, e = e1,
                   w = wdeg1, n = ndeg1, M = Mdeg1,
                   juliandate = juliandate1, year = year1, 
                   sat_id = sat_id1)

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




