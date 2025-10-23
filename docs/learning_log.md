# 🧠 Learning Log - [Leaning_APP]

## 📘 Overview
- **Purpose:** Continuous reflection on what I learn technically and conceptually.
- **Start Date:** 2025-10-22
- **Format:** Daily entries combining technical notes and personal reflection.

---

## 🗓️ Daily Entries

### 🧩 Days 1–4 - October 19–22, 2025 - Before the creation of **learning_log.md**!

#### 🧰 What I Did

- Reviewed the concept of **Clean Architecture** and studied how it could be practically applied in Django projects.  
  I explored examples of folder structures, module organization, and the correct way to isolate the domain layer.  
  Then I started writing **domain models**, keeping them as pure Python classes without any framework dependencies.

- After completing the first version of the domain models, I continued researching Clean Architecture and learned how the **infrastructure layer** should interact with the domain.  
  I implemented the first version of the **infrastructure (database) models** to represent persistence logic.

- Began sketching initial **C4 model diagrams** for the project on paper.  
  The goal was to visualize how the system components will connect later.  
  I plan to refine and upload these diagrams once the system’s structure becomes clearer.

- Ensured that the **infrastructure layer** never creates or manipulates data that the domain layer does not define or control.  
  This was based on the principle that the domain should remain the only source of truth.

- Studied how the **Mapping layer** links domain entities with database models in Django.  
  I explored different ways to keep both layers synchronized and identified where integration tests will be most useful.

- Decided to implement **type hints** throughout the project.  
  I read the official Python documentation on typing, studied **TypeVar** and **Generics**, and learned how they make code safer even when the exact type is not known in advance.

- Faced issues with **type hints in Django**.  
  Pylance in VSCode could not infer model field types because Django defines them dynamically.  
  I looked into community discussions to understand the reason and test different solutions.  
  This effort continued until October 22, when I successfully configured **django-stubs** and **mypy** to make static type checking work correctly.


#### 📘 What I Learned

- The **domain layer** should always be pure Python, with no framework imports. This keeps the business logic independent and portable.  
- The **infrastructure layer** is responsible for implementing data storage and external interfaces but must never become the source of truth.  
- The **mapping layer** ensures the domain and infrastructure stay consistent. A mismatch here should immediately raise an error.  
- The **C4 model** is a useful tool for visualizing architecture, but it becomes more valuable after the first implementation steps when system boundaries are clearer.  
- Proper **type hinting** with `mypy` and `django-stubs` improves safety and clarity but requires careful setup.  
- Django’s dynamic nature creates challenges for type checking, and solving them helps deepen understanding of how Django and Python interact internally.  
- Writing **tests early** for the mapping and infrastructure layers will help catch structural errors before they grow into architectural problems.  
- Combining theory with small, real implementations clarified many abstract concepts that were difficult to grasp before.

---
---

### 🧩 Day 4 - 2025-10-22 (Wednesday) - Tedious things just started

#### 🧰 What I Did

- Set up `django-stubs` and `mypy` configuration. Fixed VSCode integration for type checking, mainly because **Pylance** isn't very efficient with Django in VSCode.  
- Installed **Code Spell Checker** by *Street Side Software*, a simple yet useful spelling checker for VSCode. It doesn’t fix grammar, but for non-native English speakers, it’s still a great help.  
- Created supporting documentation files:  
  - `learning_log.md` -> this file itself  
  - `./docs/ADRs` -> for architectural decision records  
  - `./notes` -> personal notes (added to `.gitignore`)  
  - `changelog.md` -> for project-wide change tracking  


#### 📘 What I Learned

##### 1. MyPy doesn’t infer Django field types unless the plugin is loaded

Setting up these tools can be a bit tricky, so here’s the exact process I followed 👇  

<details>
<summary><strong>Click to expand the full setup guide</strong></summary>

**Step 1 – Install the required packages**

```bash
poetry add -D mypy django-stubs mypy-extensions
```

**Step 2 – Create a `mypy.ini` file**  
In the project root, create a file named `mypy.ini` with the following content:

