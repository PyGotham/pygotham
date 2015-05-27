"""Link helpers for the admin menu."""

from flask_admin.base import MenuLink

from pygotham.admin.utils import menu_link

__all__ = ('Login', 'Logout')

# Go back to the main site. Use '/' because the view is in a completely
# different app.
Back = MenuLink('Back to Site', '/')

# Login/Logout
Login = menu_link('Login', 'security.login', False)
Logout = menu_link('Logout', 'security.logout', True)
