

class RasterTileManager:

    def __init__(self, layers_config):
        self.spherical_mercator_xmax = 20037508.34
        self.spherical_mercator_ymax = 20037508.34
        self.spherical_mercator_xmin = -20037508.34
        self.spherical_mercator_ymin = -20037508.34
        self.tile_pixels_width = 256
        self.tile_pixels_height = 256

    def tile_sphericalmercator_extent(self, x, y, z):
        row_tiles_at_zoom = self.tiles_per_dimension(z)
        assert 0 <= x <= row_tiles_at_zoom
        assert 0 <= y <= row_tiles_at_zoom
        meters_per_tile_dimension = (self.spherical_mercator_xmax + abs(self.spherical_mercator_xmin))/row_tiles_at_zoom

        # get negative tile indexes for zoom level
        xnegative_index_end = row_tiles_at_zoom/2
        ynegative_index_start = row_tiles_at_zoom/2

        if x <= xnegative_index_end:
            upperleft_tile_cornerx = (x * meters_per_tile_dimension) - self.spherical_mercator_xmax
        else:
            upperleft_tile_cornerx = self.spherical_mercator_xmax - (x * meters_per_tile_dimension)

        if y < ynegative_index_start:
            upperleft_tile_cornery = self.spherical_mercator_ymax - (y * meters_per_tile_dimension)
        else:
            upperleft_tile_cornery = -((y * meters_per_tile_dimension) - self.spherical_mercator_ymax)

        minx = upperleft_tile_cornerx
        miny = upperleft_tile_cornery - meters_per_tile_dimension
        maxx = upperleft_tile_cornerx + meters_per_tile_dimension
        maxy = upperleft_tile_cornery
        return minx, miny, maxx, maxy

    def meters_per_pixel(self, z):
        row_tiles_at_zoom = self.number_of_tiles(z)
        meters_per_tile_row = (self.spherical_mercator_xmax + abs(self.spherical_mercator_xmin))/row_tiles_at_zoom
        result = meters_per_tile_row/self.tile_pixels_width
        return result

    def sphericalmercator_to_pixel(self, xm, ym):

        return xp, yp

    def tiles_per_dimension(self, zoom):
        return 2**zoom

    def number_of_tiles(self, zoom):
        return 2**(2*zoom)




