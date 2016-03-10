#!/bin/bash

# ticker_list = ['VTI', 'VBR', 'VEA', 'VTMGX', 'VWO', 'VSS'
# 'VNQ', 'VNQI', 'BND', 'VBMFX', 'BSV', 'VBISX', 'BNDX', 'VGTSX']

# STR="'VTI' 'VBR' 'VEA' 'VTMGX' 'VWO' 'VSS' 'VNQ' 'VNQI' 'BND' 
# 'VBMFX' 'BSV' 'VBISX' 'BNDX' 'VGTSX'"

STR="VTI VBR VEA VTMGX VWO VSS VNQ VNQI BND VBMFX BSV VBISX BNDX VGTSX"

cd cs122-project-badusumilli-dancassara-lynchc

for i in $STR; do
	echo $i
	python3 data.py $i
done