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

### 🧩 Day 6, 2025-10-24 (Friday) - In the Path of Understanding the Real Flow in Clean Architecture

#### 🧰 What I Did
- Explored how **Mappers** should behave: realized that a mapper’s role is to translate between domain entities and ORM models, not to persist data.
- Wrote the first three mappers for the first three models
- Investigated Django internals like `_prefetched_content`, understanding how Django caches preloaded relations in memory.
- Experimented with **lazy evaluation** of QuerySets, clarified when Django actually hits the database.
- Created real test data in the shell: a `LearningUnit` containing multiple `LearningBlocks`, each with several `LearningContents`.
- Investigated when and why **Repositories** and **Use Cases** should be added, and why it’s premature to implement them today.

#### 📘 What I Learned
1. **A Mapper is not a Saver and it's complicated about ManyToMany relations.**  
   Its purpose is in-memory transformation, not persistence. This separation prevents accidental side effects and aligns the ORM with the domain model cleanly. And also in a Mapper, you can’t always directly map a Domain entity to a Django model, especially with `ManyToMany` relations. The model instance must exist before Django can attach related objects. The correct approach is to create the base object first, then store related entities temporarily in a custom attribute (e.g., `_prefetched_content`) so that the data travels with the object in memory even before saving. This keeps the mapping accurate without forcing premature persistence.

2. **Django’s QuerySets are lazy, but not everything is cached.**  
   Only evaluated queries are stored, and methods like `.count()` always hit the DB (Because they are actually different SQL queries). Recognizing which operations are cached helps avoid performance traps.

3. **_prefetched_content** is Django’s internal optimization.  
   It stores preloaded related objects in memory after `prefetch_related()`, letting you iterate without extra queries. It’s a perfect example of how Django separates “data loading” from “object behavior.” Django’s `select_related` and `prefetch_related` are powerful tools for optimizing queries. They “join” related data efficiently and reducing the number of database hits greatly when navigating relationships.

4. **Clean Architecture ≠ premature abstraction.**  
   Its goal is separation of concerns, not over-engineering. You build the simplest possible working flow first, then evolve abstractions from real pain points.
  
