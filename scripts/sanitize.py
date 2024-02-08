import os
import shutil
from glob import glob

from nilearn import image


def convert_segmentations():
    in_dir = os.path.abspath(".")
out_dir = os.path.abspath("tpl-dHCPInfant")

mean_dir = os.path.join(in_dir, "mean")
age_dirs = sorted(glob(os.path.join(mean_dir, "ga_*")))
ages = [os.path.basename(age_dir) for age_dir in age_dirs]

template_dict = {
    "mask": "tpl-dHCPInfant_cohort-{weeks}_res-3_desc-brain_mask",
    "structures": "tpl-dHCPInfant_cohort-{weeks}_res-3_desc-structures_dseg",
    "template_t1": "tpl-dHCPInfant_cohort-{weeks}_res-3_T1w",
    "template_t2": "tpl-dHCPInfant_cohort-{weeks}_res-3_T2w",
    "tissues": "tpl-dHCPInfant_cohort-{weeks}_res-3_desc-tissues_dseg",
}

for age in ages:
    weeks = age.split("_")[1]
    cohort_dir = os.path.join(out_dir, f"cohort-{weeks}")
    os.makedirs(cohort_dir, exist_ok=True)

    struct_dir = os.path.join(in_dir, "structures", age)
    tissue_dir = os.path.join(in_dir, "tissues", age)
    template_dir = os.path.join(mean_dir, age)

    for k, v in template_dict.items():
        in_file = os.path.join(template_dir, f"{k}.nii.gz")
        out_file = os.path.join(cohort_dir, v.format(weeks=weeks) + ".nii.gz")
        shutil.copyfile(in_file, out_file)

    tissue_psegs = sorted(glob(os.path.join(tissue_dir, "tissue_*.nii.gz")))
    tissue_pseg_img = image.concat_imgs(tissue_psegs)
    out_tissue_pseg = os.path.join(
        cohort_dir,
        f"tpl-dHCPInfant_cohort-{weeks}_res-3_desc-tissues_probseg.nii.gz",
    )
    tissue_pseg_img.to_filename(out_tissue_pseg)

    struct_psegs = sorted(glob(os.path.join(struct_dir, "structure_*.nii.gz")))
    struct_pseg_img = image.concat_imgs(struct_psegs)
    out_struct_pseg = os.path.join(
        cohort_dir,
        f"tpl-dHCPInfant_cohort-{weeks}_res-3_desc-structures_probseg.nii.gz",
    )
    struct_pseg_img.to_filename(out_struct_pseg)
