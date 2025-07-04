SELECT id, name, email
FROM users
WHERE 1=1
{% if name %}
  AND name LIKE :name
{% endif %}
{% if email %}
  AND email LIKE :email
{% endif %}
ORDER BY id DESC
LIMIT :limit OFFSET :offset
