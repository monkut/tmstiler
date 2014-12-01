tmstiles
========

Map tile utilities supporting python3.

Previosly, in a number of projects I had used Modest Maps & TileStache to produce spatially aggragated data (geo bin) overlays for OSM with leafletjs.
However, in attempting to move more work over to python3, I soon discovered that these libraries do not (yet?) support python3.  For the spatially aggragated data (geo bin),
use case it appeared that it wasn't too much work, so this project was started to support the use-case for tile creation.  It mimics TileStache in the interface to some degree, but leaves cacheing to higher levels.

This project contains two classes which are intended for Map Tile generation, 'RasterTileManager' and 'DjangoRasterTileLayerManager'.
'DjangoRasterTileLayerManager' assumes you have data already *binned* and placed in django model.



Below is an excerpt of the https://github.com/monkut/safecasttiles project showing how the 'DjangoRasterTileLayerManager' class can be added in django for tile creation.

NOTE:  'DjangoRasterTileLayerManager' requires pillow and django.  ('RasterTileManager' alone has no additional dependencies)


```python
from io import BytesIO

from django.http import HttpResponse
from django.views.generic import View

from tmstiler.django import DjangoRasterTileLayerManager

from .models import Measurement


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
        mimetype, tile_pil_img_object = self.tilemgr.get_tile(layername, zoom, x, y)
        image_encoding = image_format.replace(".", "")  # change ".png" to just "png"
        # pillow img.tobytes() doesn't seem to work, workaround to serve raw bytes via BytesIO()
        image_fileio = BytesIO()  
        tile_pil_img_object.save(image_fileio, image_encoding)
        image_fileio.seek(0)
        return HttpResponse(image_fileio, content_type=mimetype)
```


