# NEED TO SWITCH PLOT TO GGPLOT  - http://stackoverflow.com/questions/7455046/how-to-make-graphics-with-transparent-background-in-r-using-ggplot2


import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
grdevices = importr('grDevices')
import rpy2.rinterface as rinterface
from bisect import bisect_left
job = []
plot_files = []
jobz = []
from django.conf import settings

#---  TAKE CLOSEST FUNCTION ---

class Rcode:

    def takeClosest(self, myList, myNumber):
        """
        Assumes myList is sorted. Returns closest value to myNumber.

        If two numbers are equally close, return the smallest number.
        """
        pos = bisect_left(myList, myNumber)
        if pos == 0:
            return myList[0],pos
        if pos == len(myList):
            return myList[-1]
        before = myList[pos - 1]
        after = myList[pos]
        if after - myNumber < myNumber - before:
           return after,pos
        else:
           return before,pos

    def rots(self, file, joob):
        rc = Rcode()
        #file = raw_input("Enter File Name ")

        string = 'arch = read.table("' + file + '", check.names=FALSE, sep=";", header=TRUE, stringsAsFactors=FALSE, fill=TRUE)'
        #string = 'arch = read.csv("' + file + '", header=TRUE)'
        robjects.r(string)
        robjects.r('arch.feat <-  arch')
        robjects.r('arch.feat$Company <- NULL #removes the class column')
        robjects.r('arch.feat$Location <- NULL')
        robjects.r('arch.feat$Work_Description <- NULL')
        robjects.r('arch.feat$End_Date <- NULL')
        robjects.r('arch.feat$X <- NULL')
        robjects.r('arch.feat$Job_Title <- NULL')
        robjects.r('arch.feat$URL <- NULL')
        robjects.r('arch.feat2 <- arch.feat')
        robjects.r('arch.feat2$Res <- NULL')
        robjects.r('arch.feat2 <- arch.feat2[complete.cases(arch.feat2),]')  #removesall N/As
        robjects.r('arch.feat2$Avg_Sal <- sub(",","", arch.feat2$Avg_Sal, fixed = TRUE)')
        robjects.r('arch.feat2$Avg_Sal <- as.numeric(sub("$","", arch.feat2$Avg_Sal, fixed = TRUE))')

        #robjects.r('arch.feat2 <- arch.feat2[sapply(arch.feat2, is.numeric),]')
        #robjects.r('arch.feat2 <- na.omit(arch.feat2)')

        # creates a column to multiple duration and Sal
        robjects.r('arch.feat2$mix <- as.numeric(arch.feat2$Duration)*as.numeric(arch.feat2$Avg_Sal)')
        robjects.r('arch.feat2 <- arch.feat2[order(arch.feat2$mix),]')

        # remove values greater than standard deviation of 2
        robjects.r('arch.feat2 <- arch.feat2[(abs(arch.feat2$mix - mean(arch.feat2$mix))< 2*sd(arch.feat2$mix)),]')


        median = robjects.r('median(arch.feat2$Job_num)')
        med = int(median[0])

        #------- CLUSTERING FOR JOB BELOW MEAN, 1 AT A TIME -----------

        for i in range(1,(med+2)):
            if i > med:
                data = robjects.r('data <- arch.feat2[arch.feat2$Job_num > ' + str(med) +',]')
            else:
                data = robjects.r('data <- arch.feat2[arch.feat2$Job_num == ' + str(i) +',]')

            length = robjects.r('dim(data)')
            length = length[0] #gives you number of rows of dataframe
            mix = data[4] #mix column

            # CREATES FILENAMES
            path1 = settings.MEDIA_ROOT
            path2 = '/' + joob + '_plot_' + str(i) + '.png'
            filename = path1 + path2
            path2 = '../media' + path2
            kstring = 'kmean <- kmeans(data,3)'
            robjects.r(kstring)
            plot_files.append(path2)

            # PLOTS THE CLUSTERS
            grdevices.png(file=filename, width=512, height=512, bg="transparent")
            robjects.r('plot(data[c("Avg_Sal","Duration")], col=kmean$cluster)')
            grdevices.dev_off()

            # GETS CENTER POINTS
            point = robjects.r('kmean$centers')

            # Grab the job info for the job closes the mean
            for j in range(6,9):
                sal_center = point[j+6] #*point[j-3]  #this is the MIX point - values depend on number of clusters

                #---BISECT METHOD
                # row = rc.takeClosest(mix, sal_center)
                # row = row[1]

                #---MIN METHOD
                row = min(range(len(mix)), key=lambda k: abs(mix[k]-sal_center))

                # get the row from the DATA df
                row_string = 'data['+ str(row) +',]'

                # gets the "REAL row number for the ARCH df
                job_row = robjects.r('rownames(' + row_string +')')
                jrow = int(job_row[0])
                job_str = 'arch[' + str(jrow) + ',]'
                #the row of the job for position = i
                final = robjects.r(job_str)
                jobz.append(final)

        return {'jobz':jobz, 'plot_files':plot_files, 'median':med}

        #gr devices stuff - http://rpy.sourceforge.net/rpy2/doc-2.2/html/graphics.html

        # plotting the cluster
        # plot(job1[c("Avg_Sal","Duration_Yrs")], col=results$cluster)

        #need to convert to Pandas
        #http://www.icare.univ-lille1.fr/wiki/index.php/How_to_convert_a_matplotlib_figure_to_a_numpy_array_or_a_PIL_image
        #Group By in Padas
        #http://pandas.pydata.org/pandas-docs/stable/groupby.html#splitting-an-object-into-groups

        #k means in scipy
        #http://hackmap.blogspot.com/2007/09/k-means-clustering-in-scipy.html

