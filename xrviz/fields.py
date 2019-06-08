import panel as pn
import xarray as xr
from .sigslot import SigSlot


class Fields(SigSlot):

    def __init__(self, data):
        super().__init__()
        self.set_data(data)
        self.x = pn.widgets.Select(name='x')
        self.y = pn.widgets.Select(name='y')
        self.index_selectors = pn.Column()

        self._register(self.x, 'x')

        self.connect('x', self.change_y)

        self.panel = pn.Row(pn.Column(self.x, self.y),
                            pn.Spacer(width=200),
                            self.index_selectors, name='fields',)

        if isinstance(data, xr.DataArray):
            self.setup(data)

    def set_data(self, data):
        if isinstance(data, xr.Dataset) or isinstance(data, xr.DataArray):
            self.data = data

    def setup(self, var):
        if isinstance(self.data, xr.Dataset):
            self.var = var[0]
            self.var_coords = [coord for coord in self.data[var].coords.keys()]
        else:
            self.var_coords = [coord for coord in self.data.coords.keys()]
        x_opts = self.var_coords.copy()
        self.x.options = x_opts
        self.x.value = x_opts[0]
        y_opts = x_opts.copy()
        del y_opts[0]
        if y_opts is None:
            self.y.options = []
        else:
            self.y.options = y_opts

    def change_y(self, value):
        _opts = self.var_coords.copy()
        values = _opts.copy()
        values.remove(self.x.value)
        if len(values) == 0:
            self.y.options = []
        else:
            self.y.options = values

    @property
    def kwargs(self):
        out = {p.name: p.value for p in self.panel[0]}
        return out
