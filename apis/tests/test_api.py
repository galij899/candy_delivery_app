from django.test import Client, TestCase
import json

class ApiTest(TestCase):
    def test_setUp(self):
        self.client = Client()

    def test_postCouriers(self):
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
