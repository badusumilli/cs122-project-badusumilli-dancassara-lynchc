#!/bin/bash

# ticker_list = ['VTI', 'VBR', 'VEA', 'VTMGX', 'VWO', 'VSS'
# 'VNQ', 'VNQI', 'BND', 'VBMFX', 'BSV', 'VBISX', 'BNDX', 'VGTSX']

# STR="'VTI' 'VBR' 'VEA' 'VTMGX' 'VWO' 'VSS' 'VNQ' 'VNQI' 'BND' 
# 'VBMFX' 'BSV' 'VBISX' 'BNDX' 'VGTSX'"

STR="VTI VBR VEA VTMGX VWO VSS VNQ VNQI BND VBMFX BSV VBISX BNDX VGTSX"

cd cs122-project-badusumilli-dancassara-lynchc/robo_ui/quiz

for i in $STR; do
	python3 get_data.py $i
done

python3 data.py

echo finish
