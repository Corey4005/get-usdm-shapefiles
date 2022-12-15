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

# Cool statistic

I was able to download 20 years of USDM shapefiles to my hard drive in 34 seconds using this script!
