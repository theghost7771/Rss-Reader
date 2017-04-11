from django.core.management.base import BaseCommand
from rss_reader.feeds.models import Feed, FeedItem


class Command(BaseCommand):
    help = 'Update feeds'

    def handle(self, *args, **options):
        to_update = []
        for feed in Feed.objects.filter(is_active=True):
            self.stdout.write('Parsing {} feed'.format(feed.name))
            feed_items = feed.collect_items()
            to_update.extend(feed_items)

            self.stdout.write(self.style.SUCCESS('Collected %d items for %s' % (len(feed_items), feed.name)))

        FeedItem.objects.bulk_create(to_update)
        self.stdout.write(self.style.SUCCESS('Successfully added %d items' % len(to_update)))

