from django.test import TestCase, Client

from hackernews.models import Item
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

    def test_order_ASC(self):
        ItemFactory.create_batch(4)
        ItemFactory.create(title='title_0')

        got = self.client.get('/posts', {'order': 'title'})

        self.assertListEqual(
            [item['title'] for item in got.data],
            [i.title for i in Item.objects.order_by('title')]
        )

    def test_order_DESC(self):
        ItemFactory.create_batch(4)
        ItemFactory.create(title='title_0')

        got = self.client.get('/posts', {'order': '-title'})

        self.assertListEqual(
            [item['title'] for item in got.data],
            [i.title for i in Item.objects.order_by('-title')]
        )

    def test_invalid_field_by_order(self):
        ItemFactory.create_batch(4)
        ItemFactory.create(title='title_0')

        got = self.client.get('/posts', {'order': 'invalid_field'})

        self.assertListEqual(
            [item['title'] for item in got.data],
            [i.title for i in Item.objects.order_by('id')]
        )

    def test_default_limit(self):
        pass

    def test_limit(self):
        pass

    def test_offset(self):
        pass

    def test_offset_and_limit(self):
        pass

    def test_offset_and_limit_and_order(self):
        pass
