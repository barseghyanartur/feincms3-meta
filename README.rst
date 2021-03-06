=============
feincms3-meta
=============

Helpers and mixins for making meta and `open graph`_ tags less annoying.

Usage
=====

1. Inherit ``feincms3_meta.models.MetaMixin``
2. Optional, but recommended: Add a setting for default tags::

    META_TAGS = {
        'site_name': 'My site',
        'title': 'Default title',
        'description': (
            'The default description,'
            ' maybe long.'
        ),
        'image': '/static/app/logo.png',
    }

3. If you define ``fieldsets`` on a ``ModelAdmin`` subclass, you may
   want to use the helper ``MetaMixin.admin_fieldset()``, or maybe not.

4. Use the dictionary returned by ``feincms3_meta.utils.meta_tags`` or
   even the HTML fragment returned by
   ``feincms3_meta.utils.meta_tags_html`` in your project::

    return render(request, ..., {
        ...
        'meta_tags': meta_tags_html(
            [object],
            request=request,
        ),
    })

.. _open graph: http://ogp.me/
