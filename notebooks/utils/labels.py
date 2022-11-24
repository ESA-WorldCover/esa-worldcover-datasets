import enum

import numpy as np


class LabelsColors(enum.Enum):

    # 10,0,100,0,255,Trees covered area
    # 20,255,187,34,255,Shrub covered area
    # 30,255,255,76,255,Grassland
    # 40,240,150,255,255,Cropland
    # 50,250,0,0,255,Built-up
    # 60,180,180,180,255,Bare areas
    # 70,240,240,240,255,Snow and/or ice cover
    # 80,0,100,200,255,Permament water bodies
    # 90,0,150,160,255,Herbaceous wetland
    # 95,0,207,117,255,Mangroves
    # 100,250,230,160,255,Lichens and mosses

    NO_DATA = (0, 'nodata', 'Not sure', 'No Data', np.array([0, 0, 0]))
    TREE = (10, 'tree', 'tree', 'Trees covered area',
            np.array([0, 100, 0]) / 255)
    SHRUB = (20, 'shrub', 'shrub', 'Shrub cover area',
             np.array([255, 187, 34]) / 255)
    GRASS = (30, 'grass', 'grassland', 'Grassland',
             np.array([255, 255, 76]) / 255)
    CROP = (40, 'crop', 'crops', 'Cropland', np.array([240, 150, 255]) / 255)
    BUILT = (50, 'built', 'urban/built-up',
             'Built-up', np.array([250, 0, 0]) / 255)
    BARE = (60, 'bare', 'bare', 'Bare areas', np.array([180, 180, 180]) / 255)
    SNOW_AND_ICE = (70, 'snow', 'snow and ice', 'Snow and/or ice cover',
                    np.array([240, 240, 240]) / 255)
    WATER = (80, 'water', 'water', 'Permanent water',
             np.array([0, 100, 200]) / 255)
    WETLAND = (90, 'wetland', 'wetland (herbaceous)', 'Herbaceous wetland',
               np.array([0, 150, 160]) / 255)
    MANGROVES = (95, 'mangroves', None, 'Mangroves',
                 np.array([0, 207, 117]) / 255)
    LICHENS = (100, 'lichens_mosses', 'Lichen and moss', 'Lichen and moss',
               np.array([250, 230, 160]) / 255)

    def __init__(self, val1, val2, val3, val4, val5):
        self.id = val1
        self.class_name = val2
        self.iiasa_name = val3
        self.esa_class_name = val4
        self.color = val5


def label_to_rgb(lc_pred, colors_enum=None):

    colors_enum = LabelsColors if colors_enum is None else colors_enum

    colors = {lc.id: {'name': lc.class_name,
                      'color': lc.color}
              for lc in colors_enum}

    rgb_pred = np.zeros((lc_pred.shape[0],
                         lc_pred.shape[1],
                         3))

    for k, v in colors.items():
        for ch in range(3):
            im = rgb_pred[:, :, ch]
            im[lc_pred == k] = v['color'][ch]

    return rgb_pred

colors = {lc.id: {'name': lc.class_name,
                  'color': lc.color}
          for lc in LabelsColors}

legend_dict = {lc.id: lc.esa_class_name
               for lc in LabelsColors}
