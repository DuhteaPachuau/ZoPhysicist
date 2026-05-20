from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, FeaturedLesson, Lesson, PracticeQuestion


def published_lessons():
    return Lesson.objects.filter(is_published=True).select_related("category").prefetch_related("tags")


def published_questions():
    return PracticeQuestion.objects.filter(is_published=True).select_related("category", "related_lesson").prefetch_related("tags")


def home(request):
    lessons = published_lessons()
    featured = lessons.filter(is_featured=True)[:3]
    curated = FeaturedLesson.objects.filter(is_active=True, lesson__is_published=True).select_related("lesson")[:4]
    context = {
        "featured_lessons": featured,
        "curated_lessons": curated,
        "latest_lessons": lessons[:6],
        "continue_lessons": lessons[6:9],
        "categories": Category.objects.all()[:8],
        "trending_topics": ["Quantum fields", "Relativity", "Astrophysics", "Thermodynamics", "Optics", "Mechanics"],
        "meta_title": "ZoPhysicist",
        "meta_description": "Tunlai takin Science leh Technology lam thiam ang aw! Chhiar la,chhinchhiah la,ti chhin la,thiam rawh.",
        
    }
    return render(request, "lessons/home.html", context)


def lesson_detail(request, slug):
    lesson = get_object_or_404(published_lessons(), slug=slug)
    Lesson.objects.filter(pk=lesson.pk).update(views=lesson.views + 1)
    related = published_lessons().filter(category=lesson.category).exclude(pk=lesson.pk)[:3]
    ordered = list(published_lessons().values_list("id", "slug", "title"))
    current_index = next((index for index, item in enumerate(ordered) if item[0] == lesson.id), None)
    previous_lesson = ordered[current_index + 1] if current_index is not None and current_index + 1 < len(ordered) else None
    next_lesson = ordered[current_index - 1] if current_index not in (None, 0) else None
    return render(
        request,
        "lessons/lesson_detail.html",
        {
            "lesson": lesson,
            "related_lessons": related,
            "previous_lesson": previous_lesson,
            "next_lesson": next_lesson,
            "meta_title": f"{lesson.title} - ZoPhysicist",
            "meta_description": lesson.short_description,
            "og_image": lesson.cover_image.url if lesson.cover_image else None,

        },
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    query = request.GET.get("q", "").strip()
    lessons = published_lessons().filter(category=category)
    if query:
        lessons = lessons.filter(Q(title__icontains=query) | Q(short_description__icontains=query) | Q(tags__name__icontains=query)).distinct()
    paginator = Paginator(lessons, 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "lessons/category_detail.html",
        {
            "category": category,
            "page_obj": page_obj,
            "query": query,
            "meta_title": f"{category.name} Lessons - ZoPhysicist",
            "meta_description": category.description,
        },
    )


def practice_home(request):
    questions = published_questions()
    exam_cards = [
        ("jee-main", "JEE Main", "Topic-wise previous year physics questions for fast exam practice."),
        ("jee-advanced", "JEE Advanced", "Higher-order conceptual and multi-step physics problems."),
        ("neet", "NEET", "Medical entrance physics PYQs with direct solutions."),
        ("boards", "Boards", "Board-style conceptual and numerical practice."),
    ]
    return render(
        request,
        "lessons/practice_home.html",
        {
            "exam_cards": exam_cards,
            "latest_questions": questions[:6],
            "categories": Category.objects.all(),
            "meta_title": "Practice PYQ Questions - ZoPhysicist",
            "meta_description": "Practice JEE Main, JEE Advanced, NEET, and board physics questions with solutions.",
        },
    )


def practice_exam(request, exam):
    valid_exams = dict(PracticeQuestion.EXAM_CHOICES)
    if exam not in valid_exams:
        return custom_404(request, None)
    questions = published_questions().filter(exam=exam)
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    year = request.GET.get("year", "").strip()
    difficulty = request.GET.get("difficulty", "").strip()
    if query:
        questions = questions.filter(Q(title__icontains=query) | Q(question__icontains=query) | Q(solution__icontains=query)).distinct()
    if category:
        questions = questions.filter(category__slug=category)
    if year:
        questions = questions.filter(year=year)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    paginator = Paginator(questions, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    years = published_questions().filter(exam=exam).values_list("year", flat=True).distinct().order_by("-year")
    return render(
        request,
        "lessons/practice_exam.html",
        {
            "exam": exam,
            "exam_name": valid_exams[exam],
            "page_obj": page_obj,
            "categories": Category.objects.all(),
            "years": years,
            "difficulty_choices": PracticeQuestion.DIFFICULTY_CHOICES,
            "query": query,
            "selected_category": category,
            "selected_year": year,
            "selected_difficulty": difficulty,
            "meta_title": f"{valid_exams[exam]} Physics PYQ - ZoPhysicist",
            "meta_description": f"Practice {valid_exams[exam]} physics questions with answers and detailed solutions.",
        },
    )


def practice_question_detail(request, pk):
    question = get_object_or_404(published_questions(), pk=pk)
    related = published_questions().filter(category=question.category).exclude(pk=question.pk)[:4]
    return render(
        request,
        "lessons/practice_detail.html",
        {
            "question": question,
            "related_questions": related,
            "meta_title": f"{question.title} - ZoPhysicist Practice",
            "meta_description": f"{question.get_exam_display()} {question.year} physics question with detailed solution.",
        },
    )


def lab_home(request):
    labs = [
        ("lab_waves", "Wave Sandbox", "Tune amplitude, frequency, and speed to watch waves evolve."),
        ("lab_pendulum", "Pendulum Lab", "Change length, gravity, and angle to explore oscillation."),
        ("lab_lens", "Lens Simulator", "Move object and focal length to see image formation."),
        ("lab_spectrum", "Spectrum Mixer", "Mix RGB light and create glowing colors."),
    ]
    return render(
        request,
        "lessons/lab_home.html",
        {
            "labs": labs,
            "meta_title": "Physics Lab - ZoPhysicist",
            "meta_description": "Interactive physics simulations for refreshing visual exploration.",
        },
    )


def lab_waves(request):
    return render(request, "lessons/lab_waves.html", {"meta_title": "Wave Sandbox - ZoPhysicist Lab"})


def lab_pendulum(request):
    return render(request, "lessons/lab_pendulum.html", {"meta_title": "Pendulum Lab - ZoPhysicist Lab"})


def lab_lens(request):
    return render(request, "lessons/lab_lens.html", {"meta_title": "Lens Simulator - ZoPhysicist Lab"})


def lab_spectrum(request):
    return render(request, "lessons/lab_spectrum.html", {"meta_title": "Spectrum Mixer - ZoPhysicist Lab"})


def search(request):
    query = request.GET.get("q", "").strip()
    lessons = published_lessons()
    results = lessons.none()
    if query:
        results = lessons.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(full_content__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(category__name__icontains=query)
        ).distinct()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        suggestions = list(results[:6].values("title", "slug", "short_description"))
        return JsonResponse({"suggestions": suggestions})
    return render(
        request,
        "lessons/search.html",
        {
            "query": query,
            "results": results[:24],
            "meta_title": "Search Physics Lessons - ZoPhysicist",
            "meta_description": "Search modern physics lessons, articles, formulas, and visual learning resources.",
        },
    )


def about(request):
    return render(request, "lessons/about.html", {"meta_title": "About ZoPhysicist", "meta_description": "The mission behind ZoPhysicist."})


def contact(request):
    sent = request.method == "POST"
    return render(request, "lessons/contact.html", {"sent": sent, "meta_title": "Contact ZoPhysicist", "meta_description": "Contact the ZoPhysicist team."})


def custom_404(request, exception):
    return render(request, "404.html", status=404)
