from django.test import Client, TestCase
import json


class ApiTest(TestCase):
    def test_setUp(self):
        self.client = Client()

    def test_postCouriers_correct(self):
        data = {
                "data": [
                    {
                        "courier_id": 1,
                        "courier_type": "foot",
                        "regions": [1, 12, 22],
                        "working_hours": ["11:35-14:05", "09:00-11:00"]
                    },
                    {
                        "courier_id": 2,
                        "courier_type": "bike",
                        "regions": [22],
                        "working_hours": ["09:00-18:00"]
                    },
                    {
                        "courier_id": 3,
                        "courier_type": "car",
                        "regions": [12, 22, 23, 33],
                        "working_hours": []
                    },
                ]
            }

        correct_response = {"couriers": [{"id": 1}, {"id": 2}, {"id": 3}]}

        response = self.client.post(path='/couriers',
                                    data=data,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), correct_response)

    def test_postCouriers_badrequest(self):
        """
        Проверка на пропущенные, неописанные и невалидные поля
        """

        data = {
            "data": [
                {
                    "courier_id": 4,
                    "courier_type": "foot",
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"],
                    "someField": "someValue"
                },
                {
                    "courier_id": 5,
                    "courier_type": "bike",
                    "working_hours": ["09:00-18:00"]
                },
                {
                    "courier_id": 6,
                    "courier_type": "car",
                    "regions": [12, 22, 23, 33],
                    "working_hours": ["10:00-12:00"]
                },
            ]
        }

        correct_response = {
            "validation_error": {
                "couriers": [{"id": 4}, {"id": 5}]
            }
        }

        response = self.client.post(path='/couriers',
                                    data=data,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), correct_response)

    def test_patchCouriers_correct(self):

        self.test_postCouriers_correct()

        data = {
            "regions": [11, 33, 2]
        }

        correct_response = {
                        "courier_id": 2,
                        "courier_type": "bike",
                        "regions": [11, 33, 2],
                        "working_hours": ["09:00-18:00"]
                    }

        response = self.client.patch(path='/couriers/2',
                                     data=data,
                                     content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), correct_response)

    def test_patchCouriers_badrequest(self):

        data = {
            "SomeField": [11, 33, 2]
        }

        response = self.client.patch(path='/couriers/2',
                                     data=data,
                                     content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_postOrders_correct(self):

        data = {
                "data": [
                    {
                        "order_id": 1,
                        "weight": 0.23,
                        "region": 12,
                        "delivery_hours": ["09:00-18:00"]
                    },
                    {
                        "order_id": 2,
                        "weight": 50,
                        "region": 1,
                        "delivery_hours": ["09:00-18:00"]
                    },
                    {
                        "order_id": 3,
                        "weight": 0.02,
                        "region": 22,
                        "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                    },
                ]
            }

        correct_response = {
                "orders": [{"id": 1}, {"id": 2}, {"id": 3}]
            }

        response = self.client.post(path='/orders',
                                    data=data,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), correct_response)

    def test_postOrders_badrequest(self):

        data = {
            "data": [
                {
                    "order_id": 4,
                    "weight": 0.23,
                    "region": 12,
                },
                {
                    "order_id": 5,
                    "weight": 51,
                    "region": 1,
                    "delivery_hours": ["09:00-18:00"]
                },
            ]
        }

        correct_response = {
            "validation_error": {
                "orders": [{"id": 4}, {"id": 5}]
            }
        }

        response = self.client.post(path='/orders',
                                    data=data,
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), correct_response)
