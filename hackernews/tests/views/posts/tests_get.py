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
        ItemFactory.create_batch(6)

        got = self.client.get('/posts')

        self.assertEqual(Item.objects.count(), 6)
        self.assertEqual(len(got.data), 5)

    def test_limit(self):
        ItemFactory.create_batch(6)

        got = self.client.get('/posts', {'limit': 3})

        self.assertEqual(len(got.data), 3)
        self.assertEqual(
            [item['id'] for item in got.data],
            [item.id for item in Item.objects.order_by('id')[:3]]
        )

    def test_offset_and_limit(self):
        ItemFactory.create_batch(6)

        got = self.client.get('/posts', {'limit': 3, 'offset': 3})

        self.assertEqual(len(got.data), 3)
        self.assertEqual(
            [item['id'] for item in got.data],
            [item.id for item in Item.objects.order_by('id')[3:6]]
        )

    def test_offset_and_limit_and_order(self):
        ItemFactory.create_batch(6)

        got = self.client.get('/posts', {'limit': 3, 'offset': 3, 'order': '-url'})

        self.assertEqual(len(got.data), 3)
        self.assertEqual(
            [item['url'] for item in got.data],
            [item.url for item in Item.objects.order_by('-url')[3:6]]
        )

    def test_big_number_limit(self):
        ItemFactory.create_batch(110)

        got = self.client.get('/posts', {'limit': 100500})

        self.assertEqual(Item.objects.count(), 110)
        self.assertEqual(len(got.data), 100)

    def test_not_positive_number_limit(self):
        ItemFactory.create_batch(6)

        got = self.client.get('/posts', {'limit': -3})

        self.assertEqual(len(got.data), 5)

    def test_not_positive_number_offser(self):
        ItemFactory.create_batch(6)

        got = self.client.get('/posts', {'limit': 3, 'offset': -3})

        self.assertEqual(len(got.data), 3)
        self.assertEqual(
            [item['id'] for item in got.data],
            [item.id for item in Item.objects.order_by('id')[:3]]
        )
