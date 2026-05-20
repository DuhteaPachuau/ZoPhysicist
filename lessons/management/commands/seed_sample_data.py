from django.core.management.base import BaseCommand
from django.utils import timezone

from lessons.models import Category, FeaturedLesson, Lesson, PracticeQuestion, Tag


LESSON_BODY = """
<h2>The central idea</h2>
<p>Physics is a compression language for nature. A small model can explain a large range of observations when the variables are chosen carefully.</p>
<p>Start by asking what is conserved, what changes, and what scale matters. Most problems become calmer once those three questions are separated.</p>
<div class="formula">F = ma</div>
<h2>Build intuition</h2>
<p>Imagine tracking a system frame by frame. If motion changes, something transferred momentum. If temperature changes, energy moved. If light bends, spacetime or material structure shaped its path.</p>
<pre><code>given: known quantities
model: choose conservation law
solve: isolate the unknown
check: units and limiting cases</code></pre>
<h3>Why it matters</h3>
<p>Good physics thinking is not memorizing formulas. It is learning how to see hidden structure in motion, fields, waves, particles, heat, and information.</p>
"""


class Command(BaseCommand):
    help = "Create sample ZoPhysicist categories, tags, lessons, and featured entries."

    def handle(self, *args, **options):
        categories = [
            ("Mechanics", "Motion, forces, momentum, and energy in everyday systems.", "#55d7ff"),
            ("Quantum Physics", "Wavefunctions, uncertainty, quantization, and modern devices.", "#a66cff"),
            ("Relativity", "Space, time, gravity, and the structure of the cosmos.", "#6cf0b6"),
            ("Thermodynamics", "Heat, entropy, engines, and statistical behavior.", "#ffcf66"),
            ("Optics", "Light, lenses, interference, and imaging systems.", "#ff7bbd"),
            ("Astrophysics", "Stars, galaxies, black holes, and cosmic evolution.", "#7aa7ff"),
        ]
        category_map = {}
        for name, description, color in categories:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": description, "accent_color": color},
            )
            category.description = description
            category.accent_color = color
            category.save()
            category_map[name] = category

        tag_names = ["Beginner", "Formula", "Visual", "Deep Dive", "Conceptual", "Modern Physics"]
        tag_map = {name: Tag.objects.get_or_create(name=name)[0] for name in tag_names}

        lessons = [
            ("Newton's Laws Without the Fog", "Mechanics", "A clean guide to force, acceleration, and how to reason from free-body diagrams.", 7, True, ["Beginner", "Formula", "Conceptual"]),
            ("Energy Conservation as a Superpower", "Mechanics", "Learn when energy methods make motion problems dramatically simpler.", 6, True, ["Visual", "Formula"]),
            ("Quantum Uncertainty, Clearly Explained", "Quantum Physics", "Why uncertainty is not measurement failure, but a feature of wave-like reality.", 8, True, ["Modern Physics", "Deep Dive"]),
            ("Wavefunctions and Probability Clouds", "Quantum Physics", "A visual entry point into amplitudes, measurement, and quantum states.", 9, False, ["Visual", "Modern Physics"]),
            ("Special Relativity in One Thought Experiment", "Relativity", "Use light clocks to understand time dilation and why simultaneity is relative.", 8, True, ["Deep Dive", "Conceptual"]),
            ("Entropy Is Not Just Disorder", "Thermodynamics", "A sharper way to think about microstates, probability, and the arrow of time.", 7, False, ["Conceptual", "Deep Dive"]),
            ("Interference: When Light Adds and Cancels", "Optics", "Understand fringes, phase, and how waves reveal hidden path differences.", 5, False, ["Visual", "Beginner"]),
            ("Black Holes and Escape Velocity", "Astrophysics", "Connect Newtonian escape speed with the threshold where light cannot return.", 6, False, ["Modern Physics", "Formula"]),
            ("Fields: The Invisible Architecture", "Relativity", "Why modern physics describes influence through fields rather than distant pushes.", 7, False, ["Conceptual", "Modern Physics"]),
        ]

        created_lessons = []
        for index, (title, category_name, description, minutes, featured, tags) in enumerate(lessons):
            lesson, _ = Lesson.objects.get_or_create(
                title=title,
                defaults={
                    "category": category_map[category_name],
                    "short_description": description,
                    "full_content": LESSON_BODY,
                    "publish_date": timezone.now() - timezone.timedelta(days=index * 3),
                    "reading_time": minutes,
                    "is_featured": featured,
                },
            )
            lesson.category = category_map[category_name]
            lesson.short_description = description
            lesson.full_content = LESSON_BODY
            lesson.reading_time = minutes
            lesson.is_featured = featured
            lesson.is_published = True
            lesson.save()
            lesson.tags.set(tag_map[tag] for tag in tags)
            created_lessons.append(lesson)

        for priority, lesson in enumerate([item for item in created_lessons if item.is_featured][:4]):
            FeaturedLesson.objects.get_or_create(
                lesson=lesson,
                defaults={"headline": f"Editor's pick: {lesson.title}", "priority": priority},
            )

        practice_questions = [
            (
                "JEE Main: Work done by a constant force",
                "jee-main",
                2024,
                "Mechanics",
                "easy",
                "<p>A force of 10 N moves a body by 5 m in the direction of force. Find the work done.</p>",
                "20 J",
                "50 J",
                "5 J",
                "100 J",
                "B",
                "<p>Work done by a constant force is <strong>W = Fs cos theta</strong>. Here theta = 0, so W = 10 x 5 = 50 J.</p>",
                "W = Fs cos theta",
                "Newton's Laws Without the Fog",
            ),
            (
                "NEET: Lens formula numerical",
                "neet",
                2023,
                "Optics",
                "medium",
                "<p>An object is placed 30 cm from a convex lens of focal length 15 cm. The image distance is:</p>",
                "15 cm",
                "30 cm",
                "45 cm",
                "60 cm",
                "B",
                "<p>Using 1/f = 1/v - 1/u, with f = 15 cm and u = -30 cm, we get 1/v = 1/15 - 1/30 = 1/30, so v = 30 cm.</p>",
                "1/f = 1/v - 1/u",
                "Interference: When Light Adds and Cancels",
            ),
            (
                "JEE Advanced: Entropy change idea",
                "jee-advanced",
                2022,
                "Thermodynamics",
                "hard",
                "<p>For a reversible isothermal expansion of an ideal gas, entropy change depends on:</p>",
                "Only temperature",
                "Only pressure",
                "Volume ratio",
                "Molecular mass only",
                "C",
                "<p>For reversible isothermal expansion, Delta S = nR ln(V2/V1). It depends on the volume ratio.</p>",
                "Delta S = nR ln(V2/V1)",
                "Entropy Is Not Just Disorder",
            ),
            (
                "Boards: Escape velocity concept",
                "boards",
                2024,
                "Astrophysics",
                "medium",
                "<p>Escape velocity from a planet depends on which quantities?</p>",
                "Mass and radius of planet",
                "Mass of escaping body",
                "Temperature only",
                "Atmospheric pressure only",
                "A",
                "<p>Escape velocity is v = sqrt(2GM/R), so it depends on planet mass M and radius R.</p>",
                "v = sqrt(2GM/R)",
                "Black Holes and Escape Velocity",
            ),
        ]

        lesson_map = {lesson.title: lesson for lesson in created_lessons}
        for title, exam, year, category_name, difficulty, question, a, b, c, d, correct, solution, formula, lesson_title in practice_questions:
            item, _ = PracticeQuestion.objects.get_or_create(
                title=title,
                defaults={
                    "exam": exam,
                    "year": year,
                    "category": category_map[category_name],
                    "difficulty": difficulty,
                    "question": question,
                    "option_a": a,
                    "option_b": b,
                    "option_c": c,
                    "option_d": d,
                    "correct_option": correct,
                    "solution": solution,
                    "formula_used": formula,
                    "related_lesson": lesson_map.get(lesson_title),
                },
            )
            item.exam = exam
            item.year = year
            item.category = category_map[category_name]
            item.difficulty = difficulty
            item.question = question
            item.option_a = a
            item.option_b = b
            item.option_c = c
            item.option_d = d
            item.correct_option = correct
            item.solution = solution
            item.formula_used = formula
            item.related_lesson = lesson_map.get(lesson_title)
            item.is_published = True
            item.save()
            item.tags.set([tag_map["Formula"], tag_map["Conceptual"]])

        self.stdout.write(self.style.SUCCESS("ZoPhysicist sample data created."))