5. - **Clean architecture path.**
    Clarified how Clean Architecture layers map to Django (Until this point I think like that! It's very very likely to change tomorrow!): 
    Interface (views) → Application (use cases) → Infrastructure (ORM) → Domain (entities).

6. **Don’t invent artificial IDs when natural uniqueness already exists.**  
    If a combination of fields (like `user_id`, `gateway_id`, and `date`) already makes a record unique, use that as a **composite key** instead of generating a fake hash or UUID.  
    Creating a synthetic ID in such cases doesn’t add clarity, it hides the natural structure of the data and introduces unnecessary complexity.  
    Good database design reflects the **real logical identity** of an entity, not an arbitrary one invented for convenience or “creativity.”


**Summary:**  
Today’s work connected architecture with reality. Instead of memorizing Clean Architecture rules, I learned *why* each boundary exists, to keep responsibilities clear, code predictable, and growth manageable. This session turned abstract “architecture talk” into an actual flow I can see, test, and extend.



### 🧩 Day 7 — 2025-10-25 (Saturday) - Ship a clean Unit Details endpoint (read path only)

#### 🧰 What I Did

- Locked the external contract (URL) first
  Decided the only scope for the first phase is GET /units/<unit_id>/. This keeps the surface area tiny and lets me verify boundary wiring end-to-end without touching behavior that depends on user progress. 

- Created a minimal, framework-thin View (Interface layer) -> UnitDetailsView.get
    parses inputs,
    calls GetUnitDetailsService.execute(unit_id),
    returns the DTO as JSON.
    No ORM, no domain logic in the view. Just request/response translation.

- Separated Application from Domain (foldering decision)
  Introduced a top-level application/ package (separate from domain/).Rationale: Application orchestrates use cases and depends on Domain, not the other way around. This preserves inward-only dependencies and allows UI/framework swaps later (templates → SPA) with minimal churn.

- Defined the Domain repository interface (unit reading path only)

- Implemented Infrastructure repository that honors the Domain repository interface
  Uses prefetch_related("blocks") to materialize the two M2M hops efficiently.

- Introduced explicit Mappers (ORM ↔ Domain), not inside the repository but inside /infrastructure
  LearningContentMapper (two-way), LearningBlockMapper (two-way) and LearningUnitMapper (today: ORM→Domain only)
  Rationale: keep Repository focused on data access while mapping stays reusable/testable and isolated.

- Clarified ordering concerns (not implemented yet by design)
  Blocks and contents are M2M. Their display order is not intrinsic to the child; it belongs to the relationship (through table). For now I read them as-is; I’ll add an order column on the through tables and then apply .order_by("through__order") (or Prefetch with an ordered queryset). A TODO is left in code to make the dependency explicit.


#### 📘 What I Learned

- Continued learning select_related vs prefetch_related, using the right tool based on the case
  select_related is only for FK/OneToOne (JOIN in a single query).
  prefetch_related is for M2M/reverse relations (separate queries + in-memory join) -> It can be used for more complicated ManyToMany relations
  With Unit→Blocks→Contents (M2M→M2M), prefetch_related("blocks__contents") is the correct, scalable approach. A single gigantic SQL JOIN is neither necessary nor desirable here; Django’s prefetch does the optimal 2–3 queries and caches them.

- Why unit_obj.__dict__ doesn’t show everything
  __dict__ stores concrete model fields; relationships are descriptors and their prefetched data lives in _prefetched_objects_cache. Seeing blocks but not contents on Unit is expected because contents isn’t a direct field on Unit; it belongs to Block.

- M2M write semantics are special
  You cannot assign a list to an M2M attribute on a model instance constructor; you must save() then call .set([...]) (or .add(...)). For read-only mapping, stash temporary data (e.g., _prefetched_contents) or keep mapping in Domain space and avoid constructing ORM objects you won’t persist.

- Abstract methods are contracts, not “optional guidance”
  Marking the Domain Repository.get_unit_by_id as @abstractmethod ensures no one can instantiate a half-implemented repo. This enforces architecture boundaries at runtime, not just in docs.

- Mapper responsibilities are directional and should be explicit
  Keep ORM → Domain and Domain → ORM paths separate to avoid accidental coupling and make tests simpler. Application will have its own Domain → DTO mapping, again in a different layer.

- URL-first thinking helps keep boundaries honest
  By committing early to GET /units/<unit_id>/ as the only delivery target, I prevented scope creep and kept the View dumb, the Use Case focused, and the Repository & Mapper well-factored.

- Verified ORM loading behavior and caching
  prefetch_related produces ~3 queries for Unit→Blocks→Contents, then uses memory cache (_prefetched_objects_cache) so subsequent block.contents.all() calls don’t hit the DB. Used reset_queries() + connection.queries to assert query counts during navigation.

- Observed that after prefetching, Django stores results in `_prefetched_objects_cache`, and if those related objects themselves have nested relationships (like other ManyToMany or ForeignKey fields also included in the same `prefetch_related` call), Django recursively fills their own `_prefetched_objects_cache` as well. When `.all()` is called, it checks these caches instead of hitting the database again. Which is smart!

- Reconfirmed why content (Which are in second connection with unit, unit has ManyToMany relation with blocks and each block has ManyToMany relation with contents) won’t appear in unit_obj.__dict__ (it’s not a direct field on Unit), whereas blocks does (it’s a declared M2M on Unit).

- Realized that in my domain layer, I shouldn’t connect entities to each other as nested Python objects (e.g., `LearningUnit` → `LearningBlock` → `LearningContent` as full objects). -> The reason is that if nested objects are stored directly, every sub-entity must be fully constructed and resolved in memory whenever a parent entity is loaded, which breaks the independence and purity of the domain layer. So I think, in the **Domain layer**, each entity should reference other entities **by their IDs**, not by direct object instances.


