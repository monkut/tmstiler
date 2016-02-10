from urllib.parse import urlparse


class InvalidCoordinateForZoom(Exception):
    pass


class RasterTileManager:

    def __init__(self):
        # About Spherical Mercator
        # http://docs.openlayers.org/library/spherical_mercator.html
        self.spherical_mercator_xmax = 20037508.34
        self.spherical_mercator_ymax = 20037508.34
        self.spherical_mercator_xmin = -20037508.34
        self.spherical_mercator_ymin = -20037508.34
        self.tile_pixels_width = 256
        self.tile_pixels_height = 256

    def parse_url(self, url):
        """
        Parse out the layername, zoom, x, y and image file format from given URL.
        :param url: url of map server in format: 'http://www.someserver.com/partofurl/layername/zoom/x/y.png'
        :return: layername, x, y, z, tile image format (png/jpg)
        """
        result = urlparse(url)
        layername, z, x, ypart = result.path.rsplit("/", 4)[-4:]
        y, image_format = ypart.split(".")
        return layername, int(z), int(x), int(y), image_format

    def tile_sphericalmercator_extent(self, zoom, tilex, tiley):
        """
        Calculate the given tile's Spherical Mercator extent
        :param zoom: zoom level
        :param tilex: TMS tile X
        :param tiley: TMS tile Y
        :return: Tile's Spherical Mercator extent (minx, miny, maxx, maxy)
        """
        xtiles_at_zoom, ytiles_at_zoom = self.tiles_per_dimension(zoom)
        if not (0 <= tilex <= xtiles_at_zoom):
            msg = 'x({}) not less than expected xtiles_at_zoom({}) for zoom({})!'.format(tilex, xtiles_at_zoom, zoom)
            raise InvalidCoordinateForZoom(msg)
        if not (0 <= tiley <= ytiles_at_zoom):
            msg = 'y({}) not less than expected ytiles_at_zoom({}) for zoom({})!'.format(tiley, ytiles_at_zoom, zoom)
            raise InvalidCoordinateForZoom(msg)
        # note these values are expected to be the same since tiles are squares
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

    def sphericalmercator_to_pixel(self, zoom, tilex, tiley, xm, ym):
        """
        Given a specific zoom & tile location,
        Reproject spherical-mercator value to raster x/y pixel values
        :param zoom: zoom level
        :param tilex: TMS tile X
        :param tiley: TMS tile Y
        :param xm: X in Spherical Mercator (meters)
        :param ym: Y in Spherical Mercator (meters)
        :return: xp, yp (x, y raster pixel coordinates)
        """
        # get tile extents
        tile_minx, tile_miny, tile_maxx, tile_maxy = self.tile_sphericalmercator_extent(zoom, tilex, tiley)

        tile_meters_x_width = tile_maxx - tile_minx
        tile_meters_y_height = tile_maxy - tile_miny
        meters_per_xpixel = tile_meters_x_width/256
        meters_per_ypixel = tile_meters_y_height/256

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
        shifted_xm = xm - tile_minx
        shifted_ym = ym - tile_miny
        # invert y (for raster space)
        inverted_ym = shifted_ym - tile_meters_y_height

        # convert from meters (0 - shifted_max) to pixels (0 - 256)
        xp = shifted_xm / meters_per_xpixel
        yp = abs(inverted_ym / meters_per_ypixel)

        # make sure pixels are in the expected range.
        assert 0 <= xp <= 256
        assert 0 <= yp <= 256

        return int(xp), int(yp)

    def tiles_per_dimension(self, zoom):
        """
        Refer to http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames for details
        :param zoom: Zoom level to calculate row/column numbers for
        :return: number of tile columns(x), rows(y) at zoom level
        """
        tile_count = 2**zoom
        # only support square tiles
        assert self.tile_pixels_height == self.tile_pixels_width
        return tile_count, tile_count

