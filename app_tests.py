import json
import unittest
from http import HTTPStatus

import app

BASE_URL = '/'
OTHER_ROUTE = BASE_URL + 'some_other_route'

JSON_MIMETYPE = 'application/json'
INCORRECT_MIMETYPE = 'plain/text'

SAMPLE_INPUT = '{"vehicles":[{"id":1,"start_index":0,"capacity":[4]},{"id":2,"start_index":1,"capacity":[6]},{"id":3,"start_index":2,"capacity":[6]}],"jobs":[{"id":1,"location_index":3,"delivery":[2],"service":327},{"id":2,"location_index":4,"delivery":[1],"service":391},{"id":3,"location_index":5,"delivery":[1],"service":297},{"id":4,"location_index":6,"delivery":[2],"service":234},{"id":5,"location_index":7,"delivery":[1],"service":357},{"id":6,"location_index":8,"delivery":[1],"service":407},{"id":7,"location_index":9,"delivery":[1],"service":382}],"matrix":[[0,516,226,853,1008,1729,346,1353,1554,827],[548,0,474,1292,1442,2170,373,1801,1989,1068],[428,466,0,1103,1175,1998,226,1561,1715,947],[663,1119,753,0,350,1063,901,681,814,1111],[906,1395,1003,292,0,822,1058,479,600,1518],[1488,1994,1591,905,776,0,1746,603,405,1676],[521,357,226,1095,1167,1987,0,1552,1705,1051],[1092,1590,1191,609,485,627,1353,0,422,1583],[1334,1843,1436,734,609,396,1562,421,0,1745],[858,1186,864,1042,1229,1879,984,1525,1759,0]]}'
SAMPLE_OUTPUT = '{"totalDeliveryDuration":3950,"routes":{"1":["7"],"2":["4"],"3":["1","2","5","6","3"]}}'

EMPTY_ROUTES_INPUT = '{"vehicles":[{"id":1,"start_index":0,"capacity":[4]},{"id":2,"start_index":1,"capacity":[6]},{"id":3,"start_index":2,"capacity":[6]}],"jobs":[{"id":1,"location_index":3,"delivery":[2],"service":327},{"id":2,"location_index":4,"delivery":[1],"service":391}],"matrix":[[0,516,226,853,1008],[548,0,474,1292,1442],[428,466,0,1103,1175],[663,1119,753,0,350],[906,1395,1003,292,0]]}'
EMPTY_ROUTES_OUTPUT = '{"totalDeliveryDuration":1203,"routes":{"1":["1","2"],"2":[],"3":[]}}'

UNASSIGNED_DELIVERY_INPUT = '{"vehicles":[{"id":1,"start_index":0,"capacity":[4]}],"jobs":[{"id":1,"location_index":1,"delivery":[2],"service":327},{"id":2,"location_index":2,"delivery":[1],"service":391},{"id":3,"location_index":3,"delivery":[1],"service":297},{"id":4,"location_index":4,"delivery":[2],"service":234},{"id":5,"location_index":5,"delivery":[1],"service":357},{"id":6,"location_index":6,"delivery":[1],"service":407},{"id":7,"location_index":7,"delivery":[1],"service":382}],"matrix":[[0,853,1008,1729,346,1353,1554,827],[663,0,350,1063,901,681,814,1111],[906,292,0,822,1058,479,600,1518],[1488,905,776,0,1746,603,405,1676],[521,1095,1167,1987,0,1552,1705,1051],[1092,609,485,627,1353,0,422,1583],[1334,734,609,396,1562,421,0,1745],[858,1042,1229,1879,984,1525,1759,0]]}'
UNASSIGNED_DELIVERY_OUTPUT = '{"totalDeliveryDuration":2305,"routes":{"1":["2","5","6","3"]}}'