```ini
[mypy]
plugins = mypy_django_plugin.main
ignore_missing_imports = True
disallow_untyped_defs = True
strict_optional = True

[mypy.plugins.django-stubs]
django_settings_module = "your_project.settings"
```

**Step 3 – Verify that MyPy is working correctly**

Run this command in your terminal:
```bash
poetry run mypy --show-traceback --show-error-codes your_app/models.py
```

If everything is set up properly, you should see:
```
Success: no issues found in 1 source file
```

**Step 4 – Verify your Python interpreter in VSCode**

Press `Ctrl + Shift + P`, type **Python: Select Interpreter**, and make sure it matches the environment shown by:
```bash
poetry env info --path
```

**Step 5 – Check VSCode’s MyPy integration**

Open `.vscode/settings.json` and ensure these lines exist:
```json
{
  "mypy-type-checker.importStrategy": "fromEnvironment",
  "mypy-type-checker.args": ["--config-file", "mypy.ini"]
}
```

If everything is correct, MyPy type checking should now work seamlessly inside VSCode. 🎉

</details>

---

##### 2. Async doesn’t help with CPU-bound tasks, it’s for I/O operations only

I explored how Python’s async model works and where it makes sense to use it.  
Async helps when tasks wait for external resources (like APIs, DB queries, or files).  
It doesn’t speed up CPU-heavy code, that’s where **multi-processing**, **workers**, or **thread pools** come in.  

I also reviewed how frameworks like **Celery** manage background tasks, and how combining Django (for HTTP and persistence) with **FastAPI** (for async micro-tasks) can improve responsiveness.  

For example, you could:  
- Let Django handle incoming requests quickly.  
- Offload longer tasks to FastAPI via Redis (acting as a short-term state store).  
- Use Redis so Django can quickly return “waiting” responses, then update once results arrive, keeping Django as the single source of truth.  

---

##### 3. Keeping a `learning_log.md` and `changelog.md` is worth it

Maintaining clear documentation files helps track both **technical progress** and **personal growth**.  
`learning_log.md` captures your reasoning and discoveries; `changelog.md` keeps product evolution transparent.  
Together, they make your repository much more professional, something senior engineers always value.


### 🧩 Day 5 - 2025-10-23 (Thursday) - Mappers & App Setup

#### 🧰 What I Did

- Added the new `infrastructure.django_app` to the Django settings and configured its `AppConfig`.
- Created the initial migration for the app and registered the models in the Django admin to ensure that the database and admin interface were working correctly.
- Researched in depth how **mappers** should be implemented in Django projects following the **Clean Architecture** approach.
  I specifically compared two approaches:
  1. Defining mapper logic *inside* Django ORM models (e.g., `to_domain()` / `from_domain()` methods inside `infrastructure/models.py`)
  2. Keeping all mappers in a **separate module** such as `infrastructure/mappers.py`
- Started to Implement the first version of `mappers.py` to handle conversions between ORM models (`LearningUnitModel`, `LearningBlockModel`, `LearningContentModel`) and their corresponding Domain entities.
- The goal was to build a fully working data flow for these three models to understand how data travels across layers in a Clean Architecture system.

---

#### 📘 What I Learned

- Keeping mappers **outside** of ORM models is a much cleaner and more maintainable design choice, because it **preserves the separation of concerns** between persistence and domain logic.    
  This coupling makes testing harder which is especially important for me, because I don’t need to run the entire Django environment just to test the mapper functions that happen to live inside Django classes, which I think can make CI tests longer without adding something valuable. It also breaks the single responsibility principle.  
  By extracting mappers into their own module changes can be localized.
- Each class should have **one clear responsibility (SRP)**, ORM models already handle persistence, so they shouldn’t also manage domain conversion.
- By isolating mapper logic in a dedicated file:
  - The code becomes easier to test independently.
  - The structure naturally scales as the project grows.
- This exercise helped clarify how Clean Architecture separates responsibilities and how each layer communicates through explicit, testable boundaries.


---
---
