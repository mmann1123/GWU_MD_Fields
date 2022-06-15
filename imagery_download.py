# use geepy environment, run earthengine authenticate in commandline first
#%%

import pendulum
import ee
from helpers import *
from ipygee import *
import ipygee as ui

ee.Initialize()
import geetools
from geetools import ui, cloud_mask, batch


# ## Define an ImageCollection
site = ee.Geometry.Polygon(
    [
        [-76.1684467617, 38.9017496111],
        [-76.1185919989, 38.9017496111],
        [-76.1185919989, 38.9453828665],
        [-76.1684467617, 38.9453828665],
        [-76.1684467617, 38.9017496111],
    ]
)


# Set parameters
bands = ["B2", "B3", "B4", "B8"]
scale = 10
# date_pattern = "mm_dd_yyyy"  # dd: day, MMM: month (JAN), y: year
folder = "MD_Crop_Images"

region = site
extra = dict(sat="Sen_TOA")
CLOUD_FILTER = 75

#%%
for year in list(range(2017, 2022)):
    for month in list(range(1, 13)):

        print("year ", str(year), " month ", str(month))
        dt = pendulum.datetime(year, month, 1)
        # start = pendulum.datetime(2017, 1, 1)
        # end = pendulum.datetime(2021, 12, 31)

        # period = pendulum.period(start, end)
        # for dt in period.range("months", 3):

        collection = get_s2_sr_cld_col(
            site,
            dt.start_of("month").to_datetime_string()[0:10],
            dt.end_of("month").to_datetime_string()[0:10],
            CLOUD_FILTER=CLOUD_FILTER,
        )

        s2_sr = (
            collection.map(add_cld_shdw_mask)
            .map(apply_cld_shdw_mask)
            .select(bands)
            .median()
        )
        s2_sr = geetools.batch.utils.convertDataType("uint32")(s2_sr)
        # eprint(s2_sr)

        # # export clipped result in Tiff
        crs = "EPSG:4326"

        img_name = "S2_SR_" + str(year) + "_" + str(month).zfill(2)
        export_config = {
            "scale": scale,
            "maxPixels": 5000000000,
            "driveFolder": folder,
            "region": site,
        }
        task = ee.batch.Export.image(s2_sr, img_name, export_config)
        task.start()

#%%% Download Modis
poly = ee.Geometry.Polygon(
    [
        [-76.1684467617, 38.9017496111],
        [-76.1185919989, 38.9017496111],
        [-76.1185919989, 38.9453828665],
        [-76.1684467617, 38.9453828665],
        [-76.1684467617, 38.9017496111],
    ]
)

for collection in ["MYD13Q1", "MOD13Q1"]:
    col13q1 = ee.ImageCollection(f"MODIS/061/{collection}")

    col13q1_mask = (
        col13q1.map(cloud_mask.modis13q1())
        .filterBounds(poly)
        .filterDate("2008-01-01", "2022-01-01")
        .select("NDVI")
    )

    # eprint(col13q1_mask)

    tasklist = batch.Export.imagecollection.toDrive(
        col13q1_mask,
        folder="MD_Crop_Images",
        scale=250,
        region=poly,
        namePattern="MOD_NDVI_{system_date}",
        dataType="int",
        skipEmptyTiles=True,
        maxPixels=1e13,
        crs="EPSG:4326",
    )
    print("done")

#%%
# modis = ee.ImageCollection("MODIS/061/MOD13Q1")
# imagecol = (
#     ee.ImageCollection("MODIS/061/MOD13Q1")
#     .filterDate("2019-02-21", "2019-03-23")
#     .filterBounds(poly)
# )
# imagecol_masked = imagecol.map(cloud_mask.modis13q1())

# #%%

# MapMOD = ui.Map()
# MapMOD.show()

# #%%

# site = ee.Geometry.Point([-71.8, -43])
# date = ee.Date("2017-08-01")
# visMOD = {
#     "bands": ["sur_refl_b01", "sur_refl_b02", "sur_refl_b03"],
#     "min": 0,
#     "max": 5000,
# }
# modis = modis.filterDate(date, date.advance(4, "month"))
# i_mod = ee.Image(modis.first())
# MapMOD.addLayer(i_mod, visMOD, "MODIS TERRA Original Image")
# MapMOD.centerObject(site, zoom=8)


# mod_mask = cloud_mask.modis13q1()
# i_masked = mod_mask(i_mod)
# MapMOD.addLayer(i_masked, visMOD, "Masked MODIS")


#%%

# import pendulum
# import ee

# ee.Initialize()
# import geetools
# from ipygee import *

# # ## Define an ImageCollection
# site = ee.Geometry.Polygon(
#     [
#         [-76.1684467617, 38.9017496111],
#         [-76.1185919989, 38.9017496111],
#         [-76.1185919989, 38.9453828665],
#         [-76.1684467617, 38.9453828665],
#         [-76.1684467617, 38.9017496111],
#     ]
# )


# # Set parameters
# bands = ["B2", "B3", "B4", "B8"]
# scale = 10
# name_pattern = "{sat}_{system_date}"
# # date_pattern = "mm_dd_yyyy"  # dd: day, MMM: month (JAN), y: year
# folder = "MYFOLDER"
# data_type = "uint32"
# # region = site
# extra = dict(sat="Sen_TOA")


