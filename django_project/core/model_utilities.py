from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class TimeStampedModelMixin(object):
    created = AutoCreatedField('created')
    modified = AutoLastModifiedField('modified')
