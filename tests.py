import unittest
import datetime

from PIL import Image, ImageDraw

from tmstiler.rtm import RasterTileManager


SPHERICAL_MERCATOR_SRID = 3857  # google maps projection


class Point:

    def __init__(self, x, y, srid=SPHERICAL_MERCATOR_SRID):
        self.x = x
        self.y = y
        self.srid = srid


class DummyMeasurement:

    def __init__(self, location, date, counts, value):
        self.location = location
        self.date = date
        self.counts = counts
        self.value = value


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
        return "hsl(0,100%,50%)"  # pure red for now...


class TestRasterTileManager(unittest.TestCase):

    def test_tile_sphericalmercator_extent_munich_z8(self):
        """
        Test upper-right coord
        """
        # Munich (sphericl mercator)
        # 11.5804, 48.1394
        # x = 1289124.2311824248
        # y = 6130077.43992735
        z = 8
        tilex = 136
        tiley = 167

        rtm = RasterTileManager()
        # expected results taken from:
        # http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
        expected_extent = (1252344.271424327, 6105178.323193599, 1408887.3053523675, 6261721.357121639)
        actual_extent = rtm.tile_sphericalmercator_extent(z, tilex, tiley)
        coord_type = {0:"xmin", 1: "ymin", 2: "xmax", 3: "ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                                                     round(actual, 2),
                                                                                     coord_type[idx],
                                                                                     round(expected, 2),
                                                                                     rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax,
                                                                     rtm.spherical_mercator_ymax)
            msg += "\nzoom: {}".format(z)
            msg += "\ntilex: {}".format(tilex)
            msg += "\ntiley: {}".format(tiley)
            msg += "\nactual extents:   {}".format(actual_extent)
            msg += "\nexpected extents: {}".format(expected_extent)
            self.assertTrue(round(actual, 2) == round(expected, 2), msg)

    def test_tile_sphericalmercator_extent_sydney_z5(self):
        """
        Test lower-right coord
        """
        # Sydney (spherical mercator)
        z = 5
        tilex = 29
        tiley = 12

        rtm = RasterTileManager()
        # expected results taken from:
        # http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
        expected_extent = (16280475.528516259, -5009377.085697312, 17532819.79994059, -3757032.814272983)
        actual_extent = rtm.tile_sphericalmercator_extent(z, tilex, tiley)
        coord_type = {0:"xmin", 1: "ymin", 2: "xmax", 3: "ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                                                     round(actual, 2),
                                                                                     coord_type[idx],
                                                                                     round(expected, 2),
                                                                                     rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax,
                                                                     rtm.spherical_mercator_ymax)
            msg += "\nzoom: {}".format(z)
            msg += "\ntilex: {}".format(tilex)
            msg += "\ntiley: {}".format(tiley)
            msg += "\nactual extents:   {}".format(actual_extent)
            msg += "\nexpected extents: {}".format(expected_extent)
            self.assertTrue(round(actual, 2) == round(expected, 2), msg)

    def test_tile_sphericalmercator_extent_santiago_z7(self):
        """
        Test lower-left coord
        """
        z = 7
        tilex = 38
        tiley = 51

        rtm = RasterTileManager()
        # expected results taken from:
        # http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
        expected_extent = (-8140237.7642581295, -4070118.8821290657, -7827151.696402049, -3757032.814272983)
        actual_extent = rtm.tile_sphericalmercator_extent(z, tilex, tiley)
        coord_type = {0: "xmin", 1: "ymin", 2: "xmax", 3: "ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                                                     round(actual, 1),
                                                                                     coord_type[idx],
                                                                                     round(expected, 1),
                                                                                     rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax,
                                                                     rtm.spherical_mercator_ymax)
            msg += "\nzoom: {}".format(z)
            msg += "\ntilex: {}".format(tilex)
            msg += "\ntiley: {}".format(tiley)
            msg += "\nactual extents:   {}".format(actual_extent)
            msg += "\nexpected extents: {}".format(expected_extent)
            self.assertTrue(round(actual, 1) == round(expected, 1), msg)

    def test_tile_sphericalmercator_extent_chicago_z6(self):
        """
        Test upper-left coord
        """
        z = 6
        tilex = 16
        tiley = 40

        rtm = RasterTileManager()
        # expected results taken from:
        # http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
        expected_extent = (-10018754.171394622, 5009377.085697312, -9392582.035682458, 5635549.221409474)
        actual_extent = rtm.tile_sphericalmercator_extent(z, tilex, tiley)
        coord_type = {0:"xmin", 1: "ymin", 2: "xmax", 3: "ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                                                     round(actual, 1),
                                                                                     coord_type[idx],
                                                                                     round(expected, 1),
                                                                                     rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax,
                                                                     rtm.spherical_mercator_ymax)
            msg += "\nzoom: {}".format(z)
            msg += "\ntilex: {}".format(tilex)
            msg += "\ntiley: {}".format(tiley)
            msg += "\nactual extents:   {}".format(actual_extent)
            msg += "\nexpected extents: {}".format(expected_extent)
            self.assertTrue(round(actual, 1) == round(expected, 1), msg)

    def test_tile_sphericalmercator_extent_fukushima_z10(self):
        z = 10
        tilex = 911
        tiley = 626

        rtm = RasterTileManager()
        expected_extent = (15615167.634322088, 4461476.466949169, 15654303.392804097, 4500612.225431178)
        actual_extent = rtm.tile_sphericalmercator_extent(z, tilex, tiley)
        coord_type = {0: "xmin", 1: "ymin", 2: "xmax", 3: "ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                                                     round(actual, 1),
                                                                                     coord_type[idx],
                                                                                     round(expected, 1),
                                                                                     rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax,
                                                                     rtm.spherical_mercator_ymax)
            msg += "\nzoom: {}".format(z)
            msg += "\ntilex: {}".format(tilex)
            msg += "\ntiley: {}".format(tiley)
            msg += "\nactual extents:   {}".format(actual_extent)
            msg += "\nexpected extents: {}".format(expected_extent)
            self.assertTrue(round(actual, 1) == round(expected, 1), msg)

    def test_sphericalmercator_to_pixel_japan(self):
        pixel_size_meters = 250
        tile_pixel_size = 256
        zoom = 10
        tilex = 911
        tiley = 626
        rtmgr = RasterTileManager()
        tile_extent = rtmgr.tile_sphericalmercator_extent(zoom, tilex, tiley)

        # create dummy data in extent
        upperleft_x = tile_extent[0]  # minx
        upperleft_y = tile_extent[3]  # maxy

        # create measurement instances for the left half of the tile
        # --> get the x halfway point
        xmin = tile_extent[0]  # minx
        xmax = tile_extent[2]  # maxx
        ymin = tile_extent[1]  # miny
        tile_width = xmax - xmin
        half_tile_width = tile_width/2
        halfx = xmin + half_tile_width

        # create DummyMeasurement() objects for half of the tile
        d = datetime.date(2014, 11, 28)
        x = upperleft_x
        created_measurement_count = 0
        temp_measurements = []
        while x <= halfx:
            y = upperleft_y
            while y >= ymin:
                point = Point(x, y, srid=SPHERICAL_MERCATOR_SRID)
                m = DummyMeasurement(location=point,
                                     date=d,
                                     counts=50,
                                     value=1)
                temp_measurements.append(m)
                created_measurement_count += 1
                y -= pixel_size_meters
            x += pixel_size_meters

        # create tile image from data
        tile_image = Image.new("RGBA",
                               (tile_pixel_size, tile_pixel_size),
                               (255, 255, 255, 0))
        draw = ImageDraw.Draw(tile_image)
        legend = Legend()
        processed_pixel_count = 0
        for pixel in temp_measurements:
            color_str = legend.get_color_str(pixel.value)
            self.assertTrue(color_str == "hsl(0,100%,50%)")

            # pixel x, y expected to be in spherical-mercator
            # attempt to transform, note if srid is not defined this will generate an error
            if pixel.location.srid != SPHERICAL_MERCATOR_SRID:
                pixel.location.transform(SPHERICAL_MERCATOR_SRID)

            # adjust to upper-left/nw
            upperleft_point = pixel.location
            # (xmin, ymin, xmax, ymax)
            sphericalmercator_bbox = (upperleft_point.x,
                                      upperleft_point.y - pixel_size_meters,
                                      upperleft_point.x + pixel_size_meters,
                                      upperleft_point.y)
            # transform pixel spherical-mercator coords to image pixel coords
            # --> min values
            xmin, ymin = sphericalmercator_bbox[:2]
            pxmin, pymin = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmin, ymin)

            # --> max values
            xmax, ymax = sphericalmercator_bbox[2:]
            pxmax, pymax = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmax, ymax )
            upperleft_point = (pxmin, pymax)
            upperright_point = (pxmax, pymax)
            lowerright_point = (pxmax, pymin)
            lowerleft_point = (pxmin, pymin)
            coords = (upperleft_point, upperright_point, lowerright_point, lowerleft_point, upperleft_point)

            # draw pixel on tile
            draw.polygon(coords, fill=color_str)
            processed_pixel_count += 1

        # confirm that half of image is red
        # --> get percentage of image that is red.
        color_counts = tile_image.getcolors()  #
        red = (255, 0, 0, 255)
        red_percentage = sum(count for count, color in color_counts if color == red)/sum(count for count, _ in color_counts)
        self.assertTrue(red_percentage >= 0.48, "Resulting Tile image Red({}) < 0.48".format(round(red_percentage, 4)))

    def test_sphericalmercator_to_pixel_chicago(self):
        pixel_size_meters = 2500
        tile_pixel_size = 256
        zoom = 6
        tilex = 16
        tiley = 40
        rtmgr = RasterTileManager()
        tile_extent = rtmgr.tile_sphericalmercator_extent(zoom, tilex, tiley)

        # create dummy data in extent
        upperleft_x = tile_extent[0]  # minx
        upperleft_y = tile_extent[3]  # maxy

        # create measurement instances for the left half of the tile
        # --> get the x halfway point
        xmin = tile_extent[0]  # minx
        xmax = tile_extent[2]  # maxx
        ymin = tile_extent[1]  # miny
        tile_width = xmax - xmin
        half_tile_width = tile_width/2
        halfx = xmin + half_tile_width

        # create DummyMeasurement() objects for half of the tile
        d = datetime.date(2014, 11, 28)
        x = upperleft_x
        created_measurement_count = 0
        temp_measurements = []
        while x <= halfx:
            y = upperleft_y
            while y >= ymin:
                point = Point(x, y, srid=SPHERICAL_MERCATOR_SRID)
                m = DummyMeasurement(location=point,
                                     date=d,
                                     counts=50,
                                     value=1)
                temp_measurements.append(m)
                created_measurement_count += 1
                y -= pixel_size_meters
            x += pixel_size_meters

        # create tile image from data
        tile_image = Image.new("RGBA", (tile_pixel_size, tile_pixel_size), (255,255,255, 0))
        draw = ImageDraw.Draw(tile_image)
        legend = Legend()
        processed_pixel_count = 0
        for pixel in temp_measurements:
            color_str = legend.get_color_str(pixel.value)
            self.assertTrue(color_str == "hsl(0,100%,50%)")

            # pixel x, y expected to be in spherical-mercator
            # attempt to transform, note if srid is not defined this will generate an error
            if pixel.location.srid != SPHERICAL_MERCATOR_SRID:
                pixel.location.transform(SPHERICAL_MERCATOR_SRID)

            # adjust to upper-left/nw
            upperleft_point = pixel.location
            # (xmin, ymin, xmax, ymax)
            sphericalmercator_bbox = (upperleft_point.x ,
                                      upperleft_point.y - pixel_size_meters,
                                      upperleft_point.x + pixel_size_meters,
                                      upperleft_point.y)
            # transform pixel spherical-mercator coords to image pixel coords
            # --> min values
            xmin, ymin = sphericalmercator_bbox[:2]
            pxmin, pymin = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmin, ymin)

            # --> max values
            xmax, ymax = sphericalmercator_bbox[2:]
            pxmax, pymax = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmax, ymax )
            upperleft_point = (pxmin, pymax)
            upperright_point = (pxmax, pymax)
            lowerright_point = (pxmax, pymin)
            lowerleft_point = (pxmin, pymin)
            coords = (upperleft_point, upperright_point, lowerright_point, lowerleft_point, upperleft_point)

            # draw pixel on tile
            draw.polygon(coords, fill=color_str)
            processed_pixel_count += 1

        # confirm that half of image is red
        # --> get percentage of image that is red.
        color_counts = tile_image.getcolors()  #
        red = (255, 0, 0, 255)
        red_percentage = sum(count for count, color in color_counts if color == red)/sum(count for count, _ in color_counts)
        self.assertTrue(red_percentage >= 0.48, "Resulting Tile image Red({}) < 0.48".format(round(red_percentage, 4)))

    def test_sphericalmercator_to_pixel_rio(self):
        pixel_size_meters = 2500
        tile_pixel_size = 256
        zoom = 6
        tilex = 24
        tiley = 27
        rtmgr = RasterTileManager()
        tile_extent = rtmgr.tile_sphericalmercator_extent(zoom, tilex, tiley)

        # create dummy data in extent
        upperleft_x = tile_extent[0]  # minx
        upperleft_y = tile_extent[3]  # maxy

        # create measurement instances for the left half of the tile
        # --> get the x halfway point
        xmin = tile_extent[0]  # minx
        xmax = tile_extent[2]  # maxx
        ymin = tile_extent[1]  # miny
        tile_width = xmax - xmin
        half_tile_width = tile_width/2
        halfx = xmin + half_tile_width

        # create DummyMeasurement() objects for half of the tile
        d = datetime.date(2014, 11, 28)
        x = upperleft_x
        created_measurement_count = 0
        temp_measurements = []
        while x <= halfx:
            y = upperleft_y
            while y >= ymin:
                point = Point(x, y, srid=SPHERICAL_MERCATOR_SRID)
                m = DummyMeasurement(location=point,
                                     date=d,
                                     counts=50,
                                     value=1)
                temp_measurements.append(m)
                created_measurement_count += 1
                y -= pixel_size_meters
            x += pixel_size_meters

        # create tile image from data
        tile_image = Image.new("RGBA",
                               (tile_pixel_size, tile_pixel_size),
                               (255, 255, 255, 0))
        draw = ImageDraw.Draw(tile_image)
        legend = Legend()
        processed_pixel_count = 0
        for pixel in temp_measurements:
            color_str = legend.get_color_str(pixel.value)
            self.assertTrue(color_str == "hsl(0,100%,50%)")

            # pixel x, y expected to be in spherical-mercator
            # attempt to transform, note if srid is not defined this will generate an error
            if pixel.location.srid != SPHERICAL_MERCATOR_SRID:
                pixel.location.transform(SPHERICAL_MERCATOR_SRID)

            # adjust to upper-left/nw
            upperleft_point = pixel.location
            # (xmin, ymin, xmax, ymax)
            sphericalmercator_bbox = (upperleft_point.x ,
                                      upperleft_point.y - pixel_size_meters,
                                      upperleft_point.x + pixel_size_meters,
                                      upperleft_point.y)
            # transform pixel spherical-mercator coords to image pixel coords
            # --> min values
            xmin, ymin = sphericalmercator_bbox[:2]
            pxmin, pymin = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmin, ymin)

            # --> max values
            xmax, ymax = sphericalmercator_bbox[2:]
            pxmax, pymax = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmax, ymax )
            upperleft_point = (pxmin, pymax)
            upperright_point = (pxmax, pymax)
            lowerright_point = (pxmax, pymin)
            lowerleft_point = (pxmin, pymin)
            coords = (upperleft_point, upperright_point, lowerright_point, lowerleft_point, upperleft_point)

            # draw pixel on tile
            draw.polygon(coords, fill=color_str)
            processed_pixel_count += 1

        # confirm that half of image is red
        # --> get percentage of image that is red.
        color_counts = tile_image.getcolors()  #
        red = (255, 0, 0, 255)
        red_percentage = sum(count for count, color in color_counts if color == red)/sum(count for count, _ in color_counts)
        self.assertTrue(red_percentage >= 0.48, "Resulting Tile image Red({}) < 0.48".format(round(red_percentage, 4)))

    def test_sphericalmercator_to_pixel_sydney(self):
        pixel_size_meters = 2500
        tile_pixel_size = 256
        zoom = 7
        tilex = 117
        tiley = 51
        rtmgr = RasterTileManager()
        tile_extent = rtmgr.tile_sphericalmercator_extent(zoom, tilex, tiley)

        # create dummy data in extent
        upperleft_x = tile_extent[0]  # minx
        upperleft_y = tile_extent[3]  # maxy

        # create measurement instances for the left half of the tile
        # --> get the x halfway point
        xmin = tile_extent[0]  # minx
        xmax = tile_extent[2]  # maxx
        ymin = tile_extent[1]  # miny
        tile_width = xmax - xmin
        half_tile_width = tile_width/2
        halfx = xmin + half_tile_width

        # create DummyMeasurement() objects for half of the tile
        d = datetime.date(2014, 11, 28)
        x = upperleft_x
        created_measurement_count = 0
        temp_measurements = []
        while x <= halfx:
            y = upperleft_y
            while y >= ymin:
                point = Point(x, y, srid=SPHERICAL_MERCATOR_SRID)
                m = DummyMeasurement(location=point,
                                     date=d,
                                     counts=50,
                                     value=1)
                temp_measurements.append(m)
                created_measurement_count += 1
                y -= pixel_size_meters
            x += pixel_size_meters

        # create tile image from data
        tile_image = Image.new("RGBA",
                               (tile_pixel_size, tile_pixel_size),
                               (255, 255, 255, 0))
        draw = ImageDraw.Draw(tile_image)
        legend = Legend()
        processed_pixel_count = 0
        for pixel in temp_measurements:
            color_str = legend.get_color_str(pixel.value)
            self.assertTrue(color_str == "hsl(0,100%,50%)")

            # pixel x, y expected to be in spherical-mercator
            # attempt to transform, note if srid is not defined this will generate an error
            if pixel.location.srid != SPHERICAL_MERCATOR_SRID:
                pixel.location.transform(SPHERICAL_MERCATOR_SRID)

            # adjust to upper-left/nw
            upperleft_point = pixel.location
            # (xmin, ymin, xmax, ymax)
            sphericalmercator_bbox = (upperleft_point.x ,
                                      upperleft_point.y - pixel_size_meters,
                                      upperleft_point.x + pixel_size_meters,
                                      upperleft_point.y)
            # transform pixel spherical-mercator coords to image pixel coords
            # --> min values
            xmin, ymin = sphericalmercator_bbox[:2]
            pxmin, pymin = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmin, ymin)

            # --> max values
            xmax, ymax = sphericalmercator_bbox[2:]
            pxmax, pymax = rtmgr.sphericalmercator_to_pixel(zoom, tilex, tiley, xmax, ymax )
            upperleft_point = (pxmin, pymax)
            upperright_point = (pxmax, pymax)
            lowerright_point = (pxmax, pymin)
            lowerleft_point = (pxmin, pymin)
            coords = (upperleft_point, upperright_point, lowerright_point, lowerleft_point, upperleft_point)

            # draw pixel on tile
            draw.polygon(coords, fill=color_str)
            processed_pixel_count += 1

        # confirm that half of image is red
        # --> get percentage of image that is red.
        color_counts = tile_image.getcolors()  #
        red = (255, 0, 0, 255)
        red_percentage = sum(count for count, color in color_counts if color == red)/sum(count for count, _ in color_counts)
        self.assertTrue(red_percentage >= 0.48, "Resulting Tile image Red({}) < 0.48".format(round(red_percentage, 4)))

    def test_lonlat_to_tile(self):
        rtmgr = RasterTileManager()
        longitude = 7.56198
        latitude = 47.47607
        zoom = 11
        tilex, tiley = rtmgr.lonlat_to_tile(zoom, longitude, latitude)
        self.assertTrue(tilex == 1067 and tiley == 716)

    def test_get_neighbor_tiles(self):
        rtmgr = RasterTileManager()
        zoom = 6
        tilex = 63
        tiley = 60
        actual = rtmgr.get_neighbor_tiles(zoom, tilex, tiley)
        expected = [(63, 61), (62, 61), (62, 60), (62, 59), (63, 59)]
        msg = 'actual({}) != expected({})'.format(actual, expected)
        self.assertTrue(set(actual) == set(expected), msg)

        zoom = 7
        tilex = 119
        tiley = 0
        actual = rtmgr.get_neighbor_tiles(zoom, tilex, tiley)
        expected = [(118, 1), (119, 1), (120, 1), (118, 0), (120, 0)]
        msg = 'actual({}) != expected({})'.format(actual, expected)
        self.assertTrue(set(actual) == set(expected), msg)

        zoom = 11
        tilex = 1893
        tiley = 15
        actual = rtmgr.get_neighbor_tiles(zoom, tilex, tiley)
        expected = [(1893, 16), (1892, 16), (1894, 16), (1892, 15), (1894, 15), (1892, 14), (1893, 14), (1894, 14)]
        msg = 'actual({}) != expected({})'.format(actual, expected)
        self.assertTrue(set(actual) == set(expected), msg)


if __name__ == '__main__':
    unittest.main(verbosity=2)