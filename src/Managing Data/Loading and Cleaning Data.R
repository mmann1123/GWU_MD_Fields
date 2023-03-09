library(data.table)
library(tmap)
library(sf)
library(dplyr)
library(compare)


allfiles <- list.files("./AgLeader data/", recursive = T)

head(allfiles)

#testing grepl function to find word "harvest"
test <- grepl("Harvest", allfiles, ignore.case = TRUE)
table(test)

#pulling out only files with word harvest in them.
harvest <- allfiles[grepl("Harvest", allfiles, ignore.case = TRUE)]
test3 <- grepl("csv", harvest, ignore.case = TRUE)
table(test3)

#pulling out only CSV files with harvest in file name.
harvest.only.csv <- harvest[grepl("csv", harvest, ignore.case = TRUE)]

#read all csv files into a large list of tables
tables <- lapply(paste("./agleader data/",harvest.only.csv, sep=""), read.csv, header = TRUE)

#saving it for easy reloading
saveRDS(tables, file = "./data/harvest.all.projects.joe.tommy.rds")

###############
#reloading
harvest <- readRDS(file = "./data/harvest.all.projects.joe.tommy.rds")

#makes into data.table
harvestdt <- lapply(harvest, as.data.table)

#removes list and puts into giant single spreadsheet
combined <- rbindlist(harvestdt, fill = TRUE, idcol = TRUE)

#Removing duplicates
#we found that when including more variables like ""Elevation.ft.","Crop.Flw.M..lb.s.","Moisture..."" that we gained about 1215 new rows, we're not sure why, they may be 
#duplicates, but it's such a small number we're going to leave it for now. 
#Potentially more concerning, when only using the following variables, "Date,Latitude,Longitude,Field,Distance.ft.,Yld.Mass.Dry..lb.ac.," there were about 500k rows eliminated
#it's hard to say for sure if we are gaining a lot of new duplicates, or not, but something we can come back to .

rem.dups <- unique(combined, by=c("Date","Latitude","Longitude","Field","Distance.ft.","Yld.Mass.Dry..lb.ac.","Prod.ac.h.","Speed.mph.","Prod.ac.h.","Track.deg.","Elevation.ft.","Crop.Flw.M..lb.s.","Moisture..."))

#this returns 1.729 million, about 1000 fewer than above.
#rem.dups.fewer <- unique(combined, by=c("Date","Latitude","Longitude","Field","Distance.ft.","Yld.Mass.Dry..lb.ac.","Prod.ac.h.","Speed.mph.","Prod.ac.h.","Track.deg."))

#this one returns 1.16 million records, but doesn't have nearly as many variables.  it seems like it would be enough to pull out all the duplicates, but we are erring on the side
#of being overly inclusive so have settled on the code above returning 1.729 million variables.
#rem.dups.dplyr <-  distinct(combined, Date,Latitude,Longitude,Field,Distance.ft.,Yld.Mass.Dry..lb.ac., .keep_all = TRUE)

#this is how you can compare the different datasets:
# #comparison <- anti_join(rem.dups,rem.dups.fewer)
# head(comparison)
# unique(comparison$Date)
# unique(comparison$Field)
# 
# checking <- subset(rem.dups.fewer, Date=="10/25/2018" & Field=="J-03")
# head(checking)
# 
# checking.more.inclusive <- subset(rem.dups, Date=="10/25/2018" & Field=="J-03")
# head(checking.more.inclusive)
# 
# #we put them in different orders to check what was going on
# checking.more.inclusive <- checking.more.inclusive[order(checking.more.inclusive$Prod.ac.h.),]
# #we put them in different orders to check what was going on
# checking.more.inclusive <- checking.more.inclusive[order(checking.more.inclusive$Obj..Id),]
# 
# head(checking.more.inclusive)
# checking.more.inclusive[1:10, ]
# 
# #we plotted them but it didn't help.
# #read as SF object - this lets the program know that these two columsn are the spatial data
# sfcombo = st_as_sf(checking.more.inclusive, coords = c("Longitude", "Latitude"), crs = 4326)
# sfcombo2 = st_as_sf(checking, coords = c("Longitude", "Latitude"), crs = 4326)
# #this makes maps zoomable and interactive in the plot window
# tmap_mode("view")
# tm_shape(sfcombo) + tm_bubbles(col="Yld.Mass.Dry..lb.ac.", size =.3) 
# tm_shape(sfcombo2) + tm_bubbles(col="Yld.Mass.Dry..lb.ac.", size =.3) 


##########Saving
saveRDS(rem.dups, file= "./data/all.Tommy.Joe.harvest.duplicates.removed.rds")


#read as Spatial SF object - this lets the program know that these two columsn are the spatial data
sfcombo = st_as_sf(rem.dups, coords = c("Longitude", "Latitude"), crs = 4326)
head(sfcombo)

#good tutorial on CRS's and projections: https://geocompr.robinlovelace.net/reproj-geo-data.html
#source for major CRS's on MD website under the CADD section: https://imap.maryland.gov/iMap2/Pages/training-documents.aspx 
#a good one to use in metric: https://epsg.io/6487

#state law specifies using feet in this one: https://epsg.io/2248
crops = st_transform(sfcombo, 2248)

#########################################
#format your dates so you can look at year, month, etc.

names(crops)
head(crops)

crops$date <- as.Date(crops$Date,format='%m/%d/%Y')

#i have to do this because geopackage can't have same named columns, it's case INSENSITIVE.
crops$dateorig <- crops$Date 
crops$Date <- NULL

crops$year <- as.numeric(format(crops$date,'%Y'))
crops$month <- as.numeric(format(crops$date,'%m'))
crops$dayofyear  <- strftime(crops$date, format = "%j")

###fixing field names a little and adding a 'section' letter based field column
# unique(crops$Field)
# crops$Field <- as.character(crops$Field)
# 
# crops$fieldfix <- ifelse(crops$Field=="McGrath Study", "Z-McGrath Study",
#                          ifelse(crops$Field=="Manor House", "Z-Manor House",
#                                 ifelse(crops$Field=="Dively corn 2013", "Z-Dively corn 2013",
#                                        ifelse(crops$Field=="Ken Plots", "Z-Ken Plots", crops$Field))))
# 
# head(crops)
# unique(crops$fieldfix)

#This creates a Range field 
crops$range <- substr(crops$Field,1,1)
head(crops)

crops$yield <- crops$Yld.Vol.Dry..bu.ac.


saveRDS(crops, file = "./data/HarvestDataCompiledCleanedProjected.rds")
st_write(crops, "./data/CropDataCompiledCleanedProjected.gpkg", driver="GPKG", append = FALSE)  # Create a geopackage file
class(crops)


