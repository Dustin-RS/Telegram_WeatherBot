import unittest
import WeatherParser


class TestWeatherParserMethods(unittest.TestCase):
    """
    Class for unit testing WeatherParser methods.
    """
    def test_get_desc_emoji_1(self):
        """
        Test for converting string to emojis.
        """
        self.assertEqual(WeatherParser.get_desc_emoji("overcast clouds"), '☁️')

    def test_get_desc_emoji_2(self):
        self.assertEqual(WeatherParser.get_desc_emoji("light rain"), '🌦️')

    def test_get_desc_emoji_3(self):
        self.assertEqual(WeatherParser.get_desc_emoji("heavy snow"), '❄️')

    def test_gettime_from_datetime(self):
        self.assertEqual(WeatherParser.gettime_from_datetime("2001-08-20 00:12:15"), "00:12:15")


if __name__ == '__main__':
    unittest.main()  # Launch unit tests.