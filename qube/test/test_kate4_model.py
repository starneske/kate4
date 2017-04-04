#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testkate4Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_kate4_model(self):
        from qube.src.models.kate4 import kate4
        kate4_data = kate4(name='testname')
        kate4_data.tenantId = "23432523452345"
        kate4_data.orgId = "987656789765670"
        kate4_data.createdBy = "1009009009988"
        kate4_data.modifiedBy = "1009009009988"
        kate4_data.createDate = str(int(time.time()))
        kate4_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            kate4_data.save()
            self.assertIsNotNone(kate4_data.mongo_id)
            kate4_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
