from django.test import TestCase, Client

from hackernews.tests.factory import ItemFactory


class PostsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_response_empty(self):
        got = self.client.get('/posts')

        self.assertListEqual(got.data, [])

    def test_response(self):
        item = ItemFactory.create()

        got = self.client.get('/posts')

        data = got.data[0]

        self.assertEqual(data['id'], item.id)
        self.assertEqual(data['title'], item.title)
        self.assertEqual(data['url'], item.url)
        self.assertEqual(data['created'], item.created.strftime('%Y-%m-%dT%H:%M:%S.%f'))

    def test_order(self):
        pass

    def test_limit(self):
        pass

    def test_offset(self):
        pass

    def test_offset_and_limit(self):
        pass

    def test_offset_and_limit_and_order(self):
        pass
