# get-usdm-shapefiles
This is a tool to help users download large quantities of [US drought monitor shapefiles](https://droughtmonitor.unl.edu/DmData/GISData.aspx) from the GIS database.

# Clone this repo
```
git clone https://github.com/Corey4005/get-usdm-shapefiles.git
```
# Requirements 
[GNU Wget version 1.14](https://www.gnu.org/software/wget/)

# How to use this tool

Open a command prompt and enter a starting and end date:

```python
python get_usdm.py 20000104 20201229 #example timestamp representing startdate 2000-01-04 and enddate 2020-12-29 (20 years!) 
```
This script will create a file called `usdm_links.txt` containing all of the links that wget could call to download US drought monitor shapefiles. 

Then, you can call wget on the textfile and retreive the shapefiles from USDM REST API services. 

```
wget -i usdm_links.txt -P shapefiles/ --progress=bar:force:noscroll
```
All of the shapefiles between the start and end date will be downloaded to the `shapefiles` directory!

In order to unzip the .zip files in the `/shapefiles` directory so that you can get each .shp, .prj, .xml, .sbn, .dbf, open a command prompt and enter the following:

```python
python unzip.py
```
# Cool statistic

I was able to download 20 years of USDM shapefiles to my hard drive in 34 seconds using this script! 

# Example script utilizing 20 years of USDM data

For a project I was working on, I needed USDM data for [18 USDA SCAN soil moisture sites](https://www.nrcs.usda.gov/wps/portal/wcc/home/quicklinks/imap#version=167&elements=&networks=SCAN&states=AL&counties=!&hucs=&minElevation=&maxElevation=&elementSelectType=all&activeOnly=true&activeForecastPointsOnly=false&hucLabels=false&hucIdLabels=false&hucParameterLabels=false&stationLabels=&overlays=&hucOverlays=&basinOpacity=100&basinNoDataOpacity=100&basemapOpacity=100&maskOpacity=0&mode=stations&openSections=dataElement,parameter,date,basin,elements,location,networks&controlsOpen=true&popup=&popupMulti=&popupBasin=&base=esriNgwm&displayType=inventory&basinType=6&dataElement=PREC&depth=-8&parameter=PCTAVG&frequency=DAILY&duration=mtd&customDuration=&dayPart=E&year=2018&month=11&day=1&monthPart=E&forecastPubMonth=6&forecastPubDay=1&forecastExceedance=50&useMixedPast=true&seqColor=1&divColor=3&scaleType=D&scaleMin=&scaleMax=&referencePeriodType=POR&referenceBegin=1981&referenceEnd=2010&minimumYears=20&hucAssociations=true&lat=32.547&lon=-85.342&zoom=5.0) across Alabama. 

The metadata for the example is found [here](https://github.com/Corey4005/get-usdm-shapefiles/tree/main/usdascan). 

I ran the [`make_dataframe.py`](https://github.com/Corey4005/get-usdm-shapefiles/blob/main/make_dataframe.py) script on the `/shapefiles` directory to collect the USDM data for each point, for each shapefile. I then sent this data to the `/outdata` directory, where you can find an [example drought climatology](https://github.com/Corey4005/get-usdm-shapefiles/tree/main/outdata) in .csv format. 
