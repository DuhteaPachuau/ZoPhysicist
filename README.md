# ZoPhysicist

ZoPhysicist is a complete Django-powered educational website for publishing premium physics lessons and scientific articles. There is no public login or registration flow. Lessons, categories, tags, cover images, and featured content are managed through the Django admin panel.

## Features

- Django backend with `Lesson`, `Category`, `Tag`, and `FeaturedLesson` models
- Admin panel for creating, editing, deleting, featuring, and organizing lessons
- Home, lesson detail, category, search, about, contact, and custom 404 pages
- Practice/PYQ section for JEE Main, JEE Advanced, NEET, and board-style physics questions
- Admin-managed practice questions with exam, year, chapter, difficulty, options, answer, formula, solution, tags, and related lesson
- Responsive mobile-first UI using custom HTML, CSS, and JavaScript
- Sticky navbar, right-side mobile drawer, dark/light mode, scroll reveal, progress bar, table of contents, live search suggestions, share buttons, answer reveal, and scroll-to-top
- SEO and Open Graph metadata, favicon, lazy images, semantic HTML, and accessible labels

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_sample_data
python manage.py createsuperuser
python manage.py runserver
```

Open the site at:

```text
http://127.0.0.1:8000/
```

Open the admin panel at:

```text
http://127.0.0.1:8000/admin/
```

Open the Practice/PYQ section at:

```text
http://127.0.0.1:8000/practice/
```

## Editing Lessons

In Django admin, create or edit lessons under `Lessons`. The `full_content` field includes a simple rich editor with buttons for headings, paragraphs, bold, italic, lists, links, formulas, code, and images.

Use `H2` and `H3` headings for lesson sections. Those headings automatically appear in the public lesson page `Contents` dropdown.

You can also switch to HTML view and write HTML directly, including:

```html
<h2>Section title</h2>
<p>Lesson paragraph.</p>
<div class="formula">E = mc^2</div>
<pre><code>formula or code notes</code></pre>
```

Cover images can be uploaded from the admin panel. If no cover image is provided, the site displays a generated futuristic lesson cover.

## Practice / PYQ Questions

In Django admin, create or edit questions under `Practice questions`. Each question includes:

- Exam type: JEE Main, JEE Advanced, NEET, or Boards
- Year, category/chapter, difficulty, and tags
- Question text and four options
- Correct answer
- Detailed solution and formula used
- Optional related lesson

Published questions appear on the Practice pages and can be filtered by exam, chapter, year, and difficulty.

## Project Structure

```text
zophysicist/
lessons/
templates/
static/
media/
requirements.txt
manage.py
README.md
```
