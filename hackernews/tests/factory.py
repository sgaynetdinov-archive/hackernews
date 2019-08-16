import factory


class ItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'hackernews.Item'

    hacker_news_id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: f'title_{n}')
    url = factory.Sequence(lambda n: f'url_{n}')
