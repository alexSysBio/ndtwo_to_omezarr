
"""
Alexandros Papagiannakis, 2025, MIT license
"""

import numpy as np
import zarr

from ome_zarr.io import parse_url
from ome_zarr.format import FormatV04
from ome_zarr.writer import write_image, add_metadata

import matplotlib.pyplot as plt
import os
from skimage.data import binary_blobs

import dask.array as da

from dataclasses import asdict
import os

import ndtwo_to_python as ndtwo
import omezarr_auxiliary as aux # type: ignore



def ndtwo_to_omezarr(source_path, destination_path, time_intercal_sec):

    xr, iter_axis, metadata_dict = ndtwo.nd2_to_array(source_path)
    ndtwo.raise_error_if_zero_dim(xr)

    chunks = aux.get_chunks(xr, start_chunk_ratio=8)
    # chunks = (1,1,1,256,256)
    print(f"Using chunks {chunks} for array of shape {xr.shape}")

    axes = aux.generate_axes(iter_axis)
    print(f"Using axes {axes} for array of shape {xr.shape}")

    store = parse_url(destination_path, mode="w").store
    root = zarr.group(store=store, zarr_format=2)

    xr_da = da.from_array(xr, chunks=chunks)

    write_image(
                image=xr_da,
                group=root,
                axes=axes,
                storage_options={},
                fmt=FormatV04(),
                multiscales=True,   
                compute=True
                )
    

    print(root.tree())  

    root.attrs["multiscales"] = [
        {
            "version": "0.4",
            "name": "image",
            "datasets": [
                {
                    "path": "0",
                    "coordinateTransformations": [
                        {"type": "scale", "scale": aux.get_axis_calibration(metadata_dict, axes, time_intercal_sec)}
                    ]
                }
            ],
            "axes": axes
        }
    ]


    add_metadata(root, aux.get_omero_metadata(metadata_dict))

    print("OME-Zarr written successfully.")



def read_omezarr(path, level=0):

    level_path = f"{path}/{level}"
    arr = zarr.open(level_path, mode='r')

    np_arr = np.array(arr)
    return np_arr




def ndtwo_to_omezarr_per_position(source_path, destination_path, time_interval_sec):
    
    xr, iter_axis, metadata_dict = ndtwo.nd2_to_array(source_path)
    ndtwo.raise_error_if_zero_dim(xr)

    axes = aux.generate_axes(iter_axis)
    print(f"Using axes {axes} for array of shape {xr.shape}")

    store = parse_url(destination_path, mode="w").store
    root = zarr.group(store=store, zarr_format=2)
    # Detect position axis
    n_positions, pos_axis_index = aux.get_number_of_positions(xr, axes)
    print(f"Detected {n_positions} positions at axis index {pos_axis_index}")

    # Iterate over positions
    for p in range(n_positions):
        arr_p = aux.get_position_slice(xr, pos_axis_index, p)
        axes_for_write = [ax for ax in axes if ax['name'] != 'p']  # remove position axis for writing
        # print(axes_for_write)
        chunks = aux.get_chunks(arr_p, start_chunk_ratio=8)
        xr_da = da.from_array(arr_p, chunks=chunks)
        # print(arr_p.shape)

        grp = root.require_group(f"{p}")
        grp.attrs["zarr_format"] = 2

        write_image(
            image=xr_da,
            group=grp,
            axes=axes_for_write,
            storage_options={},
            fmt=FormatV04(),
            multiscales=True,
            compute=True
        )

        # Scaling / multiscales
        grp.attrs["multiscales"] = [
            {
                "version": "0.4",
                "name": f"position_{p}",
                "datasets": [
                    {
                        "path": "0",
                        "coordinateTransformations": [
                            {"type": "scale", "scale": aux.get_axis_calibration(metadata_dict, axes_for_write, time_interval_sec)}
                        ]
                    }
                ],
                "axes": axes_for_write
            }
        ]

        # Metadata
        add_metadata(grp, aux.get_omero_metadata(metadata_dict))
        # grp.attrs["extra_metadata"] = [
        #     {
        #         "channel": ch["channel"]["name"],
        #         "loops": ch.get("loops", {}),
        #         "microscope": ch.get("microscope", {}),
        #         "volume": ch.get("volume", {})
        #     } for ch in metadata_dict["channels"]
        # ]

    print(root.tree())  
    print("OME-Zarr written successfully per position. You can now open it in Napari.")



def read_all_positions_level0(base_path):
    
    positions = sorted([d for d in os.listdir(base_path) if d.isdigit()], key=int)
    arrays = []


    for pos in positions:
        pos_root = os.path.join(base_path, pos)
        grp = zarr.open(pos_root, mode="r")

        try:
            axes = [ax["name"] for ax in grp.attrs["multiscales"][0]["axes"]]
        except Exception as e:
            print(f"Could not read axes metadata for {pos}: {e}")
            axes = None

        level0 = os.path.join(pos_root, "0")
        
        arr = np.array(zarr.open(level0, mode="r"))
        arrays.append(arr)

    axes = ["p"] + axes  
    arrays = np.array(arrays)

    return arrays, axes

