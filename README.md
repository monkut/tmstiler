tmstiler
========

Map tile utilities supporting python3.

This project supports map tile creation using python3. 
(_and the project serves as a personal study of tile maps_)  

It mimics [TileStache](http://tilestache.org/) in the interface to some degree, but leaves caching to higher levels.

This project contains two classes intended for use in Map Tile generation:
 
    * RasterTileManager
    
    * DjangoRasterTileLayerManager
      
'RasterTileManager' provides helper methods for raster space to spherical mercator conversion.
For transforming spherical mercator (google maps) projected points to tile pixel locations the '.sphericalmercator_to_pixel(zoom, tilex, tiley, xm, ym)' method is available.

'DjangoRasterTileLayerManager' allows you to use data already *binned* and placed in a django model containing a _PointField_, to generate .png tiles.

Sample image created with tiles rendered using the tmstiler's 'DjangoRasterTileLayerManager' in the [safecasttiles](https://github.com/monkut/safecasttiles) project:

![Safecast Data 2014-10](https://lh5.googleusercontent.com/8Uj8wENmgpN0s59mmbKqwced4z2WaxcFGK-fRp3kXas=s259-p-no)

Below is an excerpt of the [safecasttiles](https://github.com/monkut/safecasttiles) project, showing how the 'DjangoRasterTileLayerManager' class can be added in django for tile creation.

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

###Optional:

The following libraries are needed to make use of the 'DjangoRasterTileLayerManager()' class, for generating custom geo binned data from django Models containing a PointField(). (Currently only square bins are supported, but it should be pretty trival to support Polygon objects)

- django: [geodjango] https://www.djangoproject.com/download/ (optional)
- pillow: https://github.com/python-pillow/Pillow (optional)

