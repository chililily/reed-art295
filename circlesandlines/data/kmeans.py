import math

class County:
    def __init__(self, name, values):
        self.name = name
        self.values = values
    def distance(self, othervals):
        dist = 0
        for i in range(len(self.values)):
            dist += abs(self.values[i]-othervals[i])
        return dist

class Cluster:
    def __init__(self):
        self.centroid = []
        self.contents = []
    def updateCentroid(self):
        for i in range(len(self.centroid)):
            total = 0
            for county in self.contents:
                total += county.values[i]
            mean = total/len(self.contents)
            self.centroid[i] = mean
    def names(self):
        names = ""
        for c in self.contents:
            names += c.name + "; "
        return names
    def clear(self):
        self.contents = []

def readData(filename):
    counties = []
    with open(filename, "r") as f:
        data = f.readlines()
        for line in data[1:]:
            c = line.split(";")
            i = 2
            while i <= len(c)-1:
                c[i] = float(c[i])
                i += 1
            c[3] = c[3]/c[18]
            counties.append(County(c[0], c[2:18]))
    return counties

def normalizeCounties(counties):
    for i in range(len(counties[0].values)):
        total = 0
        for c in counties:
            total += c.values[i]
        mean = total/len(counties)
        diffsum = 0
        for c in counties:
            c.values[i] = c.values[i] - mean
            diffsum += c.values[i]**2
        stdev = (diffsum/len(counties))**0.5
        for c in counties:
            c.values[i] = c.values[i]/stdev

def initClusters(counties, num):
    clusters = []
    for i in range(num):
        newcluster = Cluster()
        newcluster.centroid = counties[i].values[:]
        clusters.append(newcluster)
    return clusters

def placeCounties(counties, clusters):
    for county in counties:
        best, minDist = clusters[0], county.distance(clusters[0].centroid)
        for c in clusters[1:]:
            dist = county.distance(c.centroid)
            if dist < minDist:
                best, minDist = c, dist
        best.contents.append(county)

def updateCentroids(clusters):
    for c in clusters:
        c.updateCentroid()

def clearClusters(clusters):
    for c in clusters:
        c.clear()

def writeOutput(clusters, filename):
    with open(filename, "w") as f:
        i = 1
        for c in clusters:
            f.write("Cluster " + str(i) + "\n")
            f.write("size: " + str(len(c.contents)) + "\n")
            f.write(str(c.centroid) + "\n")
            f.write(c.names())
            f.write("\n" + "\n")
            i += 1

def kmeans(infile, outfile, k, cycles):
    counties = readData(infile)
    normalizeCounties(counties)
    clusters = initClusters(counties, k)
    for i in range(cycles):
        clearClusters(clusters)
        placeCounties(counties, clusters)
        updateCentroids(clusters)
    writeOutput(clusters, "output45.txt")

kmeans("counties.txt", "output45.txt", 45, 120)
