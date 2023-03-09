library(data.table)
library(sf)
library(ggplot2)
library(tmap)

#this makes maps zoomable and interactive in the plot window
tmap_mode("view")

#Reading RDS File
crops <- readRDS(file = "./data/HarvestDataCompiledCleanedProjected.rds")
head(crops)

#Checking for NA Values
colSums(is.na(crops))

#data after NA values removed
new_crops = subset(crops,select = -c(Satellites,Hding.Veh.deg.,Diff.Status.1,Active.Rows..1..,
                                    VDOP,HDOP,PDOP,Elvtr.Speed.rpm.,Com.Sale.G..., Income...ac.,Profit.Loss...ac.))
head(new_crops)


#cor(new_crops[,c('Track.deg.','Swth.Wdth.ft.','Distance.ft.','Duration.s.','Elevation.ft.','Crop.Flw.M..lb.s.',' Moisture...','Grain.Temp..F.','Yld.Mass.Dry..lb.ac.','Yld.Mass.Wet..lb.ac.','Yld.Vol.Dry..bu.ac.','Yld.Vol.Wet..bu.ac.','Speed.mph.','Prod.ac.h.','Crop.Flw.V..bu.h.','year','month','yield')])
# correlation for all variables
#round(cor(data_),digits = 2 )



#Simple Linear Regression for yield vs Track.deg.
#The function used for building linear models is lm(). 
linearMod <- lm(yield ~ Track.deg., data=new_crops)  # build linear regression model on full data
print(linearMod)

#Now that we have built the linear model, we also have established the relationship between the predictor and response in the form of a mathematical formula for yield as a function for Track.deg. For the  output, you can notice the ‘Coefficients’ part having two components: Intercept:  99.55864 , speed: 0.03022   These are also called the beta coefficients. In other words,
#yield = Intercept + (β∗ Track.deg.)
#=> yield =  99.55864 + 0.03022 ∗ Track.deg.


