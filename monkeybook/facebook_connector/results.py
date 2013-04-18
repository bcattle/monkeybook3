import datetime
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
            if result_name in fields:
                field = fields[result_name]
                setattr(self, result_name, field.to_python(result_val))
                fields.pop(result_name)

        # Raise an error if an unused field is `required`
        for field in fields:
            if field.required:
                raise BlankFieldError('Field %s is required' % field.orig_name)


class ResultsCollection(list):
    pass

