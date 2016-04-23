---
layout: archive
title: "Physics Index"
permalink: /physics/
author_profile: true
---

{% include base_path %}

{% for post in site.categories.physics %}
  {% include archive-single.html %}
{% endfor %}
