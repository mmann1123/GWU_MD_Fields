library(data.table)
library(sf)
library(ggplot2)
library(tmap)

#this makes maps zoomable and interactive in the plot window
tmap_mode("view")


crops <- readRDS(file = "./data/HarvestDataCompiledCleanedProjected.rds")


#pracitice creating new column for variety, make Product into broad crop type,
unique(crops$Product)



crops$prod

unique(crops$year)
table(crops$year)

#looking at field e5
e5 <- subset(crops, Field=="E-05")

unique(e5$year)
e5$year <- as.factor(e5$year)

#looking at field C 8910
#looking at field e5
sort(unique(crops$Field))

b5 <- subset(crops, Field=="B-05|06|07|08")
b5 <- subset(crops, Field=="B-05|06")


unique(b5$year)
b5$year <- as.factor(b5$year)
str(b5)
table(b5$year, b5$Product)
unique(e5$year)
e5$year <- as.factor(e5$year)

#plotting b5
tm_shape(b5) + tm_bubbles(col="yield", size =.3) + tm_facets(by="year", free.scales = T)
sort(unique(crops$Field))


#plotting field e5 by year
tmap_mode("plot")
tm_shape(e5) + tm_bubbles(col="yield", size =.3) + tm_facets(by="year", free.scales = T)
  sort(unique(crops$Field))

table(e5$year)
e5dt <- as.data.table(e5) #have to change back to data.table format
head(e5dt)
str(e5dt$year)
e5dt$year <- as.numeric(e5dt$year)
table(e5dt$year)

e5plot <- e5dt[, .(avgyield=mean(yield)), by=c("year","Product")]

ggplot(e5plot, aes(year, avgyield, fill=Product))+ geom_bar(stat="identity", position=position_dodge())


#subsetting c8 and c9
c89 <- subset(crops, Field=="C-08|09" |Field=="C-09")
table(c89$year)
#plotting c8 and 9
tm_shape(c89) + tm_bubbles(col="yield", size =.3) + tm_facets(by="year")


#calcuating average yield by year
class(c89)
str(c89dt$year)
c89dt <- as.data.table(c89) #have to change back to data.table format
c89dt$year <- as.factor(c89dt$year)
c89plot <- c89dt[ , .(avgyield=mean(yield)), by = c("year","Product")]

ggplot(c89plot, aes(year, avgyield, fill=Product))+ geom_bar(stat="identity", position=position_dodge())







head(e5)
head(crops)




#next up to do: fix and separate out all fields that are combined 
unique(crops$Field)
unique(crops$fieldfix)


str(crops$fieldfix)
crops <- crops[order(crops$Field,crops$date),]
head(crops)

table(crops$year)


#fix all fields that are incorrectly labeled with fields - for example
#figure out if you can select spatially within R or if there's a good way to do it by coding
e5.18 <- subset(crops, year==2018 & Field == "E-05")

e5.18.soybean <- subset(crops, year==2018 & Field == "E-05" & Product == "SOYBEANS")
tm_shape(e5.18.soybean) + tm_bubbles(col="yield", size =.3) + tm_facets(by="Product")


tm_shape(e5.18) + tm_bubbles(col="yield", size =.3) + tm_facets(by="Product")
unique(e5.18$Product)



#fix Product column to show consistent major crop types - add variety column for variety information
#for example DKC62-98RIB is listed under products, google shows it's a corn variety, so put Corn in product (with correct case), and put
#the variety in a new column


#get all the dates and fields where soybeans and alfalfa have been used.
#figure out whether you should change the points to rasters, squares/polygons or what the best way to make points into area
#figure out break even point on yields for costs, talk to shannon dill and taylor about that

###############################################
########################
#focusing on e5 field fix
########################
###############################################
e5 <- subset(crops, Field == "E-05")
tm_shape(e5) + tm_bubbles(col="yield", size =.3)
#
tm_shape(e5) + tm_bubbles(col="date", size =.3)

unique(e5$date)
unique(e5$Date)


unique(e5$year)

class(e5$Date)
e5$Date <- as.character(e5$Date)
class(e5$date)


names(e5)

# this shows that the problem mapping is on this date


#confirms these are problem ones
e5misnamed <- subset(e5, Date == "9/26/2018" | Date == "11/6/2019")
tm_shape(e5misnamed) + tm_bubbles(col="Date", size =.3)


#confirmse we got all the misnames ones out
confirminggotallofthem <- subset(e5, Date != "9/26/2018" & Date != "11/6/2019")
unique(confirminggotallofthem$Date)
tm_shape(confirminggotallofthem) + tm_bubbles(col="Date", size =.3)

