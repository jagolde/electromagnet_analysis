import numpy as np
import matplotlib.pyplot as plt


def calc_field_strength(force, constants):
    """
    Function to calculate the magnetic field strength of an electromagnet at a distance along the axis

    Args:
    force (float): The theoretical desired force
    constants (list): Physics and design constants

    Returns:
    float: The theoretical field strength necessary to create the desired magnetic force
    """

    #unpack constants
    area = constants[0]
    permeability = constants[1]

    return np.sqrt((2*force*permeability)/area)

def calc_current(field, constants):
    """
    Function to calculate the theoretical necessary current for the previously calculated field strength

    Args:
    field (float): Field strength required at the point of interaction
    constants (list): Physics and design constants

    Returns:
    float: The necessary current to drive each electromagnet
    """
    #unpack constants
    permeability = constants[1]
    winds = constants[2]
    distance_constant = constants[4]

    return (2*field)/(distance_constant*permeability*winds)


def calc_winds(field, constants):
    """
    Function to calculate the theoretical necessary number of winds for the previously calculated field strength

    Args:
    field (float): Field strength required at the point of interaction
    constants (list): Physics and design constants

    Returns:
    int: The necessary number of winds to drive each electromagnet
    """
    #unpack constants
    permearbility = constants[1]
    current = constants[3]
    distance_constant = constants[4]

    return (2*field)/(distance_constant*permearbility*current)

def back_solve(winds, current):
    # free_space_permeability = 4*np.pi*10**-7
    # air_permeability_modifier = 1.0000037
    # air_permeability = free_space_permeability/air_permeability_modifier

    air_permeability =1.25663753*10**-6

    magnet_area = 0.01


    #model parameters
    permanent_magnet_area = 0.01 #m APPROX
    core_diameter = 0.005 #m
    core_radius = core_diameter/2 #m
    core_length = 0.01 #m APPROX
    distance = 0.001 #total guess
    # distance_constant = np.cos(np.arctan(core_radius/(core_length+distance))) - np.cos(np.arctan(core_radius/distance))
    distance_constant = ((distance+core_length)/np.sqrt((distance+core_length)**2 + (core_radius)**2)) - (distance/np.sqrt(distance**2 + (core_radius)**2))

    field_strength = (air_permeability*winds*current*distance_constant)/2
    force = (field_strength**2 * magnet_area)/(2*air_permeability)

    return [field_strength, force]

current_spacing = np.linspace(0.1,1,10)
field_strength = []
for i in current_spacing:
    field_strength.append(back_solve(100000,i)[1])

plt.plot(current_spacing, field_strength)
plt.title("Force vs Current")
plt.show()

field_strength = back_solve(100000,0.75)
print(field_strength)

core_diameter = 0.005 #m
core_radius = core_diameter/2 #m

core_circumfrence = np.pi * core_diameter

print(core_circumfrence)
wire_length = 1000*core_circumfrence

print(wire_length)



# #from sherry
# force = 6 #N

# #design variables
# number_of_winds = 0
# current = 0.23 #A

# #pysics parameters
# free_space_permeability = 4*np.pi*10**-7
# air_permeability_modifier = 1.0000037
# air_permeability = air_permeability_modifier/free_space_permeability

# #model parameters
# permanent_magnet_area = 0.01 #m APPROX
# core_width = 0.005 #m
# core_length = 0.01 #m APPROX
# distance = 0.001 #total guess
# distance_constant = np.cos(np.tan(core_width/(core_length*distance))) - np.cos(np.tan(core_width/distance))

# #constants = [magnet_area, air_perm, winds, current, distance_constant]
# constants_vector = [permanent_magnet_area, air_permeability, number_of_winds, current, distance_constant]

# field_strength_est = calc_field_strength(force, constants_vector)
# #current_est = calc_current(field_strength_est, constants_vector)
# winds_est = calc_winds(field_strength_est, constants_vector)

# print(winds_est)

# ###add length of wire calculation to figure out equivalent resistance of the wire