NO_JOBS_INPUT = '{"vehicles":[{"id":1,"start_index":0,"capacity":[4]},{"id":2,"start_index":1,"capacity":[6]},{"id":3,"start_index":2,"capacity":[6]}],"jobs":[],"matrix":[[0,516,226],[548,0,474],[428,466,0]]}'
NO_VEHICLES_INPUT = '{"vehicles":[],"jobs":[{"id":1,"location_index":1,"delivery":[2],"service":327},{"id":2,"location_index":2,"delivery":[1],"service":391},{"id":3,"location_index":3,"delivery":[1],"service":297},{"id":4,"location_index":4,"delivery":[2],"service":234},{"id":5,"location_index":5,"delivery":[1],"service":357},{"id":6,"location_index":6,"delivery":[1],"service":407},{"id":7,"location_index":7,"delivery":[1],"service":382}],"matrix":[[0,350,1063,901,681,814,1111],[292,0,822,1058,479,600,1518],[905,776,0,1746,603,405,1676],[1095,1167,1987,0,1552,1705,1051],[609,485,627,1353,0,422,1583],[734,609,396,1562,421,0,1745],[1042,1229,1879,984,1525,1759]]}'
BAD_MATRIX_INPUT = '{"vehicles":[{"id":1,"start_index":0,"capacity":[4]},{"id":2,"start_index":1,"capacity":[6]},{"id":3,"start_index":2,"capacity":[6]}],"jobs":[{"id":1,"location_index":3,"delivery":[2],"service":327},{"id":2,"location_index":4,"delivery":[1],"service":391},{"id":3,"location_index":5,"delivery":[1],"service":297},{"id":4,"location_index":6,"delivery":[2],"service":234},{"id":5,"location_index":7,"delivery":[1],"service":357},{"id":6,"location_index":8,"delivery":[1],"service":407},{"id":7,"location_index":9,"delivery":[1],"service":382}],"matrix":[[0,516,226,853,1008,1729,346,1353,1554,827],[373,1801,1989,1068],[428,1998,226,1561,1715,947],[663,1119,753,901,681,814,1111],[906,1395,1003,600,1518],[1488,1994,1591,905,776,0,1746,603,405,1676],[521,357,226,1095,1167,1987,0,1552],[1092,1590,1191,609,485,1353,0,422,1583],[1334,1843,1436,734,0,1745],[858,1186,864,1042,1229,1879,984,1525,1759]]}'
MISSING_MATRIX_INPUT = '{"vehicles":[{"id":1,"start_index":0,"capacity":[4]},{"id":2,"start_index":1,"capacity":[6]},{"id":3,"start_index":2,"capacity":[6]}],"jobs":[{"id":1,"location_index":3,"delivery":[2],"service":327},{"id":2,"location_index":4,"delivery":[1],"service":391},{"id":3,"location_index":5,"delivery":[1],"service":297},{"id":4,"location_index":6,"delivery":[2],"service":234},{"id":5,"location_index":7,"delivery":[1],"service":357},{"id":6,"location_index":8,"delivery":[1],"service":407},{"id":7,"location_index":9,"delivery":[1],"service":382}]}'


class TestCorrectlyConfiguredApp(unittest.TestCase):
    def setUp(self):
        app.load_config()
        self.app = app.app.test_client()
        self.app.testing = True

    def test_unexpected_methods(self):
        response = self.app.get(BASE_URL)
        self.assertEqual(response.status_code, 405)

    def test_unexpected_mimetype(self):
        response = self.app.post(BASE_URL, data=SAMPLE_INPUT, content_type=INCORRECT_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_try_another_routes(self):
        response = self.app.post(OTHER_ROUTE)
        self.assertEqual(response.status_code, 404)

    def test_given_sample_request(self):
        response = self.app.post(BASE_URL, data=SAMPLE_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data()), json.loads(SAMPLE_OUTPUT))

    def test_if_there_will_be_empty_routes(self):
        response = self.app.post(BASE_URL, data=EMPTY_ROUTES_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data()), json.loads(EMPTY_ROUTES_OUTPUT))

    def test_if_there_will_be_unassigned_delivery(self):
        response = self.app.post(BASE_URL, data=UNASSIGNED_DELIVERY_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data()), json.loads(UNASSIGNED_DELIVERY_OUTPUT))

    def test_no_input(self):
        response = self.app.post(BASE_URL, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_input_as_empty_object(self):
        response = self.app.post(BASE_URL, data='{}', content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_if_there_is_no_jobs_to_do(self):
        response = self.app.post(BASE_URL, data=NO_JOBS_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_if_there_is_no_vehicles(self):
        response = self.app.post(BASE_URL, data=NO_VEHICLES_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_unexpected_input(self):
        response = self.app.post(BASE_URL, data=SAMPLE_OUTPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_distance_matrix_incomplete(self):
        response = self.app.post(BASE_URL, data=BAD_MATRIX_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_distance_matrix_not_provided(self):
        response = self.app.post(BASE_URL, data=MISSING_MATRIX_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


class TestMisconfiguredApp(TestCorrectlyConfiguredApp):
    def setUp(self):
        app.load_config()
        app.configuration[app.CONFIG_OPTIMIZATION_SERVER][app.CONFIG_VROOM][app.CONFIG_PORT] = '150'
        self.app = app.app.test_client()
        self.app.testing = True

    def test_given_sample_request(self):
        response = self.app.post(BASE_URL, data=SAMPLE_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_if_there_will_be_empty_routes(self):
        response = self.app.post(BASE_URL, data=EMPTY_ROUTES_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_if_there_will_be_unassigned_delivery(self):
        response = self.app.post(BASE_URL, data=UNASSIGNED_DELIVERY_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_if_there_is_no_jobs_to_do(self):
        response = self.app.post(BASE_URL, data=NO_JOBS_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_if_there_is_no_vehicles(self):
        response = self.app.post(BASE_URL, data=NO_VEHICLES_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_unexpected_input(self):
        response = self.app.post(BASE_URL, data=SAMPLE_OUTPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_distance_matrix_incomplete(self):
        response = self.app.post(BASE_URL, data=BAD_MATRIX_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_distance_matrix_not_provided(self):
        response = self.app.post(BASE_URL, data=MISSING_MATRIX_INPUT, content_type=JSON_MIMETYPE)
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)


if __name__ == '__main__':
    unittest.main()
