import json

from django.core.management.base import BaseCommand
from web.models import Movie


class Command(BaseCommand):
    help = 'Seed movies data from JSON file'

    def handle(self, *args, **kwargs):
        with open('web/fixtures/movies.json', 'r') as file:
            data = json.load(file)
            for movie in data:
                dataset = Movie.objects.filter(name=movie['name']).count()
                if dataset == 0:
                    Movie.objects.create(
                        name=movie['name'],
                        description=movie['description'],
                        imgPath=movie['imgPath'],
                        duration=movie['duration'],
                        genre=movie['genre'],
                        language=movie['language'],
                        mpaaRating_type=movie['mpaaRating']['type'],
                        mpaaRating_label=movie['mpaaRating']['label'],
                        userRating=movie['userRating'],
                    )
        self.stdout.write(self.style.SUCCESS(
            'Movies data imported successfully'))
