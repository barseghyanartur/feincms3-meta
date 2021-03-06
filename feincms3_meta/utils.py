from __future__ import unicode_literals

from django.conf import settings
from django.utils.html import format_html


def meta_tags(
        objects=(),
        *,
        request,
        url_keys=('canonical', 'image', 'url'),
        **kwargs):
    """
    Return a dictionary containing meta tag information: Keys include
    (but are not limited to):

    - ``title``
    - ``description``
    - ``image`` (Full URL)
    - ``canonical`` (Full URL)
    - ``url`` (Full URL, overridden using ``canonical``)

    Data is taken in order from the following sources:

    - Any keyword arguments to this function
    - Any ``MetaMixin`` instances passed as an iterable
    - The ``META_TAGS`` setting, if available

    URLs (all keys in ``url_keys``) are passed through
    ``request.build_absolute_uri``.

    The recommended set of keys for ``META_TAGS`` is ``site_name``,
    ``title``, ``description`` and ``image``. See
    `The Open Graph protocol <http://ogp.me/>`_ for additional details.
    """
    meta = {'type': 'website'}
    meta.update(getattr(settings, 'META_TAGS', {}))

    for object in reversed(objects):
        meta['title'] = object.meta_title or object.title
        if object.meta_description:
            meta['description'] = object.meta_description
        if object.meta_image:
            meta['image'] = object.meta_image.url
        elif getattr(object, 'image', None):
            meta['image'] = object.image.url
        if object.meta_canonical:
            meta['canonical'] = object.meta_canonical
            meta['url'] = object.meta_canonical
        else:
            meta['url'] = request.get_full_path()

    meta.update(kwargs)

    for key in url_keys:
        if meta.get(key):
            meta[key] = request.build_absolute_uri(meta[key])

    return meta


def meta_tags_html(*args, **kwargs):
    meta = meta_tags(*args, **kwargs)
    template = [
        '<meta property="og:%s" content="{%s}">' % (key, key)
        for key in sorted(meta.keys())
        if key not in ('canonical',)
    ]
    template.append(
        '<meta name="description" content="{description}">'
    )
    if meta.get('canonical'):
        template.append(
            '<link rel="canonical" href="{canonical}">'
        )

    return format_html('\n  '.join(template), **meta)
