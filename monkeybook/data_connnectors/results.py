import datetime, collections, copy
from pytz import utc


class BlankFieldError(Exception):
    pass


class ResultField(object):
    val = None

    def __init__(self, required=False):
        """
        If a `required` field is not recieved from facebook,
        we raise an exception
        """
        self.required = required

    def to_python(self, value):
        return value


class IntegerField(ResultField):
    def to_python(self, value):
        return int(value)           # fail loudly


class TimestampField(ResultField):
    def to_python(self, value):
        return datetime.datetime.utcfromtimestamp(float(value)).replace(tzinfo=utc)


class ResourceResult(object):
    _fields = None

    def _get_fields(self):
        fields = {}
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, ResultField):
                fields[name] = attr
        return fields


    def _assign_values(self, fields, result):
        # Assign the incoming dict to fields
        for result_name, result_val in result.items():
            if result_name in fields \
                and result_val is not None and result_val != '':
                field = fields[result_name]
                setattr(self, result_name, field.to_python(result_val))
                fields.pop(result_name)


    def _check_required_fields(self, err_data=None):
        err_data = err_data or ''
        for name, field in self._fields.items():
            if field.required:
                raise BlankFieldError('Field %s is required. Input was "%s"' % (name, err_data))
            else:
                setattr(self, name, None)


    def __init__(self, result=None, base=None, **kwargs):
        """
        Builds a ResourceResult.
        `result` is a dict of fields, e.g. in from fb

        This can also take an existing ResourceResult and
        extend it by adding additional fields.

        `kwargs` are the values of the new fields
        """
        # Find all fields
        self._fields = self._get_fields()
        fields = copy.copy(self._fields)

        # Assign the fields from the base instance, if any
        if base:
            for field in base._fields:
                setattr(self, field, getattr(base, field, None))

        # Assign fields defined in this class
        if result:
            self._assign_values(fields, result)
        self._assign_values(fields, kwargs)

        # Raise an error if an unused field is `required`
        self._check_required_fields()


class ResultsCollection(list):
    _field_indices = {}

    def get_by_field(self, field_name, value):
        """
        Allows the collection to be indexed by any
        of its fields, returns all values that match.
        Mappings are created lazily
        """
        if not len(self):
            raise IndexError('get_by_field() called before the collection has any values')

        assert hasattr(self[0], field_name)

        if field_name not in self._field_indices:
            self._field_indices[field_name] = collections.defaultdict(list)
            for element in self:
                key = getattr(element, field_name)
                self._field_indices[field_name][key].append(element)

        return self._field_indices[field_name][value]
