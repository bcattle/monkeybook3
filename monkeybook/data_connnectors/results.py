import datetime, copy
from collections import defaultdict
from pytz import utc


class BlankFieldError(Exception):
  pass


class ResultField(object):
  def __init__(self, required=False):
    """
    If a `required` field is not recieved from facebook,
    we raise an exception
    """
    self.val = None
    self.required = required

  def to_python(self, value):
    return value


class IntegerField(ResultField):
  def to_python(self, value):
    return int(value)       # fail loudly


class TimestampField(ResultField):
  def to_python(self, value):
    return datetime.datetime.utcfromtimestamp(float(value)).replace(tzinfo=utc)


class ConnectorResult(object):
  def _get_fields(self):
    fields = {}
    for name, attr in self.__class__.__dict__.items():
      if isinstance(attr, ResultField):
        fields[name] = attr
    return fields


  def _assign_values(self, fields, result):
    # Assign the incoming dict to fields
    for result_name, result_val in result.items():
      if result_name in fields:
        if result_val is not None and result_val != '':
          field = fields[result_name]
          setattr(self, result_name, field.to_python(result_val))
          fields.pop(result_name)
      else:
        raise AttributeError('Attempted to set value of field %s not defined in class' % result_name)


  def _check_required_fields(self, fields, err_data=None):
    err_data = err_data or ''
    for name, field in fields.items():
      if field.required:
        raise BlankFieldError('Field %s is required. Input was "%s"' % (name, err_data))
      else:
        setattr(self, name, None)


  def __init__(self, result=None, base=None, **kwargs):
    """
    Builds a ConnectorResult.
    `result` is a dict of fields, e.g. in from fb

    This can also take an existing ConnectorResult and
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
    self._check_required_fields(fields, result)


class ResultsCollection(list):
  def __init__(self, *args, **kwargs):
    self._field_indices = {}
    super(ResultsCollection, self).__init__(*args, **kwargs)
    
    # Signals is a sparse mapping of friend/photo/comment ids to a value
    # For example
    # signals['friend_value'][friend1_id] = .75
    # signals['friend_value'][friend2_id] = .5
    # signals['friend_value'][friend3_id] = .9
    # I can now easily slice and dice this structure to get the top friends
    self.signals = defaultdict(lambda: defaultdict(int))
    

  def _make_mapping_by_field(self, field_name):
    self._field_indices[field_name] = defaultdict(list)
    for element in self:
      key = getattr(element, field_name)
      self._field_indices[field_name][key].append(element)


  def _scalar(self, field_name):
    """
    Returns a set of all values of one field
    """
    values = [getattr(result, field_name) for result in self]
    return values

  def get_sorted_by_signal(self, signal, min_value=None, 
                           max_elements=None, reverse=True, id_only=False):
    values = [(k, v) for k, v in self.signals[signal].iteritems() 
              if min_value is None or v > min_value]
    values.sort(key=lambda x: x[1], reverse=reverse)
    if id_only:
      values = [k for k, v in values]
    return values[:max_elements]
    
    
  def get_by_id(self, id):
    return self.get_by_field('id', id)[0]
  
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
      self._make_mapping_by_field(field_name)

    return self._field_indices[field_name][value]


  def merge_no_duplicates(self, id_field, new_results):
    """
    Merges into this list,
    discarding any that are duplicate
    by keying on the specified field
    """
    keys = set(self._scalar(id_field))
    for result in new_results:
      if getattr(result, id_field) not in keys:
        self.append(result)
    # Cache invalidation
    self._field_indices = {}
