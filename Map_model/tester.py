from cityModel import travel_time, index_check
from cityModel import endpoint1, endpoint3, intersection1, intersection2, intersection3, onRamp1, offRamp1
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

    def test_index_check(self):
        '''
        def index_check(
                current_place: Any,
                next_place: Any,
                previous_place: Any) -> None
        '''
        self.assertTrue(index_check(endpoint3, intersection2, previous_place=None), True)
        #  entering the roadnetwork, no previous location
        self.assertTrue(index_check(endpoint1, intersection2, intersection2), True)
        #  entering an endpoint, should be able to leave it as well

        self.assertTrue(index_check(intersection2, intersection1, endpoint3), True)
        self.assertTrue(index_check(intersection2, intersection1, intersection3), True)
        #  inter 3 ---> inter 2 ---> inter 1





        pass





if __name__ == '__main__':
    unittest.main()
