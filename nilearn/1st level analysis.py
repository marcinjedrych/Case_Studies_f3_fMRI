# -*- coding: utf-8 -*-
"""
Created on Sat May 27 15:26:16 2023

First level analysis

@author: Marcin
"""

import nilearn
import nibabel as nib
import pandas as pd
import numpy as np
from nilearn import plotting
from nilearn import datasets, surface
from nilearn.glm.first_level import make_first_level_design_matrix, run_glm

# Load fMRI data
#fmri_img = nib.load("C:/Users/Marcin/ds004044-download/derivatives/fmriprep/sub-01/sub-01_ses-1_task-motor_run-1_space-T1w_desc-preproc_bold_denoised.nii.gz")
fmri_img = nib.load("C:/Users/Marcin/ds004044-download/sub-01/ses-1/func/sub-01_ses-1_task-motor_run-01_bold.nii.gz")
print('fmri data shape:', np.shape(fmri_img))
# Load event file
events = pd.read_csv("C:/Users/Marcin/ds004044-download/sub-01/ses-1/func/sub-01_ses-1_task-motor_run-01_events.tsv", delimiter='\t')
#print(events)
print('events shape:', np.shape(events))

# Define the TR (Repetition Time) of your fMRI data
TR = 2.0  # Replace with the actual TR value of your data

# Calculate the number of volume scans per event
scans_per_event = 8

# Calculate the total number of scans
total_scans = len(events) * scans_per_event

# Create the frame_times array
frame_times = np.arange(0, total_scans) * TR

# Create the design matrix
design_matrix = make_first_level_design_matrix(frame_times=frame_times, events=events)

# Print the shape of the design matrix
print("Design matrix shape:", design_matrix.shape)

#________________________________________________________

#first level analysis
from nilearn.glm.first_level import FirstLevelModel
first_level_model = FirstLevelModel(t_r = 2)
first_level_model = first_level_model.fit(fmri_img, events=events, design_matrices=design_matrix)

fsaverage = nilearn.datasets.fetch_surf_fsaverage()

#define contrasts
contrasts = {
    'Rest': np.array([1] + [0] * 22),  # Contrast vector for Rest (Condition 0)
    'Condition1': np.array([0] + [1] + [0] * 21),  # Contrast vector for Condition 1
    'Condition2': np.array([0] * 2 + [1] + [0] * 20),  # Contrast vector for Condition 2
    'Condition3': np.array([0] * 3 + [1] + [0] * 19),  # Contrast vector for Condition 3
    'Condition4': np.array([0] * 4 + [1] + [0] * 18),  # Contrast vector for Condition 4
    'Condition5': np.array([0] * 5 + [1] + [0] * 17),  # Contrast vector for Condition 5
    'Condition6': np.array([0] * 6 + [1] + [0] * 16),  # Contrast vector for Condition 6
    'Condition7': np.array([0] * 7 + [1] + [0] * 15),  # Contrast vector for Condition 7
    'Condition8': np.array([0] * 8 + [1] + [0] * 14),  # Contrast vector for Condition 8
    'Condition9': np.array([0] * 9 + [1] + [0] * 13),  # Contrast vector for Condition 9
    'Condition10': np.array([0] * 10 + [1] + [0] * 12),  # Contrast vector for Condition 10
    'Condition11': np.array([0] * 11 + [1] + [0] * 11),  # Contrast vector for Condition 11
    'Condition12': np.array([0] * 12 + [1] + [0] * 10),  # Contrast vector for Condition 12
}


from nilearn.glm.contrasts import compute_contrast

#LEFT hemisphere
texture = surface.vol_to_surf(fmri_img, fsaverage.pial_left)
labels, estimates = run_glm(texture.T, design_matrix.values)

for index, (contrast_id, contrast_val) in enumerate(contrasts.items()):
    print('  Contrast % i out of %i: %s, left hemisphere' %
          (index + 1, len(contrasts), contrast_id))
    # compute contrast-related statistics
    contrast = compute_contrast(labels, estimates, contrast_val,
                                contrast_type='t')
    # we present the Z-transform of the t map
    z_score = contrast.z_score()
    # we plot it on the surface, on the inflated fsaverage mesh,
    # together with a suitable background to give an impression
    # of the cortex folding.
    plotting.plot_surf_stat_map(
        fsaverage.infl_left, z_score, hemi='left',
        title=contrast_id, colorbar=True,
        threshold=2, bg_map=fsaverage.sulc_left)

#RIGHT hemisphere
texture = surface.vol_to_surf(fmri_img, fsaverage.pial_right)
labels, estimates = run_glm(texture.T, design_matrix.values)

for index, (contrast_id, contrast_val) in enumerate(contrasts.items()):
    print('  Contrast % i out of %i: %s, right hemisphere' %
          (index + 1, len(contrasts), contrast_id))
    # compute contrast-related statistics
    contrast = compute_contrast(labels, estimates, contrast_val,
                                contrast_type='t')
    # we present the Z-transform of the t map
    z_score = contrast.z_score()
    # we plot it on the surface, on the inflated fsaverage mesh,
    # together with a suitable background to give an impression
    # of the cortex folding.
    plotting.plot_surf_stat_map(
        fsaverage.infl_right, z_score, hemi='right',
        title=contrast_id, colorbar=True,
        threshold=2, bg_map=fsaverage.sulc_right)
