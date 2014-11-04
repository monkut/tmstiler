from urllib.parse import urlparse


class InvalidCoordinateForZoom(Exception):
    pass


class RasterTileManager:

    def __init__(self):
        self.spherical_mercator_xmax = 20037508.34
        self.spherical_mercator_ymax = 20037508.34
        self.spherical_mercator_xmin = -20037508.34
        self.spherical_mercator_ymin = -20037508.34
        self.tile_pixels_width = 256
        self.tile_pixels_height = 256

    def parse_url(self, url):
        """
        :param url: url of map server in format: 'http://www.someserver.com/partofurl/layername/zoom/x/y.png'
        :return: layername, x, y, z, tile image format (png/jpg)
        """
        result = urlparse(url)
        layername, z, x, ypart = result.path.rsplit("/", 4)[-4:]
        y, image_format = ypart.split(".")
        return layername, z, x, y, image_format

    def tile_sphericalmercator_extent(self, zoom, tilex, tiley):
        xtiles_at_zoom, ytiles_at_zoom = self.tiles_per_dimension(zoom)
        if not (0 <= tilex <= xtiles_at_zoom):
            raise InvalidCoordinateForZoom("x({}) not less than expected xtiles_at_zoom({}) for zoom({})!".format(tilex, xtiles_at_zoom, zoom))
        if not (0 <= tiley <= ytiles_at_zoom):
            raise InvalidCoordinateForZoom("y({}) not less than expected ytiles_at_zoom({}) for zoom({})!".format(tiley, ytiles_at_zoom, zoom))
        # note this values are expected to be the same since tiles are squares
        meters_per_xtile_dimension = (self.spherical_mercator_xmax + abs(self.spherical_mercator_xmin))/xtiles_at_zoom
        meters_per_ytile_dimension = (self.spherical_mercator_ymax + abs(self.spherical_mercator_ymin))/ytiles_at_zoom
        assert meters_per_xtile_dimension == meters_per_ytile_dimension

        lowerleft_tile_cornerx = (tilex * meters_per_xtile_dimension) - self.spherical_mercator_xmax
        lowerleft_tile_cornery = (tiley * meters_per_ytile_dimension) - self.spherical_mercator_ymax

        minx = lowerleft_tile_cornerx
        miny = lowerleft_tile_cornery
        maxx = lowerleft_tile_cornerx + meters_per_xtile_dimension
        maxy = lowerleft_tile_cornery + meters_per_ytile_dimension
        return minx, miny, maxx, maxy

    def sphericalmercator_to_pixel(self, tile_url, xm, ym):
        """
        Given a specific tile_url, shift origin to raster/pixel space
        Reproject from spherical-mercator to raster x/y values
        :param xm:
        :param ym:
        :return:
        """
        layername, zoom, tilex, tiley, image_format = self.parse_url(tile_url)

        # get tile extents
        tile_minx, tile_miny, tile_maxx, tile_maxy = self.tile_sphericalmercator_extent(zoom, tilex, tiley)

        tile_meters_origin_shift_x = tile_maxx - tile_minx
        tile_meters_origin_shift_y = tile_maxy - tile_miny

        # adjust xm & ym to max/min values, if they exceed the given tile
        if xm > tile_maxx:
            xm = tile_maxx
        elif xm < tile_minx:
            xm = tile_minx
        if ym > tile_maxy:
            ym = tile_maxy
        elif ym < tile_miny:
            ym = tile_miny

        # shift sphereical-mercator origin to zero start from lower-left
        # --> shifts so lower right is 0,0
        # --> NOTE: value still in meters
        shifted_xm = xm - tile_meters_origin_shift_x
        shifted_ym = ym - tile_meters_origin_shift_y
        shifted_ymax = tile_maxy - tile_meters_origin_shift_y
        shifted_xmax = tile_maxx - tile_meters_origin_shift_x

        # convert from meters (0 - shifted_max) to pixels (0 - 256)
        xp = (shifted_xm * 256) / shifted_xmax
        yp = (shifted_ym * 256) / shifted_ymax
        # invert y (for raster space)
        yp = self.tile_pixels_height - yp

        return xp, yp

    def tiles_per_dimension(self, zoom):
        tile_count = 2**zoom
        # only support square tiles
        assert self.tile_pixels_height == self.tile_pixels_width
        return tile_count, tile_count

    def tiles_at_zoomlevel(self, zoom):
        return 2**(2*zoom)




