# Parameter sets for the max250 model, PRJ-175.
# Each dict is one configuration to feed into models.max250.build_max250().

one = {'holdback': -15400,
        'rotation_max_torque': 0,
        'mast_angle': -90,
        'feed_position': 196.8,
        'mast_slide_position': 0,
        'head_weight': 1623,
        'head_pos': (-26.0377, 6.9107, 0.5275),
        'mast_weight': 3087,
        'mast_pos': (-86.93, 9.52, -4.97), #approximated 20 inch further than the 3m mast
        'pivot_weight': 570,
        }

two = {'holdback': -15400,
        'rotation_max_torque': 0,
        'mast_angle': -45,
        'feed_position': 196.8,
        'mast_slide_position': 0,
        'head_weight': 1623,
        'head_pos': (-26.0377, 6.9107, 0.5275),
        'mast_weight': 3087,
        'mast_pos': (-106.93, 9.52, -4.97), #approximated 20 inch further than the 3m mast
        'pivot_weight': 570,
        }

# test the 3m to confirm with sldworks
three = {'holdback': -0,
        'rotation_max_torque': 0,
        'mast_angle': -12,
        # 'feed_position': 196.8, # 4m rods
        'feed_position': 157.42, # 3m rods
        'mast_slide_position': 0,
        'head_weight': 1623,
        'head_pos': (-26.0377, 6.9107, 0.5275),
        'mast_weight': 3757.73,
        'mast_pos': (-108.1419, 9.37, -5.6096),
        'pivot_weight': 570,
        }

cases = [one, two, three]
