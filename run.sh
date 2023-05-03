#!/bin/sh

# As this is gonna run in container, output_dir has to be inside of this project
output_dir='output'

# Run python script to create HTML report
python main.py
if [ ! 0 -eq $? ]
then
    >&2 echo "Some error occured while creating HTML report"
    exit 1
fi
echo "HTML report successfully created"

# Prepare variables
inputhtml=$(ls -t ${output_dir}/*.html | head -1) # finds latest html file
filename_noext="${inputhtml%.*}"
outputpdf="${filename_noext}.pdf"

# Convert to PDF
wkhtmltopdf "${inputhtml}" "${outputpdf}"

# SUCCESS
echo "Report converted to ${outputpdf}"
