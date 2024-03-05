#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wednesday Feb 21 13:47:48 2024

@author: hollywilson
"""

# Packages
import datetime
import calendar
from math import pi, cos, sin, tan, sqrt, acos, asin, atan, floor
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os


# Constants
G = 6.67408e-11   #Universal gravitational constant
mu = 3.986004418e14 #Earth gravitational constant with m^3
mu2 = 3.986004418e5 #Earth grav constant with km^3
re = 6378.1370 #Earth radius km
m_earth = 5.972e24  #Mass of Earth


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
    def compute_year_launched(self): 
        
        #add 1900 for years in 1900s (no launches before 1961)
        if self._year > 60:
            self.year_launched = self._year + 1900
        
        #add 2000 for years in 2000s
        elif self._year <= 60:
            self.year_launched = self._year + 2000 

    def get_year_launched(self): 
        self.compute_year_launched()
        return self.year_launched
    
    #calculate orbital period in seconds
    def compute_period(self):
        self.period = 2*pi/self.n 
    
    def get_period(self):
        self.compute_period()
        return self.period
    
    #calculate semi major axis in km
    def compute_a(self):
        self.compute_period()
        self.a = (self.period**2 * mu / (4 * pi**2) )**(1/3)/1000 
    
    def get_a(self):
        self.compute_a()
        return self.a
    
    def compute_altitude(self):
        self.compute_a()
        self.altitude = self.a - re 

    def get_altitude(self):
        self.compute_altitude()
        return self.altitude
        
    def compute_orbit_type(self):
        self.compute_altitude()

        #label orbit type depending on altitude
        if self.altitude < 2000:
            self.orbit_type = 'LEO (Low Earth Orbit)' 
        elif self.altitude >= 2000 and self.altitude < 35700:
            self.orbit_type = 'MEO (Medium Earth Orbit)'
        elif self.altitude >= 35700 and self.altitude <= 35820:
            self.orbit_type = 'GEO (Geostationary Orbit)'
        elif self.altitude < 35820:
            self.orbit_type = 'HEO (High Earth Orbit)'  

    def get_orbit_type(self):
        self.compute_orbit_type()
        return self.orbit_type
    
    def compute_orbits_per_day(self):
        self.compute_period()
        self.orbits_per_day = 24*60*60/self.period
    
    def get_orbits_per_day(self):
        self.compute_orbits_per_day()
        return self.orbits_per_day
    
    def compute_speed(self):
        self.compute_a()
        self.speed = sqrt(G*m_earth/(self.a*1000))/1000
    
    def get_speed(self):
        self.compute_speed()
        return self.speed
    
    def compute_theta(self):
        self.E = kepler_E(self.e, self.M)
        self.theta = acos( (cos(self.E) - self.e) / (1 - self.e*cos(self.E)) )
    
    def get_theta(self):
        self.compute_theta()
        return self.theta
    
    def compute_r(self):
        self.compute_a()
        self.compute_theta()
        
        self.r_0 = self.a*(1-self.e**2)/(1+self.e*cos(self.theta)) #calculate position at time of TLE

        #calculate x,y,z components
        self.x = (cos(self.RAAN) * cos(self.w) - sin(self.RAAN) * sin(self.w) * cos(self.i)) * self.r_0 * cos(self.theta) + (-cos(self.RAAN) * sin(self.w) - sin(self.RAAN) * cos(self.w) * cos(self.i)) * self.r_0 * sin(self.theta)
        self.y = (sin(self.RAAN) * cos(self.w) + cos(self.RAAN) * sin(self.w) * cos(self.i)) *self. r_0 * cos(self.theta) + (-sin(self.RAAN) * sin(self.w) + cos(self.RAAN) * cos(self.w) * cos(self.i)) * self.r_0 * sin(self.theta)
        self.z = (sin(self.w) * sin(self.i)) * self.r_0 * cos(self.theta) + (cos(self.w) * sin(self.i)) * self.r_0 * sin(self.theta)
        
        #store as position vector
        self.r = np.array([self.x *1000,self.y*1000,self.z*1000]) 

    def get_r(self):
        self.compute_r()
        return self.r

    def compute_v(self):
        self.compute_a()
        self.compute_theta()

        #calculate x,y,z components of velocity
        self.vx = (cos(self.RAAN) * cos(self.w) - sin(self.RAAN) * sin(self.w) * cos(self.i)) * (-(mu2/(self.a*(1-self.e **2)))**(1/2) * sin(self.theta)) + (-cos(self.RAAN) * sin(self.w) - sin(self.RAAN) * cos(self.w) * cos(self.i)) * (mu2/(self.a*(1-self.e **2)))**(1/2) * (self.e + cos(self.theta))
        self.vy = (sin(self.RAAN) * cos(self.w) + cos(self.RAAN) * sin(self.w) * cos(self.i)) * (-(mu2/(self.a*(1-self.e **2)))**(1/2) * sin(self.theta)) + (-sin(self.RAAN) * sin(self.w) + cos(self.RAAN) * cos(self.w) * cos(self.i)) * (mu2/(self.a*(1-self.e **2)))**(1/2) * (self.e + cos(self.theta))
        self.vz = (sin(self.w) * sin(self.i)) * (-(mu2/(self.a*(1-self.e **2)))**(1/2) * sin(self.theta)) + (cos(self.w) * sin(self.i)) * (mu2/(self.a*(1-self.e **2)))**(1/2) * (self.e + cos(self.theta))
        
        #store as velocity vector
        self.v = np.array([self.vx*1000,self.vy*1000,self.vz*1000]) 
    
    def get_v(self):
        self.compute_v()
        return self.v


"""
Main Functions
    
