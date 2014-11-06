#!/usr/bin/env python
"""
DjangoRasterTileLayerManager for django specific raster implementations.
Excepts that for each layer, a django model with a defined Point() field is given.
"""
from .rtm import RasterTileManager

from django.contrib.gis.geos import Polygon, Point
from PIL import Image, ImageDraw


SPHERICAL_MERCATOR_SRID = 3857 # google maps projection

class RequiredConfigMissing(Exception):
    pass

class ObjectMissingExpectedMethod(Exception):
    pass

class DjangoRasterTileLayerManager(RasterTileManager):
    LEGEND_REQUIRED_METHODS = ("get_hsl_color", )
    VALID_POINT_POSITIONS = ("upperleft", "upperright", "lowerleft", "lowerright", "center")
    VALID_WMS_TYPES = ("TMS", )
    LAYER_CONFIG_REQUIRED_KEYS = ("pixel_size", "point_position", "model_queryset", "model_point_fieldname", "model_value_fieldname", "legend_instance")
    LAYER_CONFIG_DEFAULTS = {"model_value_fieldname": "value",
                             "wms_type": "TMS"}

    def __init__(self, layers_config):
        """
        :param layers_config: { <layer name>: {
                                                "pixel_size":<pixel area size in meters>,
                                                "point_position":<pixel position represented by model point>,
                                                "model_queryset": <django model queryset object with model containing point & value fields>,
                                                "model_point_fieldname": <point fieldname>,
                                                "model_value_fieldname": <value fieldname>,
                                                "legend_instance": <legend object instance with 'get_hsl_color()' method, used for defining pixel color>,
                                                 },
                               }
        """
        # check incoming layer config values
        for layer_name, config_values in layers_config.items():
            if not all(required_config in config_values for required_config in self.LAYER_CONFIG_REQUIRED_KEYS):
                raise RequiredConfigMissing("Given layer config missing required values! Expected values: {}".format(self.LAYER_CONFIG_REQUIRED_KEYS))
            assert config_values["point_position"] in self.VALID_POINT_POSITIONS
            if not all(callable(getattr(config_values["legend"], m)) for m in self.LEGEND_REQUIRED_METHODS):
                raise ObjectMissingExpectedMethod("given 'legend' object does not have a defined '{}' method!".format(self.LEGEND_REQUIRED_METHODS))

            # set optional defaults
            for config_fieldname, config_default in self.LAYER_CONFIG_DEFAULTS.items():
                if config_fieldname not in config_values:
                    config_values[config_fieldname] = config_default

        self.layers_config = layers_config

        # initialize base-class variables
        super().__init__()

    def _adjust_point_to_upperleft(self, layername, point_object):
        """
        Adjust point so that it represents the upper-left coord
        :param point_object:
        :return:
        """
        layer_config = self.layers_config[layername]
        point_position = layer_config["point_position"]
        pixel_size = layer_config["pixel_size"]
        x, y = point_object
        if point_position == "upperright":
            x -= pixel_size
        elif point_position == "lowerright":
            x -= pixel_size
            y -= pixel_size
        elif point_position == "lowerleft":
            y -= pixel_size
        elif point_position == "center":
            x -= point_position/2.0
            y -= pixel_size/2.0

        return Point(x, y, srid=point_object.srid)

    def get_tile(self, layername, zoom, tilex, tiley, ignore_cached=False):
        """
        :param zoom: Zoom Level
        :param tilex: tile x value (upper left starts at 0)
        :param tiley: tile y value (upper left starts at 0)
        :param ignore_cached: If True tile is re-rendered
        :return: (<mimetype>, <resulting tile image object>)
        """
        layer_config = self.layers_config[layername]

        # get tile extents in SPHERICAL_MERCATOR_SRID
        # (xmin, ymin, xmax, ymax)
        tile_xmin, tile_ymin, tile_xmax, tile_ymax = self.tile_sphericalmercator_extent(zoom, tilex, tiley)
        tile_bbox = Polygon.from_bbox((tile_xmin, tile_ymin, tile_xmax, tile_ymax))
        tile_bbox.srid = SPHERICAL_MERCATOR_SRID
        # expand tile_bbox by 1/2 pixel to assure edge data is included
        buffered_bbox = tile_bbox.buffer(layer_config["pixel_size"]/2, quadseqs=2)

        # start drawing each block
        tile_image = Image.new("RGBA", (self.tile_pixels_width, self.tile_pixels_height), (255,255,255, 0))
        draw = ImageDraw.Draw(tile_image)

        # get & process pixel data in attached model
        kwargs = {"{}__within".format(layer_config["model_point_fieldname"]): buffered_bbox, }
        pixel_data = layer_config["model_queryset"].objects.filter(**kwargs)
        for pixel in pixel_data:
            hslcolor_str = layer_config["legend_instance"].get_hsl_color(getattr(pixel, layer_config["model_value_fieldname"]))
            model_point = getattr(pixel, layer_config["model_point_fieldname"])
            # pixel x, y expected to be in spherical-mercator
            # attempt to transform, note if srid is not defined this will generate an error
            if model_point.srid != SPHERICAL_MERCATOR_SRID:
                model_point.transform(SPHERICAL_MERCATOR_SRID)

            # adjust to upper-left/nw
            upperleft_point = self._adjust_point_to_upperleft(layername, model_point)
            # (xmin, ymin, xmax, ymax)
            sphericalmercator_bbox = (upperleft_point.x ,
                                      upperleft_point.y - layer_config["pixel_size"],
                                      upperleft_point.x + layer_config["pixel_size"],
                                      upperleft_point.y)
            # transform pixel spherical-mercator coords to image pixel coords
            # --> min values
            xmin, ymin = sphericalmercator_bbox[:2]
            pxmin, pymin = self.sphericalmercator_to_pixel(zoom, tilex, tiley, xmin, ymin)
            # --> max values
            xmax, ymax = sphericalmercator_bbox[2:]
            pxmax, pymax = self.sphericalmercator_to_pixel(zoom, tilex, tiley, xmax, ymax )
            pixel_poly_bbox = Polygon.from_bbox((pxmin, pymin, pxmax, pymax))

            # draw pixel on tile
            draw.polygon(pixel_poly_bbox.coords[0], fill=hslcolor_str)
        return tile_image
