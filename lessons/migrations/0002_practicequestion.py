from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PracticeQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("exam", models.CharField(choices=[("jee-main", "JEE Main"), ("jee-advanced", "JEE Advanced"), ("neet", "NEET"), ("boards", "Boards")], max_length=30)),
                ("year", models.PositiveIntegerField()),
                ("question", models.TextField(help_text="HTML is supported for formulas, images, and formatted text.")),
                ("option_a", models.CharField(max_length=360)),
                ("option_b", models.CharField(max_length=360)),
                ("option_c", models.CharField(max_length=360)),
                ("option_d", models.CharField(max_length=360)),
                ("correct_option", models.CharField(choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")], max_length=1)),
                ("solution", models.TextField(help_text="HTML is supported for detailed solutions.")),
                ("formula_used", models.CharField(blank=True, max_length=300)),
                ("difficulty", models.CharField(choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")], default="medium", max_length=20)),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="practice_questions", to="lessons.category")),
                ("related_lesson", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="practice_questions", to="lessons.lesson")),
                ("tags", models.ManyToManyField(blank=True, related_name="practice_questions", to="lessons.tag")),
            ],
            options={
                "ordering": ["exam", "-year", "category__name", "title"],
            },
        ),
    ]
