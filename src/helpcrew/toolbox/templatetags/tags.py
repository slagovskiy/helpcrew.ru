import uuid
from django import template

register = template.Library()


@register.filter
def date_from_now(val):
    u = str(uuid.uuid4())
    return '<span id="date_' + u + '"><script>moment.locale(\'ru\');$("#date_' + u + '").html(moment("%s").fromNow());\n</script></span>' % val
