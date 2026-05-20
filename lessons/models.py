from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    accent_color = models.CharField(max_length=24, default="#55d7ff")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="lessons")
    tags = models.ManyToManyField(Tag, blank=True, related_name="lessons")
    cover_image = models.ImageField(upload_to="lesson_covers/", blank=True, null=True)
    short_description = models.TextField(max_length=360)
    full_content = CKEditor5Field(config_name="default")  # ← updated
    publish_date = models.DateTimeField()
    reading_time = models.PositiveIntegerField(default=6, help_text="Estimated minutes")
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("lesson_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class FeaturedLesson(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="featured_slot")
    headline = models.CharField(max_length=160, blank=True)
    priority = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["priority", "-lesson__publish_date"]

    def __str__(self):
        return self.headline or self.lesson.title


class PracticeQuestion(models.Model):
    EXAM_CHOICES = [
        ("jee-main", "JEE Main"),
        ("jee-advanced", "JEE Advanced"),
        ("neet", "NEET"),
        ("boards", "Boards"),
    ]
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=220)
    exam = models.CharField(max_length=30, choices=EXAM_CHOICES)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="practice_questions")
    related_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name="practice_questions")
    tags = models.ManyToManyField(Tag, blank=True, related_name="practice_questions")
    question = CKEditor5Field(config_name="default")         # ← updated
    option_a = models.CharField(max_length=360)
    option_b = models.CharField(max_length=360)
    option_c = models.CharField(max_length=360)
    option_d = models.CharField(max_length=360)
    correct_option = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")])
    solution = CKEditor5Field(config_name="default")         # ← updated
    formula_used = models.CharField(max_length=300, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="medium")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["exam", "-year", "category__name", "title"]

    def get_absolute_url(self):
        return reverse("practice_question_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.get_exam_display()} {self.year} - {self.title}"