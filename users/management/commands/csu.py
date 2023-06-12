from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='hihi64741@gmail.com',
            first_name='Ivan',
            last_name='Belopolsky',
            is_staff=True,
            is_superuser=True,

        )

        user.set_password('vtufvfvf163')
        user.save()