# mask_all = geetools.cloud_mask.sentinel2()


# for year in list(range(2017, 2022)):
#     for month in list(range(1, 13)):
#         print("year ", str(year), " month ", str(month))
#         dt = pendulum.datetime(year, month, 1)

#         # mask_holl = cloud_mask.applyHollstein()
#         collection = (
#             ee.ImageCollection("COPERNICUS/S2_SR")  # "COPERNICUS/S2_SR"
#             .filterBounds(site)
#             .filterDate(
#                 dt.start_of("month").to_datetime_string()[0:10],
#                 dt.end_of("month").to_datetime_string()[0:10],
#             )
#             .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 30))
#             .select(bands)
#             .map(lambda img: img.addBands(geetools.indices.ndvi(img, "B8", "B4")))
#         )

#         eprint(collection)


#%%

#         geepy.get_sentinel(
#             product="COPERNICUS/S2",
#             aoi="/mnt/space/Dropbox/GWU_MD_Fields/bbox.shp",
#             start_date=dt.start_of("month").to_datetime_string()[0:10],
#             end_date=dt.end_of("month").to_datetime_string()[0:10],
#             export=True,
#             output="Sen_TOA_" + str(year) + "_" + str(month),
#         )


# # %%

# import ee

# ee.Initialize()
# from geetools import tools, composite, cloud_mask, indices
# from geetools import batch

# p = ee.Geometry.Polygon(
#     [
#         [-76.1684467617, 38.9017496111],
#         [-76.1185919989, 38.9017496111],
#         [-76.1185919989, 38.9453828665],
#         [-76.1684467617, 38.9453828665],
#         [-76.1684467617, 38.9017496111],
#     ]
# )
# fc = ee.FeatureCollection([p])
# col = (
#     ee.ImageCollection("COPERNICUS/S2")
#     .filterBounds(p)
#     .filterDate(
#         dt.start_of("month").to_datetime_string()[0:10],
#         dt.end_of("month").to_datetime_string()[0:10],
#     )
#     .map(cloud_mask.sentinel2())  # .hollsteinS2())
#     .map(lambda img: img.addBands(indices.ndvi(img, "B8", "B4")))
# )

# image = col.mosaic()

# task = batch.Export.image.toDriveByFeature(
#     image,
#     collection=fc,
#     folder="tools_exportbyfeat",
#     namePattern="test {date}",
#     scale=10,
#     dataType="float",
#     verbose=True,
# )
#%%

# bands = ["B2", "B3", "B4"]
# scale = 30
# name_pattern = "{sat}_{system_date}_{WRS_PATH:%d}-{WRS_ROW:%d}"
# date_pattern = "ddMMMy"  # dd: day, MMM: month (JAN), y: year
# folder = "MYFOLDER"
# data_type = "uint32"
# extra = dict(sat="L8SR")
# region = site


# tasks = geetools.batch.Export.imagecollection.toDrive(
#     collection=col,
#     folder=folder,
#     region=site,
#     namePattern=name_pattern,
#     scale=scale,
#     dataType=data_type,
#     datePattern=date_pattern,
#     extra=extra,
#     verbose=True,
#     maxPixels=int(1e13),
# )


# %%

for year in list(range(2016, 2022))[0:1]:
    for month in list(range(1, 13))[0:1]:

        dt = pendulum.datetime(2016, month, 1)


# ## Define an ImageCollection
site = ee.Geometry.Polygon(
    [
        [-76.1684467617, 38.9017496111],
        [-76.1185919989, 38.9017496111],
        [-76.1185919989, 38.9453828665],
        [-76.1684467617, 38.9453828665],
        [-76.1684467617, 38.9017496111],
    ]
)
mask_all = cloud_mask.sentinel2()

# mask_holl = cloud_mask.applyHollstein()
collection = (
    ee.ImageCollection("COPERNICUS/S2")
    .filterBounds(site)
    .limit(5)
    # .map(mask_all)
    .map(lambda img: cloud_mask.applyHollstein(img))
    .map(lambda img: img.addBands(indices.ndvi(img, "B8", "B4")))
)


# Set parameters
bands = ["B2", "B3", "B4", "B8"]
scale = 10
name_pattern = "{sat}_{system_date}_hollstein"
## the keywords between curly brackets can be {system_date} for the date of the
## image (formatted using `date_pattern` arg), {id} for the id of the image
## and/or any image property. You can also pass extra keywords using the `extra`
## argument. Also, numeric values can be formatted using a format string (as
## shown in {WRS_PATH:%d} (%d means it will be converted to integer)
date_pattern = "ddMMMy"  # dd: day, MMM: month (JAN), y: year
folder = "MYFOLDER"
data_type = "uint32"
region = site

# ## Export
tasks = geetools.batch.Export.imagecollection.toDrive(
    collection=collection,
    folder=folder,
    region=site,
    namePattern=name_pattern,
    scale=scale,
    dataType=data_type,
    datePattern=date_pattern,
    extra=extra,
    verbose=True,
    maxPixels=int(1e13),
)
