class BlankFieldError(Exception):
    pass


class ResultField(object):
    val = None

    def __init__(self, name=None, required=False, default=None):
        """
          `name`: the name of the field in the results dict,
          e.g. from facebook
        """
        self.name = name
        self.required = required
        self.default = default

    def set_val(self, val):
        self.val = val


class ResourceResult(object):
    def _set_field(self, field, value):
        setattr(self, field.orig_name, value)

    def __init__(self, result):
        # Find all fields
        fields = {}
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, ResultField):
                attr.orig_name = name
                # We lookup the field by "facebook name"
                if attr.name is not None:
                    fields[attr.name] = attr
                else:
                    fields[name] = attr

        # Assign the incoming dict to fields
        for result_name, result_val in result.items():
            if result_name in fields:
                self._set_field(fields[result_name], result_val)
                fields.pop(result_name)

        # Assign any blank fields to their default val
        for field in fields:
            if field.default is not None:
                self._set_field(field, field.default)

        # Raise an error if an unused field is `required`
        for field in fields:
            if field.required:
                raise BlankFieldError('Field %s is required' % field.orig_name)


class ResultsCollection(list):
    pass

