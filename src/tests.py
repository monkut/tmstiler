import unittest
from tmstiler.rtm import RasterTileManager



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
        coord_type = {0:"xmin", 1: "ymin", 2:"xmax", 3:"ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                            round(actual, 2),
                                                            coord_type[idx],
                                                            round(expected, 2),
                                                            rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax, rtm.spherical_mercator_ymax)
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
        # Sydney (sphericl mercator)
        z = 5
        tilex = 29
        tiley = 12

        rtm = RasterTileManager()
        # expected results taken from:
        # http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/
        expected_extent = (16280475.528516259, -5009377.085697312, 17532819.79994059, -3757032.814272983)
        actual_extent = rtm.tile_sphericalmercator_extent(z, tilex, tiley)
        coord_type = {0:"xmin", 1: "ymin", 2:"xmax", 3:"ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                            round(actual, 2),
                                                            coord_type[idx],
                                                            round(expected, 2),
                                                            rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax, rtm.spherical_mercator_ymax)
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
        coord_type = {0:"xmin", 1: "ymin", 2:"xmax", 3:"ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                            round(actual, 1),
                                                            coord_type[idx],
                                                            round(expected, 1),
                                                            rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax, rtm.spherical_mercator_ymax)
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
        coord_type = {0:"xmin", 1: "ymin", 2:"xmax", 3:"ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                            round(actual, 1),
                                                            coord_type[idx],
                                                            round(expected, 1),
                                                            rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax, rtm.spherical_mercator_ymax)
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
        coord_type = {0:"xmin", 1: "ymin", 2:"xmax", 3:"ymax"}
        for idx, (actual, expected) in enumerate(zip(actual_extent, expected_extent)):
            msg = "actual_{}({}) != expected_{}({})\nNumber Tiles at zoom:{}".format(coord_type[idx],
                                                            round(actual, 1),
                                                            coord_type[idx],
                                                            round(expected, 1),
                                                            rtm.tiles_per_dimension(z))
            msg += "\nSphericalMercator (xmax, ymax): {}, {}".format(rtm.spherical_mercator_xmax, rtm.spherical_mercator_ymax)
            msg += "\nzoom: {}".format(z)
            msg += "\ntilex: {}".format(tilex)
            msg += "\ntiley: {}".format(tiley)
            msg += "\nactual extents:   {}".format(actual_extent)
            msg += "\nexpected extents: {}".format(expected_extent)
            self.assertTrue(round(actual, 1) == round(expected, 1), msg)

if __name__ == '__main__':
    unittest.main()