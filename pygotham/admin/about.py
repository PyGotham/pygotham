"""Admin for AboutPage models."""

from pygotham.admin.utils import model_view
from pygotham.about import models

__all__ = ('AboutPageModelView',)


AboutPageModelView = model_view(
    models.AboutPage,
    'About Pages',
    'About',
    column_default_sort='title',
    column_list=('title', 'navbar_section', 'event', 'active'),
    form_columns=('title', 'slug', 'navbar_section', 'content', 'event', 'active'),
)
