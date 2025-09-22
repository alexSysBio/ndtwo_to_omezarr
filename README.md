# ome-zarr functions :microscope: &rarr; :computer:

Alexandros Papagiannakis, Stanford University, 2025

This repository includes functions that can be used to convert, store and read .nd2 microscopy multichannel files into OME-Zarr. Two examples are provided in the <code> apply_omezarr_to_python_github.ipynb </code> notebook with different iteration axes. The Napari viewer is also applied for specific XY positions. 


### Example 1: {'T': 65, 'C': 2, 'Y': 512, 'X': 512} ### 

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">/</span>
├── <span style="font-weight: bold">0</span> (65, 2, 512, 512) uint16
├── <span style="font-weight: bold">1</span> (65, 2, 256, 256) uint16
├── <span style="font-weight: bold">2</span> (65, 2, 128, 128) uint16
├── <span style="font-weight: bold">3</span> (65, 2, 64, 64) uint16
└── <span style="font-weight: bold">4</span> (65, 2, 32, 32) uint16
</pre>

### Example 2: {'T': 49, 'P': 5, 'C': 2, 'Y': 2048, 'X': 2048} ###

<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-weight: bold">/</span>
├── <span style="font-weight: bold">0</span>
│   ├── <span style="font-weight: bold">0</span> (49, 2, 2048, 2048) uint16
│   ├── <span style="font-weight: bold">1</span> (49, 2, 1024, 1024) uint16
│   ├── <span style="font-weight: bold">2</span> (49, 2, 512, 512) uint16
│   ├── <span style="font-weight: bold">3</span> (49, 2, 256, 256) uint16
│   └── <span style="font-weight: bold">4</span> (49, 2, 128, 128) uint16
├── <span style="font-weight: bold">1</span>
│   ├── <span style="font-weight: bold">0</span> (49, 2, 2048, 2048) uint16
│   ├── <span style="font-weight: bold">1</span> (49, 2, 1024, 1024) uint16
│   ├── <span style="font-weight: bold">2</span> (49, 2, 512, 512) uint16
│   ├── <span style="font-weight: bold">3</span> (49, 2, 256, 256) uint16
│   └── <span style="font-weight: bold">4</span> (49, 2, 128, 128) uint16
├── <span style="font-weight: bold">2</span>
│   ├── <span style="font-weight: bold">0</span> (49, 2, 2048, 2048) uint16
│   ├── <span style="font-weight: bold">1</span> (49, 2, 1024, 1024) uint16
│   ├── <span style="font-weight: bold">2</span> (49, 2, 512, 512) uint16
│   ├── <span style="font-weight: bold">3</span> (49, 2, 256, 256) uint16
│   └── <span style="font-weight: bold">4</span> (49, 2, 128, 128) uint16
├── <span style="font-weight: bold">3</span>
│   ├── <span style="font-weight: bold">0</span> (49, 2, 2048, 2048) uint16
│   ├── <span style="font-weight: bold">1</span> (49, 2, 1024, 1024) uint16
│   ├── <span style="font-weight: bold">2</span> (49, 2, 512, 512) uint16
│   ├── <span style="font-weight: bold">3</span> (49, 2, 256, 256) uint16
│   └── <span style="font-weight: bold">4</span> (49, 2, 128, 128) uint16
└── <span style="font-weight: bold">4</span>
    ├── <span style="font-weight: bold">0</span> (49, 2, 2048, 2048) uint16
    ├── <span style="font-weight: bold">1</span> (49, 2, 1024, 1024) uint16
    ├── <span style="font-weight: bold">2</span> (49, 2, 512, 512) uint16
    ├── <span style="font-weight: bold">3</span> (49, 2, 256, 256) uint16
    └── <span style="font-weight: bold">4</span> (49, 2, 128, 128) uint16
</pre>
