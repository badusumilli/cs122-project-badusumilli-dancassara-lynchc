#!/bin/bash

# ticker_list = ['VTI', 'VBR', 'VEA', 'VTMGX', 'VWO', 'VSS'
# 'VNQ', 'VNQI', 'BND', 'VBMFX', 'BSV', 'VBISX', 'BNDX', 'VGTSX']

STR="'VTI' 'VBR' 'VEA' 'VTMGX' 'VMO' 'VSS' 'VNQ' 'VNQI' 'BND' 
'VBMFX' 'BSV' 'VBISX' 'BNDX' 'VGTSX'"

for i in $STR; do
	echo $i
	python3 cs122-project-badusumilli-dancassara-lynchc/data.py $i
done