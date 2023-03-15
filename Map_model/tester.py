from cityModel import travel_time
import unittest


class TestSum(unittest.TestCase):

    # Test travel_time func for correct output of seconds, and the original speed(mph) passed to calculate that time.
    def test_travel_time_output(self):
        result_seconds, result_mph = travel_time(30, 15)
        self.assertEqual(result_seconds, 7200)
        self.assertEqual(result_mph, 15)

        result_seconds, result_mph = travel_time(28, 13.5)
        self.assertEqual(result_seconds, 7467)  # 7466.66.. should round 7467
        self.assertEqual(result_mph, 13.5)


if __name__ == '__main__':
    unittest.main()