###############################################
###############################################
###############################################
#FOR TAYLOR look into renaming in the original crops dataset, field e5, with "9/26/2018",  "11/6/2019" 
#rename field name to Z- or even better get the field map and name it better.
###############################################
###############################################
###############################################


crops










###############################################
###############################################
###############################################

?sf
str(e5.18)

#looking ovr E-2 in 2018 when there was a bufer strip
unique(e5.18$Product)
e5.18 <- subset(crops, year==2018 & Field == "E-05")
table(e5.18$Product)

setDT(e5.18)[, .(meanbycrop = mean(yield)), by = Product]

tm_shape(e5.18) + tm_bubbles(col="yield", size =.1) + tm_facets(by="Product")


hist(e5.18$yield)

explore <- setDT(crops)[, .(meanharvest=mean(Yld.Vol.Dry..bu.ac.), section=section), by = .(Field,year,Product)]
duplicated()
explore <- unique(explore)

class(crops)

explore$year <- as.factor(explore$year)

#facet on product
ggplot(data= explore, aes(x=year, y=meanharvest, fill=Product)) +
  geom_bar(stat="identity",position=position_dodge()) +
  facet_wrap(~Product)

#subset on soybeans and facet on field 
ggplot(data= subset(explore, Product=="SOYBEANS"), aes(x=year, y=meanharvest, fill=Product)) +
  geom_bar(stat="identity",position=position_dodge()) +
  facet_wrap(~fieldfix)


#subset on soybeans and facet on section 
ggplot(data= subset(explore, Product=="SOYBEANS"), aes(x=year, y=meanharvest, fill=Product)) +
  geom_bar(stat="identity",position=position_dodge()) +
  facet_wrap(~section)


#subset on field E5 where i have the cover crops 
ggplot(data= subset(explore, fieldfix=="E-05"), aes(x=year, y=meanharvest, fill=Product)) +
  geom_bar(stat="identity",position=position_dodge()) 

plot(subset(crops, fieldfix=="E-05" & year=="2019")["yield"])
plot(subset(crops, fieldfix=="E-05" & year=="2018")["yield"])
plot(subset(crops, fieldfix=="E-05" & year=="2014")["yield"])
plot(subset(crops, fieldfix=="E-05" & year=="2013")["yield"])
plot(subset(crops, fieldfix=="E-05" & year=="2011")["yield"])
plot(subset(crops, fieldfix=="E-05" & year=="2010")["yield"])
plot(subset(crops, fieldfix=="E-05" & year=="2009")["yield"])

#fix needed here in 2018 and 2019 to remove the field in the lower right, which must be on the Wye Angus farm

#this makes maps zoomable and interactive in the plot window
tmap_mode("view")

tm_shape(subset(crops, fieldfix=="E-05" & Product == "SOYBEANS")) + tm_dots(col="yield", shape = 1) +
  tm_facets(by="year") +tm_layout("year")

names(crops)
unique(crops$Product)
tm_shape(subset(crops, Product=="SOYBEANS")) + tm_dots(col="yield", shape = 1) +
  tm_facets(by="year") 



#here's one forage bean strip - it's 2018
x <- subset(crops, fieldfix=="E-05" & Product == "SOYBEANS")
x <- as.data.table(x)
x[,.(yieldmean=mean(yield)), by=year]
table(x$year)

######################
#mapping begin!
######################
#exploring 
unique(combined$Field)
table(crops$Product)



j7 <- subset(crops, Field=="J-07")
unique(j7$Date)
unique(j7$Product)


c89 <- subset(crops, crops$Field=="C-08|09")
unique(c89$Date)

head(c89)

plot(c89)

c9 <- subset(crops, crops$Field=="C-09")
unique(c9$Date)

f2019 <- subset(crops, crops$year=="2019")

class(crops)


tm_shape(f2019) + tm_dots(col="Yld.Vol.Dry..bu.ac.") + tm_facets(by = "Product")
library(tmap)

data("World")

tmap_mode("view")
tmap_mode("plot")


tm_shape(c89) + tm_dots(col="Yld.Vol.Dry..bu.ac.")

#subsetting C9 field into corn and soybean
c9corn <- subset(c9, Product=="CORN")
c9soybean <- subset(c9, Product=="SOYBEANS")

#plotting corn
corn <- tm_shape(c9corn) +
  tm_dots(col="Yld.Vol.Dry..bu.ac.")

#plotting soy
soy<- tm_shape(c9soybean) +
  tm_dots(col="Yld.Vol.Dry..bu.ac.") +
  tm_facets(by="Date")

corn

soy

tm_shape(c9) +
  tm_dots(c("Product","Yld.Vol.Dry..bu.ac.")) +
  tm_facets(by = "Date")


