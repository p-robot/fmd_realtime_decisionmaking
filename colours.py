"""
Default colours

"""


colour_line = '#2b2b2b'
colour_faint_line = '#cccccc'

text_props = {'size': 14, 'weight': 'normal'}


alpha_country = 0.4

colour_dict_country = {
    "japan" : {"chex": "#e31a1c", "crgba": [0.89, 0.102, 0.11, alpha_country]}, 
    "uk": {"chex": "#1f78b4", "crgba": [0.122, 0.471, 0.706, alpha_country]}
}


alpha_control = 0.8

colour_dict_controls = {
    "ip": {'chex':'#D3D3D3', 'crgba': [0.827,0.827,0.827, alpha_control]},
    "ipdc": {'chex': '#363636', "crgba": [0.212, 0.212, 0.212, alpha_control]},
    "ipdccp": {'chex': '#984ea3', "crgba": [152./255,78./255,163./255, alpha_control]},
    'rc3': {'chex': '#33a02c', "crgba": [0.20, 0.627, 0.173, alpha_control]},
    'rc10': {'chex': '#1f78b4', 'crgba': [0.122, 0.471, 0.706, alpha_control]},
    "v3": {'chex': '#fb9a99', 'crgba': [0.984, 0.604, 0.60, alpha_control]},
    "v10": {'chex': '#e31a1c', 'crgba': [0.89, 0.102, 0.11, alpha_control]}
}

# Collapse the nested dict down to a dictionary mapping control to a colour in hex
colour_dict_controls_hex = dict([(k, v['chex']) for k, v in colour_dict_controls.items()])
