# title: "Data Analysis and Visualization Module of Api-TRACE"
# author: "Babur Erdem"
# date: "2023-07-26"
# update date: "2024-08-17"
###
 
# Load necessary libraries.

library(ggplot2)
library(dplyr)
library(ggpubr)

getwd()

# Define variables for the experiment.

VideoName <- readline(as.character("Write the name of the experiment video: "))

IndVar <- readline(as.array("Define the independent variables: "))
IndVars <- as.vector((scan(text = IndVar, what = "", sep = ",")))
IndVars <- c(IndVars)

fps <- readline(as.character("Indicate the fps value of the experiment video: "))
fps <- as.numeric(fps)

SamplingRate <- readline(as.character("Define the desired downsampling rate (per sec): "))
SamplingRate <- as.numeric(SamplingRate)

# Following parts are used for analysis; do not change anything below.
# Read exposure event data, converting boolean values to binary.

ShockDf <- read.csv(gsub(" ", "", paste(VideoName, "_Exposure.txt")), sep = "\t", header = T)
ShockDf[ShockDf == "True"] <- 1
ShockDf[ShockDf == "False"] <- 0
ShockDf <- data.frame(sapply(ShockDf, function(x) as.numeric(as.character(x))))

#Read metadata

MetaDf <- read.csv(gsub(" ", "", paste(VideoName, "_Metadata.txt")), sep = "\t", header = T)

# Create a dataframe to store processed exposure event data.

columns = c("Video", colnames(MetaDf), "IndVar", "BeeID",
            "Time", "ExposureDuration") 

ShockedDf = data.frame(matrix
                       (nrow =(ceiling(nrow(ShockDf)/(fps*SamplingRate)))*(ncol(ShockDf)), 
                         ncol = length(columns)))
colnames(ShockedDf) <- columns

# Construct structured dataframe.
# Populate the metadata columns in the dataframe.

ShockedDf$Video <- rep(VideoName, nrow(ShockedDf))

for (colnom in colnames(MetaDf)) {
  
  IV <- as.numeric(which(colnames(ShockedDf)==colnom))
  InV <- as.numeric(which(colnames(MetaDf)==colnom))
  shocker <- c()
  
  for(vars in MetaDf[,InV]){
    shocker <- append(shocker, rep(vars, (nrow(ShockedDf)/nrow(MetaDf))), after = length(shocker))
  }
  ShockedDf[, IV] <- shocker
}

mergeInVars <- c()  
for (inVar in IndVars) {
  indepVar <- c()
  inVarColNo <- as.numeric(which(colnames(ShockedDf)==inVar ))
  indepVar <- ShockedDf[, inVarColNo]
  mergeInVars <- paste(mergeInVars, indepVar, sep = "_")
} 
ShockedDf$IndVar <- gsub("^.", "",mergeInVars)

# Generate Bee IDs based on the structure of the data.

ShockedDf$BeeID <- gsub(" ", "", (paste( VideoName, "_", "Bee", sprintf("%02d",ShockedDf$BeeNo))))

# Define time points for exposure duration calculation.

times <- c()
j=0
while (j <= ((ceiling((nrow(ShockDf))/(fps)))-1)) {
  j=j+SamplingRate
  if (j > (ceiling((nrow(ShockDf))/(fps)))){
    j = (ceiling((nrow(ShockDf))/(fps)))
  }
  times = c(times,j)
}

ShockedDf$Time <- rep(times, ncol(ShockDf))

# Calculate exposure duration for each time interval.

shockDuration = c()
for (ind in c(1:ncol(ShockDf))){
  n=1
  m=1
  shockDur = c()
  while (m <= nrow(ShockDf)){
    m=n+(fps*SamplingRate)
    x = sum(ShockDf[c(n:m), ind])
    n=n+(fps*SamplingRate)
    shockDur=c(shockDur,x)
  }
  shockDuration = c(shockDuration, shockDur)  
}
ShockedDf$ShockDuration <- shockDuration/fps

# Remove rows with NA values.

ShockedDf <- na.omit(ShockedDf)

# Write shock duration for each bee to a txt file.

write.table(ShockedDf, paste((gsub("_Exposure.txt", "" ,VideoName)), "_Data.txt", sep = ""), sep = "\t", quote=FALSE)

# Generate and save a line plot, represents for each individual's learning curve.

ggplot(data=ShockedDf, aes(x=Time, y=ShockDuration, col$BeeID)) + 
  geom_line(alpha=0.5,lwd=1) + 
  ggtitle(paste("Learning profiles of", gsub('_Exposure.txt','',VideoName), sep=" "))+
  theme(
    legend.background = element_rect(colour = NA),  
    legend.box = NULL,
    legend.key = element_rect(fill = "white", colour = "white"),
    legend.title = element_blank(),
    legend.text = element_text( size = 9),
    legend.position = "bottom",
    legend.direction ="horizontal",
    plot.title = element_text(size=13), 
    axis.title.x = element_text(size=11),
    axis.title.y = element_text(size=11),
    panel.grid.major = element_line(color = "lightgrey"),
    panel.grid.minor = element_line(color="lightgrey"),
    panel.background = element_rect(fill = "white")
  ) +
  ylim(0,(SamplingRate+5))+
  xlab("Seconds") + 
  ylab(paste("Exposure Duration in ", SamplingRate, " sec", sep = ""))+
  facet_wrap(~BeeID)

ggsave(paste(gsub("_Exposure.txt", "" ,VideoName), "_IndividualsProfiles.jpg", sep = ""))

# Generate and save a line plot, represents group learning curve.

ggline(ShockedDf, x="Time", y = "ShockDuration", color = "IndVar",
       add = c("mean_se"),size=1, ylab = (paste("Exposure Duration in ", SamplingRate, " sec", 
                                                sep = "")), xlab = "Seconds")+
  ggtitle(paste("Learning curves of", VideoName, sep=" "))+
  theme(
    legend.position = "bottom",  
    legend.title=element_blank(),
    plot.title = element_text(size=13), 
    axis.title.x = element_text(size=11),
    axis.title.y = element_text(size=11),
    panel.grid.major = element_line(color = "white"),
    panel.grid.minor = element_line(color="white"),
    panel.background = element_rect(fill = "white"),
  ) 

ggsave(paste(gsub("_Exposure.txt", "" ,VideoName), "_ExposurePlot.jpg", sep = ""))
