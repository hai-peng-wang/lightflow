
class Option:
    """ A single option which is required to run the workflow.

    The option is checked against the provided arguments to the workflow and,
    if available, its provided value is stored in the data store for use within
    the workflow.
    """
    def __init__(self, name, default=None, help=None, type=str):
        """ Initialise the workflow option.

        Args:
            name (str): The name of the option under which the value will be stored.
            default: The default value that should be used when no value is specified.
                     Set to None to make this a non-optional option.
            help (str): A short help string for this option.
            type: The type of the option. Supported types are: str, int, float, bool
        """
        self._name = name
        self._default = default
        self._help = help
        self._type = type

    @property
    def name(self):
        """ Returns the name of the option.

        Returns:
            str: the name of the option.
        """
        return self._name

    @property
    def default(self):
        """ Returns the default value of the option.

        Returns:
            str: the default value of the option
        """
        return self._default

    def convert(self, value):
        """ Converts the specified value to the type of the option.

        Args:
            value: The value that should be converted.

        Returns:
            The value with the type given by the option.
        """
        if self._type is str:
            return str(value)
        elif self._type is int:
            return int(value)
        elif self._type is float:
            return float(value)
        elif self._type is bool:
            return bool(value)
        else:
            return value


class Arguments(list):
    """ A list of options that the workflow requires in order to run. """
    def __init__(self, *args):
        """ Initialises the Arguments list"""
        super().__init__(*args)

    def check_missing(self, args):
        """ Returns the names of all options that are required but were not specified.

        All options that don't have a default value are required in order to run the
        workflow.

        Args:
            args (dict): A dictionary of the provided arguments that is checked for
                         missing options.

        Returns:
            list: A list with the names of the options that are missing from the
                  provided arguments.
        """
        return [opt.name for opt in self
                if (opt.name not in args) and (opt.default is None)]

    def consolidate(self, args):
        """ Consolidate the provided arguments.

        If the provided arguments have matching options, this performs a type conversion.
        For any option that has a default value and is not present in the provided
        arguments, the default value is added.

        Args:
            args (dict): A dictionary of the provided arguments.

        Returns:
            dict: A dictionary with the type converted and with default options enriched
                  arguments.
        """
        result = dict(args)

        for opt in self:
            if opt.name in result:
                result[opt.name] = opt.convert(result[opt.name])
            else:
                if opt.default is not None:
                    result[opt.name] = opt.convert(opt.default)

        return result
