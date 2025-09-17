

"""
Alexandros Papagiannakis, 2025, MIT license
"""

from napari import Viewer

def view_xy_position(destination_path, xy_position):
    viewer = Viewer()
    # Pick position 3
    p_group =  destination_path+'/'+str(xy_position)
    viewer.open(str(p_group), plugin="napari-ome-zarr")
