class NaptanWarnings():
    """[summary] a class to define what naptan warnings look and behave like.
    """

    def __init__(self, check_name, naptan_record, locality, admin_area):
        self.check_name = check_name
        self.naptan_record == naptan_record
        self.locality = locality
        self.admin_area = admin_area

    @classmethod
    def flag_warning(cls):
        """[summary]
        """

    @classmethod
    def resolve_warning(cls):
        """[summary] resolve the warning for the given naptan error.
        """

    @classmethod
    def suppress_warning(cls):
        """[summary]
        """

    @classmethod
    def print_warnings_to_csv(cls):
        """[summary]
        """


class LowLevelWarning(NaptanWarnings):
    """[summary]
    """


class MedLevelWarning(NaptanWarnings):
    """[summary]
    """


class CriticalLevelWarning(NaptanWarnings):
    """[summary]
    """
