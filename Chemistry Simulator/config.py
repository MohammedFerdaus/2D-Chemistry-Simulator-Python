# Display information
width = 1100
height = 700
sim_width_px = 900
fps = 60
background_color = (15, 15, 20)
simulation_background_color = (20, 20, 30)
panel_background_color = (28, 28, 38)

# Simulation units
simulation_width = 90
simulation_height = 70
scale = 10

# Integration units
dt = 0.008
bond_check_interval = 5
molecule_check_interval = 30

# Thermostat units
gamma = 0.7
temperature = 1.05

# LJ potential units
epsilon = 2
lj_cutoff_factor = 2.5
force_cap = 1000

# Element data
elements = {
    'H':  {'mass': 1.0,  'max_bonds': 1, 'color': (220, 220, 230), 'sigma': 1.8,  'radius_pixel': 18},
    'O':  {'mass': 16.0, 'max_bonds': 2, 'color': (220, 60, 60),   'sigma': 2.5,  'radius_pixel': 25},
    'N':  {'mass': 14.0, 'max_bonds': 3, 'color': (80, 130, 220),  'sigma': 2.5,  'radius_pixel': 25},
    'He': {'mass': 4.0,  'max_bonds': 0, 'color': (160, 230, 160), 'sigma': 2.0,  'radius_pixel': 20},
}

# Bonding information
bonding_form_factor = 1.5  # r_form = factor * sigma_ij
bonding_break_factor = 2.5  # r_break = factor * r0
spring_k = 25
dissipation = 0.85

bond_lengths = {
    frozenset({'H', 'H'}): 3.6,  
    frozenset({'H', 'O'}): 4.3, 
    frozenset({'H', 'N'}): 4.3,   
    frozenset({'O', 'O'}): 5.0,  
    frozenset({'N', 'N'}): 5.0,
    frozenset({'N', 'O'}): 5.0,
}

bond_orders = {            # for double/triple line rendering
    frozenset({'O', 'O'}): 2,
    frozenset({'N', 'N'}): 3,
    frozenset({'N', 'O'}): 2,
}

# Drag information
velocity_scale = 0.05    # drag pixel distance * this = initial sim velocity

# Molecules information
known_molecules = {
    # H and O
    frozenset({('H', 2)}): 'H₂',
    frozenset({('O', 2)}): 'O₂',
    frozenset({('H', 2), ('O', 1)}): 'H₂O',
    frozenset({('H', 2), ('O', 2)}): 'H₂O₂',
    frozenset({('H', 1), ('O', 1)}): 'OH·',
    frozenset({('H', 1), ('O', 2)}): 'HO₂·',

    # H and N
    frozenset({('N', 2)}): 'N₂',
    frozenset({('H', 3), ('N', 1)}): 'NH₃',
    frozenset({('H', 4), ('N', 2)}): 'N₂H₄',
    frozenset({('H', 2), ('N', 1)}): 'NH₂·',

    # N and O
    frozenset({('N', 1), ('O', 1)}): 'NO·',
    frozenset({('N', 1), ('O', 2)}): 'NO₂·',
    frozenset({('N', 2), ('O', 1)}): 'N₂O',
    frozenset({('N', 2), ('O', 3)}): 'N₂O₃',

    # H, N and O
    frozenset({('H', 1), ('N', 1), ('O', 3)}): 'HNO₃',
    frozenset({('H', 1), ('N', 1), ('O', 2)}): 'HNO₂',
    frozenset({('H', 3), ('N', 1), ('O', 1)}): 'NH₂OH',
    frozenset({('H', 1), ('N', 1), ('O', 1)}): 'HNO',
}

# Bond angles
bond_angles = {
    'O': 104.5,
    'N': 107,
    'H': 180
}

# Angle spring
angle_spring_k = 80
