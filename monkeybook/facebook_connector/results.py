import datetime, collections
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
    def __init__(self, result):
        # Find all fields
        fields = {}
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, ResultField):
                fields[name] = attr

        # Assign the incoming dict to fields
        for result_name, result_val in result.items():
            if result_name in fields \
                and result_val is not None and result_val != '':
                field = fields[result_name]
                setattr(self, result_name, field.to_python(result_val))
                fields.pop(result_name)

        # Raise an error if an unused field is `required`
        for name, field in fields.items():
            if field.required:
                raise BlankFieldError('Field %s is required. Result was "%s"' % (name, result))
            else:
                setattr(self, name, None)


class ResultsCollection(list):
    _field_indices = {}

    def get_by_field(self, field_name, value, unique_key=True):
        """
        Allows the collection to be indexed by any
        of its fields, returns all values that match.
        Mappings are created lazily

        If `unique_key` is True, it is assumed that all values
        in the collection have a unique value of the field

        If False, the collection is searched for multiple matching
        values of the field in question (slower)
        """
        if not len(self):
            raise IndexError('get_by_field() called before the collection has any values')

        assert hasattr(self[0], field_name)

        if field_name not in self._field_indices:
            if unique_key:
                self._field_indices[field_name] = {
                    getattr(item, field_name): item
                    for item in self
                }
            else:
                self._field_indices[field_name] = collections.defaultdict(list)
                for element in self:
                    key = getattr(element, field_name)
                    self._field_indices[field_name][key].append(element)

        return self._field_indices[field_name][value]
