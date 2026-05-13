from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Profile
from books.utils import generate_avatar


class Command(BaseCommand):
    help = 'Create missing profiles and generate avatars for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        total = users.count()

        self.stdout.write(f'Processing {total} user(s)...\n')

        success = 0
        failed = 0

        for user in users:
            try:
                # Get or create the profile
                profile, created = Profile.objects.get_or_create(user=user)

                # Only generate avatar if they don't already have one
                if not profile.profile_picture:
                    avatar_path = generate_avatar(user)
                    profile.profile_picture = avatar_path
                    profile.save()
                    status = "profile created + avatar generated" if created else "avatar generated"
                    self.stdout.write(f'  ✔ {user.username} → {status}')
                else:
                    self.stdout.write(f'  ⏭ {user.username} → already has a picture, skipped')

                success += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✘ {user.username} → {e}'))
                failed += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done. {success} succeeded, {failed} failed.'))