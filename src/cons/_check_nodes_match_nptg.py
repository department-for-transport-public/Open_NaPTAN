from etl import etl_pipe as etl
from report.reporting import report_failing_nodes
from checks import NaptanCheck

# %%


class NaptanNPTGComparsion(NaptanCheck):
    """[summary] a collection of methods to ensure naptan node data matches the
    nptg data from the server. Issues with the nptg inconsistency affect the
    ability to project and calculate accurate locality, admin area geographies.

    Args:
        NaptanCheck ([type]): [description]
    """

    check_name = "check_naptan nodes_match_nptg_data"
    check_warning_level = "medium"
    check_geographic_level = "stops"

    @classmethod
    @NotImplementedError
    def check_nodes_match_nptg_data(cls, gdf, named_area):
        """[summary] returns a list of admin areas in nptg,
        checks those are in the nodes file, if the nodes file has aac not
        in

        Args:
            gdf ([type]): [the master or named area naptan data file]
            named_area ([type]): [the named area of the naptan subframe]

        Raises:
            NotImplementedError: [description]
            NotImplementedError: [description]
            NotImplementedError: [description]
            NotImplementedError: [description]
            NotImplementedError: [description]
            NotImplementedError: [description]

        Returns:
            [type]: [description]
        """
        #
        check_name = "check_nodes_match_nptg_data"
        # list of all geographic admin areas
        admin_areas = [
            "Aberdeen",
            "Aberdeenshire",
            "Angus",
            "Argyll & Bute",
            "Bath & North East Somerset",
            "Bedford",
            "Blackburn with Darwen",
            "Blackpool",
            "Blaenau Gwent",
            "Bournemouth",
            "Bracknell Forest",
            "Bridgend",
            "Brighton and Hove",
            "Bristol",
            "Buckinghamshire",
            "Caerphilly",
            "Cambridgeshire",
            "Cardiff",
            "Carmarthenshire",
            "Central Bedfordshire",
            "Ceredigion",
            "Cheshire East",
            "Cheshire West & Chester",
            "Clackmannanshire",
            "Conwy",
            "Cornwall",
            "Cumbria",
            "Darlington",
            "Denbighshire",
            "Derby",
            "Derbyshire",
            "Devon",
            "Dorset",
            "Dumfries & Galloway",
            "Dundee",
            "Durham",
            "East Ayrshire",
            "East Dunbartonshire",
            "East Lothian",
            "East Renfrewshire",
            "East Riding of Yorkshire",
            "East Sussex",
            "Edinburgh",
            "Essex",
            "Falkirk",
            "Fife",
            "Flintshire",
            "Glasgow",
            "Gloucestershire",
            "Greater London",
            "Greater Manchester",
            "Gwynedd",
            "Halton",
            "Hampshire",
            "Hartlepool",
            "Herefordshire",
            "Hertfordshire",
            "Highland",
            "Inverclyde",
            "Isle of Anglesey",
            "Isle of Wight",
            "Kent",
            "Kingston upon Hull",
            "Lancashire",
            "Leicester",
            "Leicestershire",
            "Lincolnshire",
            "Luton",
            "Medway",
            "Merseyside",
            "Merthyr Tydfil",
            "Middlesbrough",
            "Midlothian",
            "Milton Keynes",
            "Monmouthshire",
            "Moray",
            "Neath Port Talbot",
            "Newport",
            "Norfolk",
            "North Ayrshire",
            "North East Lincolnshire",
            "North Lanarkshire",
            "North Lincolnshire",
            "North Somerset",
            "North Yorkshire",
            "Northamptonshire",
            "Northumberland",
            "Nottingham",
            "Nottinghamshire",
            "Orkney Islands",
            "Oxfordshire",
            "Pembrokeshire",
            "Perth & Kinross",
            "Peterborough",
            "Plymouth",
            "Poole",
            "Portsmouth",
            "Powys",
            "Reading",
            "Redcar & Cleveland",
            "Renfrewshire",
            "Rhondda Cynon Taff",
            "Rutland",
            "Scottish Borders",
            "Shetland Islands",
            "Shropshire",
            "Slough",
            "Somerset",
            "South Ayrshire",
            "South Gloucestershire",
            "South Lanarkshire",
            "South Yorkshire",
            "Southampton",
            "Southend-on-Sea",
            "Staffordshire",
            "Stirling",
            "Stockton-on-Tees",
            "Stoke-on-Trent",
            "Suffolk",
            "Surrey",
            "Swansea",
            "Swindon",
            "Telford & Wrekin",
            "Thurrock",
            "Torbay",
            "Torfaen",
            "Tyne & Wear",
            "Vale of Glamorgan",
            "Warrington",
            "Warwickshire",
            "West Berkshire",
            "West Dunbartonshire",
            "West Lothian",
            "West Midlands",
            "West Sussex",
            "West Yorkshire",
            "Western Isles",
            "Wiltshire",
            "Windsor & Maidenhead",
            "Wokingham",
            "Worcestershire",
            "Wrexham",
            "York",
        ]

        # TODO get the admin areas from the nodes file, compare against the list of
        # area names
        # nptg values
        adjanct_locals = etl.load_gazette_adjanct_localities()
        admin_codes = etl.naptan_gazette_admin_area_codes()
        districts = etl.naptan_gazette_districts()
        localities = etl.naptan_gazette_localities()
        locality_alternate = etl.load_gazette_localities_alternative_names()
        locality_hierarch = etl.load_gazette_locality_hierarchy()
        plusbusmap = etl.load_gazette_plusbus_mapping()
        plusbuszone = etl.load_gazette_plusbus_zones()
        regions = etl.naptan_gazette_region()

        # node values
        node_locs = gdf["LocalityName"].unique()
        # get nptg localities,
        nptg_locs = localities["LocalityName"].unique()
        # TODO filter to nptg to nodes, get all the localities in nptg for
        #  this area
        # get the unique area code for this admin area.
        area_admin_code = node_locs["AdminCode"].unique()
        # check the area admin code in the nptg file for the corresponding
        #  localities.
        missing_localities = nptg_locs[~nptg_locs.AdminCode.isin(area_admin_code)]
        # check if locality is
        df3 = gaz_locs[gaz_locs.LocalityName.isin(gdf.LocalityName)]
        # get all the localities
        # TODO list the localities in nptg but not nodes

        # TODO plot sample on map
        # TODO write unused localities in given area to file.
        report_failing_nodes(
            gdf,
            check_name,
        )
        return
