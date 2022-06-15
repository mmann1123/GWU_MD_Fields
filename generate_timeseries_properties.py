#%%

import xarray as xr
import geowombat as gw
import os, sys

sys.path.append("/home/mmann1123/Documents/github/xr_fresh/")
from xr_fresh.feature_calculators import *
from xr_fresh.backends import Cluster
from xr_fresh.extractors import extract_features
from glob import glob
from datetime import datetime
import matplotlib.pyplot as plt
from xr_fresh.utils import *
import logging
import warnings
import xarray as xr
from numpy import where
from xr_fresh import feature_calculators
from itertools import chain
from geowombat.backends import concat as gw_concat

_logger = logging.getLogger(__name__)
from numpy import where
from xr_fresh.utils import xarray_to_rasterio
import pandas as pd
from pathlib import Path

#%%

files = "/mnt/space/Dropbox/USA_Data/MD_Crops/MODIS_NDVI/"
band_name = "ndvi"
file_glob = f"{files}/*.tif"
strp_glob = f"{files}MOD_NDVI_%Y-%m-%dT00_00_00.tif"


complete_f = {
    "linear_time_trend": [{"param": "all"}],
    "minimum": [{}],
    "abs_energy": [{}],
    "mean_abs_change": [{}],
    "variance_larger_than_standard_deviation": [{}],
    "ratio_beyond_r_sigma": [{"r": 1}, {"r": 2}, {"r": 3}],
    "symmetry_looking": [{}],
    "sum_values": [{}],
    "autocorr": [{"lag": 1}, {"lag": 2}, {"lag": 4}, {"lag": 8}],  # mostly nan for ndvi
    "ts_complexity_cid_ce": [{}],
    "mean_change": [{}],  #  FIX  DONT HAVE
    "mean_second_derivative_central": [{}],
    "median": [{}],
    "mean": [{}],
    "standard_deviation": [{}],
    "variance": [{}],
    "skewness": [{}],
    "kurtosis": [{}],
    "absolute_sum_of_changes": [{}],
    "longest_strike_below_mean": [{}],
    "longest_strike_above_mean": [{}],
    "count_above_mean": [{}],
    "count_below_mean": [{}],
    "doy_of_maximum_first": [
        {"band": band_name}
    ],  # figure out how to remove arg for band
    "doy_of_maximum_last": [{"band": band_name}],
    "doy_of_minimum_last": [{"band": band_name}],
    "doy_of_minimum_first": [{"band": band_name}],
    "ratio_value_number_to_time_series_length": [{}],
    "quantile": [{"q": 0.05}, {"q": 0.95}],
    "maximum": [{}],
}


f_list = sorted(glob(file_glob))

dates = sorted(datetime.strptime(string, strp_glob) for string in f_list)


# add data notes
Path(f"{files}/annual_features").mkdir(parents=False, exist_ok=True)
with open(f"{files}/annual_features/0_notes.txt", "a") as the_file:
    the_file.write(
        "Gererated by /mnt/space/Dropbox/GWU_MD_Fields/generate_timeseries_properties.py \t"
    )
    the_file.write(str(datetime.now()))
#%%


# update band name
complete_f["doy_of_maximum_first"] = [{"band": band_name}]
complete_f["doy_of_maximum_last"] = [{"band": band_name}]
complete_f["doy_of_minimum_last"] = [{"band": band_name}]
complete_f["doy_of_minimum_first"] = [{"band": band_name}]


# start cluster
cluster = Cluster()
cluster.start_large_object()

# open xarray lazy
with gw.open(sorted(glob(file_glob)), band_names=[band_name], time_names=dates) as ds:
    ds = ds.chunk({"time": -1, "band": 1, "y": 350, "x": 350})  # rechunk to time

    ds.attrs["nodatavals"] = (0,)
    print(ds)

    # # generate features
    for year in sorted(list(set([x.year for x in dates]))):
        year = str(year)
        print(year)
        ds_year = ds.sel(time=slice(year + "-05-01", year + "-10-29"))
        print("interpolating")
        ds_year = ds_year.interpolate_na(dim="time", limit=5)
        ds_year = ds_year.chunk(
            {"time": -1, "band": 1, "y": 350, "x": 350}
        )  # rechunk to time

        # extract growing season year month day
        features = extract_features(
            xr_data=ds_year,
            feature_dict=complete_f,
            band=band_name,
            na_rm=True,
            persist=True,
            filepath=os.path.join(files, "annual_features/May_Oct"),
            postfix="_may_oct_" + year,
        )  #'_may_sep_'+year, '_'+year
    cluster.restart()

cluster.close()


# %%

# open xarray lazy
with gw.open(sorted(glob(file_glob)), band_names=[band_name], time_names=dates) as ds:
    ds = ds.chunk({"time": -1, "band": 1, "y": 350, "x": 350})  # rechunk to time

    ds.attrs["nodatavals"] = (0,)
    print(ds)
    # # move dates back 2 months so year ends feb 29, so month range now May = month 3, feb of following year = month 12
    # ds = ds.assign_coords(
    #     time=(pd.Series(ds.time.values) - pd.DateOffset(months=2)).values
    # )

    # # generate features
    for year in sorted(list(set([x.year for x in dates]))):
        year = str(year)
        print(year)
    #     ds_year = ds.sel(
    #         time=slice(year + "-03-01", year + "-07-29")
    #     )  # full '-03-01' to -12-29'  year+'-03-01', year+'-07-29'
    #     print("interpolating")
    #     ds_year = ds_year.interpolate_na(dim="time", limit=5)
    #     ds_year = ds_year.chunk(
    #         {"time": -1, "band": 1, "y": 350, "x": 350}
    #     )  # rechunk to time

    #     # extract growing season year month day
    #     features = extract_features(
    #         xr_data=ds_year,
    #         feature_dict=complete_f,
    #         band=band_name,
    #         na_rm=True,
    #         persist=True,
    #         filepath=os.path.join(files, "Meher_features/May_Sep"),
    #         postfix="_may_sep_" + year,
    #     )  #'_may_sep_'+year, '_'+year
    # cluster.restart()

cluster.close()
