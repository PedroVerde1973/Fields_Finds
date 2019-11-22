# Fields_Finds
Fields and Finds – A Web Interface
Web URL: https://www.geos.ed.ac.uk/~s1887709/cgi-bin/fields_finds.py 

Introduction
Following the recent discovery of several important archaeological finds in farmers’ fields located near the city of Edinburgh, Scotland, a relational database system was designed and implemented to assist with the ongoing management and protection of the discoveries, and to aid researchers and local farmers in planning their respective activities. To assist with this, a web interface has been developed to provide users with a place where they can learn more about the archaeological finds, and the fields in which they are located. The web interface provides information on both spatial (mapping and locations) and aspatial (non-spatial information about each field and find) aspects of the fields and finds.

The Solution
The objective of this project is to build a site that is fit for purpose, easy to use, legible and suitably dynamic to accommodate any future changes to the database records (e.g. change of field owner or size, addition of new finds). The web interface has been constructed using a combination of Python, Jinga HTML, JavaScript and CSS (Appendix 1, 2 and 3). In addition to a header, footer and introduction, the site is composed of two main sections; an aspatial and spatial section.

Aspatial
Two tables of information are provided in the web interface, one for finds and one for fields (figure 1). The web tables are created by querying the database tables (Fields, Crops, Finds, Class) using SQL via the python script. The results are formatted and passed to the HTML script using Jinga. Where necessary, the text has been formatted (e.g. case-change, date-time) to make it more readable.
Both tables can be independently sorted by clicking any of the column headers, while the rows have been formatted with alternating shades of grey for ease of reading. The tables are fully dynamic, such that if records in the database are updated, added or deleted the tables in the web interface will be updated accordingly.  

Spatial
An interactive map constructed using Scalable Vector Graphics (SVG) has been included. The map represents the overall survey area, overlaid with a grid representing the pre-defined coordinate system, as well as individual finds, fields and their labels (figure 2). 
Each SVG element and text are created based on coordinates stored in the fields and finds database tables. This includes the survey area box, fields and finds, the coordinate grid lines, labels and embedded descriptive feature text. This means that all map elements are fully dynamic and will reflect any future changes to the database tables, including the addition or deletion of new fields and finds.  The SVG elements and text elements are created and formatted via the python script and passed to the HTML script using Jinga.
The embedded descriptive feature text, consisting of information queried from the database, provides users with details about each find and field via a tooltip that appears when an SVG feature is hovered over. This can be useful for quickly reviewing details of a given field or find. 

Each field and find will change colour when hovered over to alert the user to which SCG element is being viewed. Using the buttons beneath the SVG mapping, the finds, fields or coordinate system can be turned on and off.  This can be helpful for users to be able examine each field and find independently of one another.  

The fields and finds have been dynamically labelled according to their unique “id” in the respective database table. The labels can be used to cross-reference the finds and fields on the maps with the table records. The coordinate grid has also been labelled to permit users to locate fields and finds by their respective coordinate combinations.

The fields are colour-coded based on the type of crop being grown. This has been determined through the database query. Finally, an SVG legend has been provided to describe each map feature and to explain which colour represents which crop.

Please note that while the web interface works in all web browsers, some elements, specifically the tooltips, have been optimized to work best in Google Chrome.
