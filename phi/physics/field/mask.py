from phi.geom import union
from .field import *
from .constant import _convert_constant_to_data, _expand_axes


class GeometryMask(Field):

    def __init__(self, name, geometries, value=1.0, flags=(), **kwargs):
        bounds = union(geometries)
        data = _convert_constant_to_data(value)
        Field.__init__(**struct.kwargs(locals(), ignore='value'))

    @struct.prop()
    def geometries(self, geometries):
        return tuple(geometries)

    def sample_at(self, points, collapse_dimensions=True):
        if len(self.geometries) == 0:
            return _expand_axes(math.zeros([1,1]), points, collapse_dimensions=collapse_dimensions)
        if len(self.geometries) == 1:
            result = self.geometries[0].value_at(points)
        else:
            result = math.max([geometry.value_at(points) for geometry in self.geometries], axis=0)
        return result * self.data

    @property
    def rank(self):
        return self.geometries[0].rank

    @property
    def component_count(self):
        return self.data.shape[-1]

    def unstack(self):
        flags = propagate_flags_children(self.flags, self.rank, 1)
        return [GeometryMask('%s[%d]' % (self.name, i), self.geometries, c, flags, batch_size=self._batch_size) for i, c in enumerate(math.unstack(self.data, -1))]

    @property
    def points(self):
        return None

    def compatible(self, other_field):
        return True

    def __repr__(self):
        return 'Union{%s}' % ', '.join([repr(g) for g in self.geometries])


def mask(geometry):
    assert isinstance(geometry, Geometry)
    return GeometryMask('mask', [geometry])


def union_mask(geometries):
    for geom in geometries:
        assert isinstance(geom, Geometry)
    return GeometryMask('union', geometries)
