import hashlib

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

import cloudinary.uploader

from books.models import Profile


AVATAR_COLORS = [
    "#E74C3C", "#8E44AD", "#2980B9", "#27AE60",
    "#F39C12", "#16A085", "#D35400", "#2C3E50",
    "#C0392B", "#1ABC9C",
]


def generate_and_upload_avatar(user):
    """Generate SVG avatar and upload directly to Cloudinary."""
    first    = (user.first_name[0] if user.first_name else user.email[0] if user.email else user.username[0]).upper()
    last     = (user.last_name[0] if user.last_name else "").upper()
    initials = f"{first}{last}" if last else first

    seed     = user.email or user.username
    hash_int = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    color    = AVATAR_COLORS[hash_int % len(AVATAR_COLORS)]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <circle cx="50" cy="50" r="50" fill="{color}"/>
  <text x="50" y="50"
        font-size="{36 if len(initials) == 1 else 28}"
        text-anchor="middle"
        dominant-baseline="middle"
        fill="white">
    {initials}
  </text>
</svg>"""

    result = cloudinary.uploader.upload(
        ContentFile(svg.encode("utf-8"), name=f"{user.username}.svg"),
        folder="profile_pictures",
        public_id=f"avatar_{user.id}",
        resource_type="raw",   # SVG must be raw, not image
        overwrite=True,
    )

    return result.get("public_id")


class Command(BaseCommand):
    help = "Create missing profiles and generate Cloudinary avatars for existing users"

    def handle(self, *args, **kwargs):
        users   = User.objects.all()
        total   = users.count()
        success = 0
        failed  = 0

        self.stdout.write(f"Processing {total} user(s)...\n")

        for user in users:
            try:
                profile, created = Profile.objects.get_or_create(user=user)

                if not profile.profile_picture:
                    public_id = generate_and_upload_avatar(user)
                    profile.profile_picture = public_id
                    profile.save()

                    status = "profile created + avatar uploaded" if created else "avatar uploaded"
                    self.stdout.write(f"  ✔ {user.username} → {status}")
                else:
                    self.stdout.write(f"  ⏭ {user.username} → already has a picture, skipped")

                success += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✘ {user.username} → {e}"))
                failed += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Done. {success} succeeded, {failed} failed."))