tmstiles
========

Map tile utilities supporting python3.

Previosly, in a number of projectsI had used a Modest Maps & TileStache to produce spatially aggragated data (geo bin) overlays for OSM with leafletjs.
However, in attempting to move more work over to python3, I soon discovered that these libraries do not (yet?) support python3.  For the spatially aggragated data (geo bin),
use case it appeared that it wasn't too much work, so this project was started to allow tile creation functionality.

This project contains two classes which are intended for Map Tile generation, 'RasterTileManager' and 'DjangoRasterTileLayerManager'.
'DjangoRasterTileLayerManager' assumes you have data already *binned* and placed in django model.



Refer to https://github.com/monkut/safecasttiles for a sample implmentation of the 'DjangoRasterTileLayerManager' class.


```
import json
import logging
from collections import OrderedDict
from urllib.parse import urljoin
from io import BytesIO

from django.http import HttpResponse
from django.views.generic import View

from tmstiler.django import DjangoRasterTileLayerManager

from .models import Measurement

SAFECAST_TILELAYER_PREFIX = "/tiles/"  # needs to match urls.py

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Legend:

    def get_color_str(self, value):
        """
        :param value:
        :return:  rgb or hsl color string in the format:

        rgb(255,0,0)
        rgb(100%,0%,0%)

        hsl(hue, saturation%, lightness%)
        where:
            hue is the color given as an angle between 0 and 360 (red=0, green=120, blue=240)
            saturation is a value between 0% and 100% (gray=0%, full color=100%)
            lightness is a value between 0% and 100% (black=0%, normal=50%, white=100%).

        For example, hsl(0,100%,50%) is pure red.
        """
        max_value = 3.99
        min_value = 0.03
        full_range = max_value - min_value
        max_h = 61
        min_h = 246
        color_range = min_h - max_h
        value_percentage = (value - min_value)/full_range
        h = int(color_range - (value_percentage * color_range))
        return "hsl({}, 100%, 50%)".format(h)


class SafecastMeasurementsTileView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create per month layers
        months = Measurement.objects.order_by("date").values_list('date', flat=True).distinct()
        layers = OrderedDict()
        legend = Legend()
        for m in months:
            qs = Measurement.objects.filter(date=m)
            month_layername = m.strftime("%Y%m")
            layers[month_layername] = {
                        "pixel_size": 1500,  # size of bin in meters
                        "point_position": "upperleft",
                        "model_queryset": qs,
                        "model_point_fieldname": "location",
                        "model_value_fieldname": "value",
                        "legend_instance": legend,  # returns a hslcolor_str
                        }
        self.tilemgr = DjangoRasterTileLayerManager(layers)

    def get(self, request):
        layername, zoom, x, y, image_format = self.tilemgr.parse_url(request.path)
        logger.info("layername({}) zoom({}) x({}) y({}) image_format({})".format(layername, zoom, x, y, image_format))
        mimetype, tile_pil_img_object = self.tilemgr.get_tile(layername, zoom, x, y)
        image_encoding = image_format.replace(".", "")
        image_fileio = BytesIO()
        tile_pil_img_object.save(image_fileio, image_encoding)
        image_fileio.seek(0)
        return HttpResponse(image_fileio, content_type=mimetype)
```


