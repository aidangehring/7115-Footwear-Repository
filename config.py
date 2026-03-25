#%%
assets_path= 'assets'
dataframes= {}

SHOES= {
    'Spezial': {
        'name': 'Adidas Spezial',
        'color': "#F8F7F7",  
        'description': 'Flat, minimal drop court shoe'
    },
    'Relentless': {
        'name': 'Nike Relentless',
        'color': '#E3000F',  
        'description': 'Cushioned daily trainer, moderate drop'
    },
    'Pegasus': {
        'name': 'Nike Pegasus',
        'color': "#198D9C",  
        'description': 'Max cushion running shoe, high drop'
    }
}

VARIABLE_LABELS = {
    'angles': 'Joint Angle (°)',
    'moments': 'Joint Moment (Nm/kg)',
    'powers': 'Joint Power (W/kg)',
    'grf': 'Ground Reaction Force (%BW)'
}
 
JOINT_OPTIONS = [
    'Left Ankle', 'Right Ankle',
    'Left Knee',  'Right Knee',
    'Left Hip',   'Right Hip'
]
 
AXIS_OPTIONS = ['X', 'Y', 'Z']
 
VARIABLE_OPTIONS = {
    'angles':  'Angles',
    'moments': 'Moments',
    'powers':  'Powers',
    'grf': 'GRF'
}