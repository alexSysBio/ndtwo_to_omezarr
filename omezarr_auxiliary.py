"""
Alexandros Papagiannakis, 2025, MIT license
"""



def generate_axes(iteration_axis):
    
    axes = []

    for ia in iteration_axis:
        if ia == 'T':
            axes.append({"name": "t", "type": "time"})
        elif ia == 'P' or ia == 'M' or ia == 'V' or ia == 'S':
            axes.append({"name": "p", "type": "position"})
        elif ia == 'C':
            axes.append({"name": "c", "type": "channel"})
        elif ia == 'Z':
            axes.append({"name": "z", "type": "space"})
        elif ia == 'Y':
            axes.append({"name": "y", "type": "space"})
        elif ia == 'X':           
            axes.append({"name": "x", "type": "space"})
    
    return axes



def get_chunks(image_array, start_chunk_ratio=8):

    chunks = []

    for sh in image_array.shape:
        new_chunk = True
        start_ratio = start_chunk_ratio
        while new_chunk and start_ratio < 10:
            if sh % start_ratio == 0:
                chunk = int(sh / start_ratio)
                new_chunk = False
            else:
                start_ratio -= 1
            # print(sh, start_ratio)
        chunks.append(chunk)

    return tuple(chunks)



def get_omero_metadata(metadata_dict):
    
    # OMERO channels
    omero_channels = []
    for ch in metadata_dict['channels']:
        cmeta = ch["channel"]
        color = cmeta["color"]
        hex_color = (
            color if isinstance(color, str)
            else f"{color.r:02X}{color.g:02X}{color.b:02X}"
        )
        omero_channels.append({
            "label": cmeta["name"],
            "color": hex_color,
            "emissionWavelength": cmeta.get("emissionLambdaNm"),
            "excitationWavelength": cmeta.get("excitationLambdaNm"),
            "active": True
        })
    omero = {
        "channels": omero_channels,
        "rdefs": {"defaultT": 0, "defaultZ": 0}
    }
    
    print(f"adding omero metadata {omero}")

    return {"omero": omero}



def get_axis_calibration(metadata_dict, axes, time_interval_sec):

    axes_cal = metadata_dict['channels'][0]['volume']['axesCalibration']
    axes_cal_bool = metadata_dict['channels'][0]['volume']['axesCalibrated']
    calibration = []

    for ax in axes:
        if ax["name"] == "t":
            calibration.append(time_interval_sec)
        elif ax["name"] == "z":
            calibration.append(axes_cal[2] if axes_cal_bool[2] else 1)
        elif ax["name"] == "y":
            calibration.append(axes_cal[1] if axes_cal_bool[1] else 1)
        elif ax["name"] == "x":
            calibration.append(axes_cal[0] if axes_cal_bool[0] else 1)
        else:
            calibration.append(1)

    print(f"adding calibrations {calibration}")

    return calibration



def get_number_of_positions(image_array, axes):

    try:
        pos_axis_index = [x for x in range(len(axes)) if axes[x]['name'] == 'p'][0]
        n_positions = image_array.shape[pos_axis_index]
    except ValueError:
        pos_axis_index = None
        n_positions = 1
    
    return n_positions, pos_axis_index



def get_position_slice(image_array, pos_axis_index, pos):

    if pos_axis_index is not None:
        slicer = [slice(None)] * image_array.ndim
        # slicer[pos_axis_index] = slice(pos, pos + 1) # This is important to keep the dimension for squeezing later
        slicer[pos_axis_index] = pos # This removes the position from the array
        arr_p = image_array[tuple(slicer)]
    else:
        arr_p = image_array

    return arr_p