---
title: "{{ data.title }}"
date: {{ date }}
category: {{ data.category }}
tags: {{ data.tags | tojson }}
{% if data.due_date %}due_date: {{ data.due_date }}{% endif %}
---

# {{ data.title }}

{{ data.summary }}

{% if data.tasks %}
## ✅ Задачи
{% for task in data.tasks %}
- [ ] {{ task }}
{% endfor %}
{% endif %}

{% if data.entities %}
## 🔗 Связи
{% for entity in data.entities %}
- [[{{ entity }}]]
{% endfor %}
{% endif %}