"""

#Function to convert from julian time to gregorian time and return a string
def datestr(date_julian): 

    #convert date to gregorian format (YYYY-MM-DD)
    date = datetime.datetime.strptime(str(floor(date_julian)), '%y%j').date() 
    date = str(date).split('-') 
    month = calendar.month_name[int(date[1])]

    #convert decimal format to hour, mins and secs                              
    UTCtime = float(str(date_julian)[5:]) 
    UTChour = '{0}'.format(str(floor(UTCtime*24)).zfill(2)) 
    UTCminutes = '{0}'.format(str(floor(UTCtime*1440 % 24)).zfill(2)) 
    UTCsecond = '{0}'.format(str(round(UTCtime*86400 %60)).zfill(2)) 

    # save and return string   
    date_string = '{}:{}:{} UTC {} {} {}'.format(UTChour, UTCminutes, UTCsecond, date[2], month, date[0]) 
    return date_string

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
def kepler_E(e,M): 
    step_size = 1e-8 #integration step
    if M < pi:#check which quadrant Mean anomaly in (because it is an angle)
        E = M + e/2
    else:
        E = M - e/2
    
    ratio = 1

    #find convergence point = eccentric anomaly
    while abs(ratio) > step_size:
            ratio = (E - e*sin(E) - M)/(1 - e*cos(E))
            E = E - ratio
    return E

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
def text_print(name, date_string, TLE):
    #call text() function to get required text
    a = text(name, date_string, TLE)  
    
    #print info on console
    print('\n') 
    for i in a:
        print(i) 

#function to save information as a text file        
def save_txt_file(name, date_string, TLE):
    a = text(name, date_string, TLE) 
    
     #open file
    f = open('{}_orbit.txt'.format(name), 'w')
    
    #write each on a new line
    for i in a:
        f.write(i)
        f.write('\n')

    #close file    
    f.close() 

def orbit_plot(name, TLE):

    # define initial values in orbit
    r_0 = TLE.get_r()
    v_0 = TLE.get_v()
    t_0 = 0
    t_n = TLE.get_period()
    dt = t_n / 100000 #integration step 
    r = r_0.copy()
    v = v_0.copy()
    t = t_0
    orbit = [r.copy()]
    vel = [v.copy()]
    times = [t]
    
    #Euler Loop
    while t < t_n:
        #calculate change in r and v vectors for each integration step
        r3 = sum((-r)**2)**1.5
        r = r + dt * v
        v = v - dt * G * m_earth * (r) / r3
        t = t + dt
        #append orbit lists for plotting
        orbit.append(r.copy())
        vel.append(v.copy())
        times.append(t)
    
    #Convert into coordinates to be plotted
    x,y,z = np.asarray(orbit).T
    
    #Create a figure with 3D axes
    fig = plt.figure(1)
    ax = plt.axes(projection='3d') #create 3d plot

    #define surface of Earth
    theta1 = np.linspace(0, 2*pi, 100)
    theta2 = np.linspace(0, pi, 100)
    x_s = re * np.outer(np.cos(theta1), np.sin(theta2))
    y_s = re * np.outer(np.sin(theta1), np.sin(theta2))
    z_s = re * np.outer(np.ones(np.size(theta1)), np.cos(theta2))
       
    #plot surface of Earth
    ax.plot_wireframe(x_s, y_s, z_s, color='#23395d', alpha = 0.2) #changed transparency of wireframe Earth because matplotlib does not integrate well with the plotted lines and would not be able to see orbit at all otherwise.
    
    # Plot body 2 orbit
    ax.plot3D(x/1000,y/1000,z/1000, 'r'); #plotting in km 
    ax.scatter(r[0]/1000,r[1]/1000,r[2]/1000, c='r', marker='o'); #mark satellite point at TLE
    ax.text2D(0.05, 0.93, "Orbit of {}".format(name) , fontsize = 14, transform=ax.transAxes) #title

    #create axis limits, to ensure scale is right for all orbits
    ax.set_xlim3d(-TLE.get_a(), TLE.get_a()) #define in terms of apogee (furthest point form earth) to make all sats fit
    ax.set_ylim3d(-TLE.get_a(), TLE.get_a())
    ax.set_zlim3d(-TLE.get_a(), TLE.get_a())

    #add x, y, z to axis labels for orientation
    ax.set_xlabel("x", fontsize = 12)
    ax.set_ylabel("y", fontsize = 12)
    ax.set_zlabel("z", fontsize = 12)

    #remove axis numbers (takes away from the visualisation)
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])

    #save graph as .png file
    plt.savefig('{}_orbit.png'.format(name))

#Function to ask to save text file and then do so if yes
def ask_save_graph(name, TLE):
    graph = 0
    while graph not in ("Y", "y", "N", 'n'):
        graph = input('Do you want to get a visualisation of the orbit? (Y/N): ') #ask for user response

    if graph == 'Y' or graph == 'y': #if yes call function orbit_plot() to run plot sequence
        orbit_plot(name, TLE)
        print('Your graph has been saved as {}_orbit.png'.format(name)) #tell user what it has been saved as



#Function to ask to save text file and then do so if yes
def ask_save_txt(name, date_string, TLE):
    text = 0
    while text not in ("Y", "y", "N", 'n'):
        text = input('Do you want to save the data of the orbit as text file? (Y/N): ') 

    if text == 'Y' or text == 'y':
            save_txt_file(name, date_string, TLE) 
            print('Your file has been saved as {}_orbit.txt'.format(name)) 


#Function to restart or exit program
def exit_restart():
    run_exit = 0
    
    #ask for user response
    while run_exit not in('', 's', 'S'):
        run_exit = input('- - - - - Press enter to exit or S to start again- - - - -') 
               
    if run_exit == '':
        os._exit(os.EX_OK) 
    elif run_exit == 'S' or 's':
        main()  


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




