# Generated for the ZoPhysicist starter project.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=140, unique=True)),
                ("description", models.TextField(blank=True)),
                ("accent_color", models.CharField(default="#55d7ff", max_length=24)),
            ],
            options={"verbose_name_plural": "categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("slug", models.SlugField(blank=True, max_length=240, unique=True)),
                ("cover_image", models.ImageField(blank=True, null=True, upload_to="lesson_covers/")),
                ("short_description", models.TextField(max_length=360)),
                ("full_content", models.TextField(help_text="HTML is supported for headings, formulas, images, and code blocks.")),
                ("publish_date", models.DateTimeField()),
                ("reading_time", models.PositiveIntegerField(default=6, help_text="Estimated minutes")),
                ("is_featured", models.BooleanField(default=False)),
                ("views", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="lessons", to="lessons.category")),
                ("tags", models.ManyToManyField(blank=True, related_name="lessons", to="lessons.tag")),
            ],
            options={"ordering": ["-publish_date"]},
        ),
        migrations.CreateModel(
            name="FeaturedLesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("headline", models.CharField(blank=True, max_length=160)),
                ("priority", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("lesson", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="featured_slot", to="lessons.lesson")),
            ],
            options={"ordering": ["priority", "-lesson__publish_date"]},
        ),
    ]
