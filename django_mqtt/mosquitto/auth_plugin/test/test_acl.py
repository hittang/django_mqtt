from django.contrib.auth.models import User
from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse

from django_mqtt.mosquitto.auth_plugin.test.utils import BasicAuthWithTopicTestCase
from django_mqtt import models


class BasicACLWithTopicTestCase(BasicAuthWithTopicTestCase):
    def setUp(self):
        BasicAuthWithTopicTestCase.setUp(self)
        self.url_testing = reverse('mqtt_acl')

    def get_post_data(self):
        return {
            'username': self.username,
            'topic': self.topic,
            'acc': self.acc
        }


class ACLTestCase(TestCase):
    def setUp(self):
        self.username = 'user'
        self.password = 'password'
        User.objects.create_user(self.username, password=self.password)
        self.url_testing = reverse('mqtt_acl')
        self.client = Client()

    @override_settings(MQTT_ACL_ALLOW=True)
    def test_login_acl_allow_true(self):
        response = self.client.post(self.url_testing, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    @override_settings(MQTT_ACL_ALLOW=False)
    def test_login_acl_allow_false(self):
        response = self.client.post(self.url_testing, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 403)

    def test_wrong_login(self):
        response = self.client.post(self.url_testing, {'username': self.username, 'password': 'wrong'})
        self.assertEqual(response.status_code, 403)

    def test_wrong_user(self):
        response = self.client.post(self.url_testing, {'username': 'wrong', 'password': 'wrong'})
        self.assertEqual(response.status_code, 403)

    def test_wrong_no_password(self):
        response = self.client.post(self.url_testing, {'username': self.username})
        self.assertEqual(response.status_code, 403)

    def test_wrong_no_username(self):
        response = self.client.post(self.url_testing, {'password': self.password})
        self.assertEqual(response.status_code, 403)

    def test_wrong_no_data(self):
        response = self.client.post(self.url_testing, {})
        self.assertEqual(response.status_code, 403)


class NoAcc(BasicACLWithTopicTestCase):
    def test_login_no_acl_allow(self):
        response = self._test_login_no_acl_allow()
        self.assertEqual(response.status_code, 403)

    def test_login_wrong_topic(self):
        response = self._test_login_wrong_topic()
        self.assertEqual(response.status_code, 403)

    def test_login_no_topic(self):
        response = self._test_login_no_topic()
        self.assertEqual(response.status_code, 403)

    def test_login_with_sus_acl_public(self):
        response = self._test_login_with_sus_acl_public()
        self.assertEqual(response.status_code, 403)

    def test_login_with_pub_acl_public(self):
        response = self._test_login_with_pub_acl_public()
        self.assertEqual(response.status_code, 403)

    def test_login_with_sus_acl(self):
        response = self._test_login_with_sus_acl()
        self.assertEqual(response.status_code, 403)

    def test_login_with_pub_acl(self):
        response = self._test_login_with_pub_acl()
        self.assertEqual(response.status_code, 403)


class PubAcc(BasicACLWithTopicTestCase):
    def setUp(self):
        BasicACLWithTopicTestCase.setUp(self)
        self.acc = models.PROTO_MQTT_ACC_PUB

    def test_login_no_acl_allow(self):
        response = self._test_login_no_acl_allow()
        self.assertEqual(response.status_code, 403)

    def test_login_wrong_topic(self):
        response = self._test_login_wrong_topic()
        self.assertEqual(response.status_code, 403)

    def test_login_no_topic(self):
        response = self._test_login_no_topic()
        self.assertEqual(response.status_code, 403)

    def test_login_with_sus_acl_public(self):
        response = self._test_login_with_sus_acl_public()
        self.assertEqual(response.status_code, 403)

    def test_login_with_pub_acl_public(self):
        response = self._test_login_with_pub_acl_public()
        self.assertEqual(response.status_code, 200)

    def test_login_with_sus_acl(self):
        response = self._test_login_with_sus_acl()
        self.assertEqual(response.status_code, 403)

    def test_login_with_pub_acl(self):
        response = self._test_login_with_pub_acl()
        self.assertEqual(response.status_code, 200)
        username = 'new_user'
        User.objects.create_user(username, password=self.password)
        response = self.client.post(self.url_testing, {'username': username,
                                                       'password': self.password,
                                                       'topic': self.topic,
                                                       'acc': self.acc
                                                       })
        self.assertEqual(response.status_code, 403)

    def test_login_with_sus_acl_group(self):
        response = self._test_login_with_sus_acl_group()
        self.assertEqual(response.status_code, 403)

    def test_login_with_pub_acl_group(self):
        response = self._test_login_with_pub_acl_group()
        self.assertEqual(response.status_code, 200)
        username = 'new_user'
        User.objects.create_user(username, password=self.password)
        response = self.client.post(self.url_testing, {'username': username,
                                                       'password': self.password,
                                                       'topic': self.topic,
                                                       'acc': self.acc
                                                       })
        self.assertEqual(response.status_code, 403)


class SusAcc(BasicACLWithTopicTestCase):
    def setUp(self):
        BasicACLWithTopicTestCase.setUp(self)
        self.acc = models.PROTO_MQTT_ACC_SUS

    def test_login_no_acl_allow(self):
        response = self._test_login_no_acl_allow()
        self.assertEqual(response.status_code, 403)

    def test_login_wrong_topic(self):
        response = self._test_login_wrong_topic()
        self.assertEqual(response.status_code, 403)

    def test_login_no_topic(self):
        response = self._test_login_no_topic()
        self.assertEqual(response.status_code, 403)

    def test_login_with_sus_acl_public(self):
        response = self._test_login_with_sus_acl_public()
        self.assertEqual(response.status_code, 200)

    def test_login_with_pub_acl_public(self):
        response = self._test_login_with_pub_acl_public()
        self.assertEqual(response.status_code, 403)

    def test_login_with_sus_acl(self):
        response = self._test_login_with_sus_acl()
        self.assertEqual(response.status_code, 200)
        username = 'new_user'
        User.objects.create_user(username, password=self.password)
        response = self.client.post(self.url_testing, {'username': username,
                                                       'password': self.password,
                                                       'topic': self.topic,
                                                       'acc': self.acc
                                                       })
        self.assertEqual(response.status_code, 403)

    def test_login_with_pub_acl(self):
        response = self._test_login_with_pub_acl()
        self.assertEqual(response.status_code, 403)

    def test_login_with_sus_acl_group(self):
        response = self._test_login_with_sus_acl_group()
        self.assertEqual(response.status_code, 200)
        username = 'new_user'
        User.objects.create_user(username, password=self.password)
        response = self.client.post(self.url_testing, {'username': username,
                                                       'password': self.password,
                                                       'topic': self.topic,
                                                       'acc': self.acc
                                                       })
        self.assertEqual(response.status_code, 403)

    def test_login_with_pub_acl_group(self):
        response = self._test_login_with_pub_acl_group()
        self.assertEqual(response.status_code, 403)
