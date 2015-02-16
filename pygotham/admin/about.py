"""Admin for AboutPage models."""

import wtforms

from pygotham.admin.utils import model_view
from pygotham.about import models

__all__ = ('AboutPageModelView',)


AboutPageModelView = model_view(
    models.AboutPage,
    'About Pages',
    'About',
    column_default_sort='title',
    column_list=('event', 'navbar_section', 'title', 'active'),
    form_columns=('event', 'navbar_section', 'title', 'content', 'active'),
)
