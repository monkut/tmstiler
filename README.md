tmstiler
========

Map tile utilities supporting python3.

In a number of projects I used Modest Maps & TileStache to produce spatially aggragated data (geo bin) overlays for OSM with leafletjs.

However, in attempting to move more work over to python3, I soon discovered that these libraries do not (yet?) support python3.  For the spatially aggragated data (geo bin)
use case, it appeared that it wasn't too much work, so this project was started to support the use-case for tile creation in python3 (_and the project serves as a personal study of tile maps_).  It mimics TileStache in the interface to some degree, but leaves cacheing to higher levels.

This project contains two classes which are intended for Map Tile generation, 'RasterTileManager' and 'DjangoRasterTileLayerManager'.
'DjangoRasterTileLayerManager' assumes you have data already *binned* and placed in a django model containing a _PointField_.

Sample image created with tiles rendered using the tmstiler's 'DjangoRasterTileLayerManager' in the [safecasttiles](https://github.com/monkut/safecasttiles) project:

![Safecast Data 2014-10](https://lh5.googleusercontent.com/8Uj8wENmgpN0s59mmbKqwced4z2WaxcFGK-fRp3kXas=s259-p-no)

Below is an excerpt of the [safecasttiles](https://github.com/monkut/safecasttiles) showing how the 'DjangoRasterTileLayerManager' class can be added in django for tile creation.

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

##Dependencies

###Required:

The 'RasterTileManager()' class uses the builtin python3 libraries.  It contains the basic methods needed for performing the calculations necessary for building individual TMS map tiles.  (To create the actual tile image files, pillow (PIL) is required, see below.)

- None

###Optional:

The following libraries are needed to make use of the 'DjangoRasterTileLayerManager()' class, for generating custom geo binned data from django Models containing a PointField(). (Currently only square bins are supported, but it should be pretty trival to support Polygon objects)

- django: [geodjango] https://www.djangoproject.com/download/ (optional)
- pillow: https://github.com/python-pillow/Pillow (optional)

