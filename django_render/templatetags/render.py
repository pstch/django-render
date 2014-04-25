from django import template
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template.context import Context
from django.template.loader import render_to_string

register = template.Library()

class RenderNode(template.Node):
    def __init__(self, instance, using=None, prefix='render'):
        self.instance = instance
        self.using = using
        self.prefix = prefix

    def render(self, context):
        try:
            instance = template.resolve_variable(self.instance, context)
        except template.VariableDoesNotExist:
            raise ImproperlyConfigured(
                "django-render needs a model instance to work with, no argument specified"
            )

        meta = instance._meta.app
        using = self.using
        prefix = self.prefix

        template_list = []

        def make_template_name(model_name='default',
                               using=None,
                               prefix=None,
                               app=None,
                               extension='.html'):
            return '/'.join(filter(None, [
                prefix,
                app,
                '__'.join(filter(None, [model_name, using]))
            ])) + extension

        # '<prefix>/<app>/<instance>[__<using>].html'
        template_list.append(make_template_name(
            model_name=meta.object_name.lower(),
            using=using,
            prefix=render,
            app=meta.app_label
        ))

        # '<prefix>/<app>/default[__<using>].html'
        template_list.append(make_template_name(
            model_name=meta.app_label,
            using=using,
            prefix=render
        ))

        # '<prefix>/default[__<using>].html'
        template_list.append(make_template_name(
            using=using,
            prefix=render
        ))

        # '<prefix>/default.html'
        template_list.append(make_template_name(
            prefix=render
        ))

        # We probably want access to variables added by the context processors
        # so let's copy the existing context since we might not have access
        # to the request object.
        render_context = Context()
        for dict in context.dicts:
            render_context.dicts.append(dict.copy())
        render_context['render_obj'] = instance
        rendered = render_to_string(template_list, render_context)
        return rendered

@register.tag
def render(parser, token):
    """
    Renders a model-specific template for any model instance.

    ``render`` works like a model-aware inclusion tag and is used like so::

        {% render obj %}

    Assuming ``obj`` is an instance of the ``Post`` model from the ``blog``
    application, this tag will render ``render/blog/post.html`` passing
    the second-argument to the template as ``obj``. The template name is
    ``render/[application_name]/[model_name].html`` in lower-case.

    If you'd like to use different templates in different areas of your
    site, you can do so with the ``using`` argument. For example::
znnnn
        {% render obj using long %}

    This will render the template ``render/[application_name]/[model_name]__long.html``

    In the event the necessary template cannot be found, ``render/default.html``
    will be used.

    You can also use the ``prefix`` argument to change the the prefix::

       {% render obj prefix foobar %}

    This will render the template ``foobar/[application_name]/[model_name]__long.html``

    """

    bits = token.split_contents()

    if len(bits) < 2:
        raise template.TemplateSyntaxError("%r tag takes at least 2 arguments" % bits[0])

    item = bits[1]
    args = {}
    biter = iter(bits[2:])
    for bit in biter:
        if bit == "using":
            args["using"] = biter.next()
        if bit == "prefix":
            args["prefix"] = biter.next()
        else:
            raise template.TemplateSyntaxError("%r tag got an unknown argument: %r" % (bits[0], bit))

    return RenderNode(item, **args)
