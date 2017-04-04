#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['KATE4_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['KATE4_MONGOALCHEMY_SERVER'] = ''
    os.environ['KATE4_MONGOALCHEMY_PORT'] = ''
    os.environ['KATE4_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.kate4 import kate4
    from qube.src.services.kate4service import kate4Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, kate4ServiceError


class Testkate4Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.kate4Service = kate4Service(context)
        self.kate4_api_model = self.createTestModelData()
        self.kate4_data = self.setupDatabaseRecords(self.kate4_api_model)
        self.kate4_someoneelses = \
            self.setupDatabaseRecords(self.kate4_api_model)
        self.kate4_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.kate4_someoneelses.save()
        self.kate4_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.kate4_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.kate4_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, kate4_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            kate4_data = kate4(name='test_record')
            for key in kate4_api_model:
                kate4_data.__setattr__(key, kate4_api_model[key])

            kate4_data.description = 'my short description'
            kate4_data.tenantId = "23432523452345"
            kate4_data.orgId = "987656789765670"
            kate4_data.createdBy = "1009009009988"
            kate4_data.modifiedBy = "1009009009988"
            kate4_data.createDate = str(int(time.time()))
            kate4_data.modifiedDate = str(int(time.time()))
            kate4_data.save()
            return kate4_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_kate4(self, *args, **kwargs):
        result = self.kate4Service.save(self.kate4_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.kate4_api_model['name'])
        kate4.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_kate4(self, *args, **kwargs):
        self.kate4_api_model['name'] = 'modified for put'
        id_to_find = str(self.kate4_data.mongo_id)
        result = self.kate4Service.update(
            self.kate4_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.kate4_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_kate4_description(self, *args, **kwargs):
        self.kate4_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.kate4_data.mongo_id)
        result = self.kate4Service.update(
            self.kate4_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.kate4_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kate4_item(self, *args, **kwargs):
        id_to_find = str(self.kate4_data.mongo_id)
        result = self.kate4Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kate4_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(kate4ServiceError):
            self.kate4Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kate4_list(self, *args, **kwargs):
        result_collection = self.kate4Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.kate4_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.kate4_data.mongo_id)
        with self.assertRaises(kate4ServiceError) as ex:
            self.kate4Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.kate4_data.mongo_id)
        self.kate4Service.auth_context.is_system_user = True
        self.kate4Service.delete(id_to_delete)
        with self.assertRaises(kate4ServiceError) as ex:
            self.kate4Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.kate4Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.kate4_someoneelses.mongo_id)
        with self.assertRaises(kate4ServiceError):
            self.kate4Service.delete(id_to_delete)
