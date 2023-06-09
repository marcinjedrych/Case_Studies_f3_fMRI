This folder contains all code needed to reproduce our SPM analysis on the dataset. All analyses were done in MATLAB version R2023a using the SPM12 package (https://www.fil.ion.ucl.ac.uk/spm/software/download/).

First, we did some additional preprocessing on the original fmriprep data. We were not able to upload the preprocessed data because data files were too large. However, one can reproduce the preprocessing analyses using the following codes in the right order:
1) Coregister
2) Segment
3) Normalize

Secondly, we performed a first level analysis using the code in the 'First Level Analysis' folder. To run this analysis, you first have to run the code 'OnsetFileAll' to create timing files for each movement condition separately (based on the event files). The contrasts that were created using this first level analysis are uploaded in the subfolder 'Results' within the 'First Level Analysis' folder. Also the timing files can be found in the subfolder 'OnsetFiles' together with the original event files.

Lastly, we did a second level analysis using the code in the 'Second Level Analysis' folder. To create the final results of the second level analysis, one should click on the 'results' button in SPM and select the SPM file and contrast that was created using the 'Second Level Analysis' code. Also here, results of this analysis are uploaded in the subfolder 'Results' in the 'Second Level Analysis' folder.

The results of the second level analysis were visualized using the MRIcroGL tool which can be downloaded here: https://www.nitrc.org/projects/mricrogl.
