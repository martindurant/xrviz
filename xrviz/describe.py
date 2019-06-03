from jinja2 import Environment, FileSystemLoader
import panel as pn
import os
import sys
import xarray as xr
from .sigslot import SigSlot


class Describe(SigSlot):
    """
    This section describes the property selected in the Display section.

    Parameters
    ----------
    data: `xarray` instance: `DataSet` or `DataArray`
        datset is used to initialize the DataSelector

    Attributes
    ----------
    panel: Displays the generated template

    """
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.panel = pn.pane.HTML(style={'font-size': '12pt'}, width=400,
                                  height=100)
        self.panel.object = "Description Area"
        self._template_load_path = os.path.join(os.path.dirname(__file__),
                                                "templates")
        self._template_env = Environment(loader=FileSystemLoader(self._template_load_path))
        self._variable_template = self._template_env.get_template('variable.html')

    def variable_pane(self, var):
        if var is not None:
            var = var[0]
            self.var_name = self.data[var].name
            var_dtype = str(self.data[var].dtype)
            var_size = self.data[var].size
            var_nbytes = self.data[var].nbytes
            var_dims = self.data[var].dims
            var_coords = [coord for coord in self.data[var].coords]
            var_attrs = [(k, v) for k, v in self.data[var].attrs.items()]

            return self._variable_template.render(var=var,
                                                  var_name=self.var_name,
                                                  var_dtype=var_dtype,
                                                  var_size=var_size,
                                                  var_nbytes=var_nbytes,
                                                  var_dims=var_dims,
                                                  var_coords=var_coords,
                                                  var_attrs=var_attrs,
                                                  )
        else:
            return self._variable_template.render(var=None)

    def setup(self, var):
        self.panel.object = self.variable_pane(var)
