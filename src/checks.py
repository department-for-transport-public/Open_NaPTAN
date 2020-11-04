import sys


class NaptanCheck():
    """[summary] the class to describe all naptan checks,
    contains all recurring attributes and methods.
    """

    def __init__(self, naptan_master_gdf, check_name,
                 check_warning_level, check_geographic_level):
        self.naptan_gdf = naptan_master_gdf
        self.check_name = check_name
        # low, medium, high, critical, na
        self.check_warning_level = check_warning_level
        # 'stop', 'stop area', 'locality', 'administrative area', 'region'
        self.check_geographic_level = check_geographic_level

    @classmethod
    def filter_bus_stops(cls, gdf):
        """[summary] takes a naptan frame and returns just the request bus stops
        types into their own dataframe.

        Args:
            gdf ([type]): [description]

        Returns:
            gdf_busstops: [description]
        """

        bus_stop_types = ['BCS', 'BCT', 'BCQ']
        # check it's a valid bus stop type.
        try:
            # multi value filter for bus stop types.
            gdf_busstops = gdf[gdf['StopType'].isin(bus_stop_types)]
            # report processing.
            print(gdf_busstops.StopType.unique())
            print(gdf_busstops.AreaName.iloc[0])
            print(gdf.shape[0] - gdf_busstops.shape[0])
            return gdf_busstops
        except Exception as e:
            print(
                f'Invalid bus stop type {e} from {gdf.AreaName.iloc[0]}')

    def naptan_geodataframe(self):
        """[summary] check it's a valid geodataframe being passed to the check.

        Returns:
            [type]: [description]
        """
        gdf = self.naptan_gdf
        # TODO - make some checks.
        return gdf

    def check_name(self):
        """[summary] checks if the name is one of the permitted tests.

        Returns:
            [type]: [description]
        """
        check_name = self.check_name
        # fix cases
        names = map(lambda x: x.lower(), ['check illegal characters'])
        if check_name.lower() in str(names):
            return check_name
        else:
            sys.exit(f'{check_name} is not a valid naptan check name.')

    def check_severity_level(self):
        """[summary] make sure the severity level is a valid entry.
        """
        severity_level = self.check_warning_level
        # check if given level is in the levels lists.
        levels = map(lambda x: x.lower(), [
                     'low', 'medium', 'high', 'critical', 'na'])
        if severity_level.lower() in str(levels):
            return severity_level
        else:
            sys.exit(f'{severity_level} is not valid.')

    def check_geographic_level(self):
        """[summary] checks that the test is being run on the correct
        geographic area level.
        """
        geo_level = self.check_geographic_level
        geo_levels = map(lambda x: x.lower(), ['stop', 'stop area', 'locality',
                                               'administrative area', 'region',
                                               'national'])
        if geo_level.lower() in str(geo_levels):
            return geo_level
        else:
            sys.exit(f'{geo_level} is not valid for this check type.')
