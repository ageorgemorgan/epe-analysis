import os

# DEFAULTS ARE HOW THEY WOULD BE STORED IN MY TRILLIUM SCRATCH FOLDER!
BASE_PATH = "/scratch/agmorgan/canesm_runs/{runid}/data/nc_output/CMIP6/CMIP/CP4C/CanESM5-1/{experiment_name}/r1i1p1f1/"
FILE_PATH = "day/{var_name}/gn/v20190429/{var_name}_day_CanESM5-1_{experiment_name}_r1i1p1f1_gn_{year}0101-{year}1231.nc"
AREACELL_PATH = "fx/areacella/gn/v20190429/areacella_fx_CanESM5-1_{experiment_name}_r1i1p1f1_gn.nc"

def join_paths(var_name, 
               year_range, 
               runid, 
               experiment_name = "historical",
               base_path = BASE_PATH,
               file_path = FILE_PATH
              ):
    """
    A function for joining output files to paths based on "high-level" info like runid

    base_path is meant to represent path to a directory where all experiment info is stored.
    It is a fstring with arguments for runid and experiment_name

    file_path is the supplemental path such that base_path + file_path is where the output to be
    joined lives
    """
    return [
        os.path.join(
            base_path.format(runid = runid, experiment_name = experiment_name), 
            file_path.format(var_name = var_name, year = my_year, experiment_name = experiment_name)
        )
            for my_year in year_range
        ]


def join_paths_areacell(
                        runid,
                        experiment_name = "historical",
                        base_path = BASE_PATH,
                        areacell_path = AREACELL_PATH,
                       ):
    """
    Joins the path of an areacell .nc file, to be used when computing averages etc.
    """
    return os.path.join(
            base_path.format(runid = runid, experiment_name = experiment_name), 
            areacell_path.format(experiment_name = experiment_name),
    ) 