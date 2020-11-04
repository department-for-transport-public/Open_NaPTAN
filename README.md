
# OpenNaPTAN Check System

A collection of methods for checking the validity of entries into the NaPTAN dataset and displaying NaPTAN geospatial data in an interactive web browser.

# Overview of OpenNaPTAN Check System

The Open NaPTAN is a collection of functions to check the validity of the public NaPTAN dataset made available on the gov.uk platform. The ETL pipeline script, provides data from the [Central NaPTAN Data Source](http://naptan.app.dft.gov.uk/DataRequest/Naptan.ashx?format=csv). Note the
unzipped Naptan dataset is nearly 300mb in size.

This data is extracted in CSV format for ease of processing using Pandas, geopandas and numpy. As well providing the data in a spreadsheet format for inspection in applications such as Excel.

The checks performed on the NaPTAN data are split into two board categories;

1. Internal Data Consistency Checks (con-checks), identifying NaPTAN records
that are not internal consistent with themselves or related NaPTAN nodes.

2. Geospatial Data Checks (geo-checks), identifying issues with the geospatial coordinates, position, and relationships between NaPTAN nodes in a network and other related nodes in the same network.

When the package is run, it will download the NaPTAN data and generate an interactive area map of the given named UK administrative area transport. You can find the named list of all UK administrative area transport authorities below or see the list including ATCO codes on this site: [named specified UK authority area](http://naptan.dft.gov.uk/naptan/smsPrefixes.htm).


The map will include all currently active NaPTAN nodes for that area and a representative sample of 3 years worth of deleted nodes. 

> _*Note:* When first downloading the NaPTAN data, this will use ~600mb.
Administrative area maps vary in size from < 1mb to 30mb (For the Greater London map)._

## Named UK Authorities for Map Generation

* Aberdeen
* Aberdeenshire
* Angus
* Argyll & Bute
* Bath & North East Somerset
* Bedford
* Blackburn with Darwen
* Blackpool
* Blaenau Gwent
* Bournemouth
* Bracknell Forest
* Bridgend
* Brighton and Hove
* Bristol
* Buckinghamshire
* Caerphilly
* Cambridgeshire
* Cardiff
* Carmarthenshire
* Central Bedfordshire
* Ceredigion
* Cheshire East
* Cheshire West & Chester
* Clackmannanshire
* Conwy
* Cornwall
* Cumbria
* Darlington
* Denbighshire
* Derby
* Derbyshire
* Devon
* Dorset
* Dumfries & Galloway
* Dundee
* Durham
* East Ayrshire
* East Dunbartonshire
* East Lothian
* East Renfrewshire
* East Riding of Yorkshire
* East Sussex
* Edinburgh
* Essex
* Falkirk
* Fife
* Flintshire
* Glasgow
* Gloucestershire
* Greater London
* Greater Manchester
* Gwynedd
* Halton
* Hampshire
* Hartlepool
* Herefordshire
* Hertfordshire
* Highland
* Inverclyde
* Isle of Anglesey
* Isle of Wight
* Kent
* Kingston upon Hull
* Lancashire
* Leicester
* Leicestershire
* Lincolnshire
* Luton
* Medway
* Merseyside
* Merthyr Tydfil
* Middlesbrough
* Midlothian
* Milton Keynes
* Monmouthshire
* Moray
* Neath Port Talbot
* Newport
* Norfolk
* North Ayrshire
* North East Lincolnshire
* North Lanarkshire
* North Lincolnshire
* North Somerset
* North Yorkshire
* Northamptonshire
* Northumberland
* Nottingham
* Nottinghamshire
* Orkney Islands
* Oxfordshire
* Pembrokeshire
* Perth & Kinross
* Peterborough
* Plymouth
* Poole
* Portsmouth
* Powys
* Reading
* Redcar & Cleveland
* Renfrewshire
* Rhondda Cynon Taff
* Rutland
* Scottish Borders
* Shetland Islands
* Shropshire
* Slough
* Somerset
* South Ayrshire
* South Gloucestershire
* South Lanarkshire
* South Yorkshire
* Southampton
* Southend-on-Sea
* Staffordshire
* Stirling
* Stockton-on-Tees
* Stoke-on-Trent
* Suffolk
* Surrey
* Swansea
* Swindon
* Telford & Wrekin
* Thurrock
* Torbay
* Torfaen
* Tyne & Wear
* Vale of Glamorgan
* Warrington
* Warwickshire
* West Berkshire
* West Dunbartonshire
* West Lothian
* West Midlands
* West Sussex
* West Yorkshire
* Western Isles
* Wiltshire
* Windsor & Maidenhead
* Wokingham
* Worcestershire
* Wrexham
* York

## Warnings

> _*Note:* Some areas contain a significantly higher number of NaPTAN Stops and therefore
will take significantly longer to load the html interactive map into your browser application._

### Prerequisties

* System level access to install a python application.
* Ability to view HTML files.
* Ability to access csv and interact with csv files.

---

#### Technologies Used

Below is a list of all main packages used throughout the application.

| Library   | Description                                                                         |
| --- | --- |
| Python    | 3.7 - the standard platform for development.                                        |
| Pipenv    | - For package, environment variable management.                                      |
| Pandas    | - Used for management of NaPTAN data, and perform most internal consistency checks. |
| Numpy     | - Used to perform data wrangling and geospatial wrangling.                          |
| Geopandas | - For wrangling NaPTAN data into geospatial formats.                                |
| Shapely   | - For geospatial analysis.                                                          |
| Folium    | - For visualisation of geospatial NaPTAN points.                                    |

#### Environment

Pipenv used for package and dependency management.

### Installation

1. Download the Github zip or the open the code in Github desktop.

2. Install in a directory on your system you have full administrative access.

3. Then update all requirements:
<pre><code>>> pip3 install -r requirements.txt
</code></pre>

4. Run the Command Line Interface (CLI), you can do this by running the main.py file from system terminal or Command Line Interface inside the src working directory.
<pre><code>>> python3 main.py
</code></pre>

> _*Note:* If you are using Ipython or similar to run the code, you will receive an error upon completion indicating an issue with the inspect module. This can be ignored._

5. Enter the named administrative area (only named areas as above are permitted, any other terms will cause the application to fail currently) you want to perform the checks on and require an interactive map.

6. Check your downloads folder for the map and error folders.

7. Open the interactive map in a web browser. The control in the top right  allows the creation of temporary geodesic measurement lines between two given points for NaPTAN stops, or from stops to specific points.

See below for an example image of a NaPTAN area map:

![Example image of a NaPTAN Area Map](/docs/screenshot_finished_map.png)

## Deployment

Cross platform for windows, macosx and linux, should all be supported. If you encounter any issues, please raise an issue request via Github.

## Versioning

![See Changelog for details](/changelog.md)

## Authors

Sam Fowler

Kimberley Brett

Giuseppe Sollazzo

## License

[MIT License](https://github.com/departmentfortransport/NaPTANTools/blob/master/LICENCE.md)

## Acknowledgements
© OpenStreetMap contributors
Open Street Map Data has been used in the development of this product.

Giuseppe Sollazzo

Kian Chapman-Raafat

Kimberley Brett

Reem Al-Jelawi

Tom Soares Mullen
