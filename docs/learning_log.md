# 🧠 Learning Log — [Leaning_APP]

## 📘 Overview
- **Purpose:** Continuous reflection on what I learn technically and conceptually.
- **Start Date:** 2025-10-22
- **Format:** Daily entries combining technical notes and personal reflection.

---

## 🗓️ Daily Entries
She go to school every day.

### 🧩 Day 0 — 2025-10-21 (Tuesday)

**🧰 What I Did**
- Set up `django-stubs` and `mypy` configuration.
- Fixed VSCode integration for type checking.

**📘 What I Learned**
- Mypy doesn’t infer Django field types unless plugin is loaded.
- Learned how async doesn’t help with CPU-bound tasks — it’s for I/O only.

**⚠️ Challenges / Mistakes**
- Tried annotating model fields manually — caused duplicate type inference.
- Misconfigured `django_settings_module`.

**💡 Insights**
- The best debugging strategy is to start from assumptions, not symptoms.
- Tooling problems often reveal weak mental models, not weak syntax.

**🎯 Next Focus**
- Write clean `mypy.ini` guide for future projects.
- Explore difference between sync worker and async event loop.

---

### 🧩 Day 2 — 2025-10-23

**🧰 What I Did**
- Refactored `LearningContentModel` to use Enum for state choices.
- Added proper type hints to all model methods.

**📘 What I Learned**
- Using `models.CharField[str, str]` with django-stubs ensures correct typing.
- `auto_now_add` generates timestamps on save, not on instance creation.

**⚠️ Challenges / Mistakes**
- Accidentally imported Enum inside model — circular import issue.
- Needed to move `LearnableState` to a separate module.

**💡 Insights**
- The real cost of clean architecture is *discipline*, not code lines.
- Explicitness in type hints helps you reason about time and state.

**🎯 Next Focus**
- Implement async task dispatcher in FastAPI.
- Start exploring event-driven design.

---

## 📊 Weekly Reflection (Optional)

| Week | Key Learnings | Mistakes | Improvements |
|------|----------------|----------|---------------|
| 1 | Django type inference, async vs CPU | Circular imports | Better layering between domain and infra |

---

## 🧩 Meta
- **Tool:** VS Code + Poetry  
- **Language:** Python 3.13  
- **Frameworks:** Django 5.2, FastAPI  
- **Last Updated:** 2025-10-22
