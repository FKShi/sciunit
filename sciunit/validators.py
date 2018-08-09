"""Cerberus validator classes for SciUnit."""

from cerberus import Validator, TypeDefinition
import quantities as pq


def register_type(cls, name):
    """Register `name` as a type to validated as an instance of class `cls`."""
    x = TypeDefinition(name, (cls,), ())
    Validator.types_mapping[name] = x


class ObservationValidator(Validator):
    """Cerberus validator class for observations."""

    def __init__(self, *args, **kwargs):
        """Must pass `test` as a keyword argument.

        Cannot be a positional argument without modifications to cerberus
        """
        try:
            self.test = kwargs['test']
        except AttributeError:
            raise Exception(("Observation validator constructor must have "
                             "a `test` keyword argument"))
        super(ObservationValidator, self).__init__(*args, **kwargs)
        register_type(pq.quantity.Quantity, 'quantity')

    def _validate_units(self, has_units, key, value):
        """Validate fields with `units` key in schema.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if has_units:
            required_units = self.test.units
            if not isinstance(value, pq.quantity.Quantity):
                self._error(key, "Must be a python quantity")
            provided_units = value.simplified.units
            if not isinstance(required_units, pq.Dimensionless):
                required_units = required_units.simplified.units
            if not required_units == provided_units:
                self._error(key,
                            "Must have units of '%s'" % self.test.units.name)
