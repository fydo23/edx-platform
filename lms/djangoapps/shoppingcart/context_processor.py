"""
This is the shoppingcart context_processor module.
Currently the only context_processor detects whether request.user has a cart that should be displayed in the
navigation.  We want to do this in the context_processor to
1) keep database accesses out of templates (this led to a transaction bug with user email changes)
2) because navigation.html is "called" by being included in other templates, there's no "views.py" to put this.
"""
from django.conf import settings
import shoppingcart
from microsite_configuration import microsite


def user_has_cart_context_processor(request):
    """
    Checks if request has an authenticated user.  If so, checks if request.user has a cart that should
    be displayed.  Anonymous users don't.
    Adds `display_shopping_cart` to the context
    """
    display_shopping_cart = (
        # user is logged in and
        request.user.is_authenticated() and
        # settings enable paid course reg
        microsite.get_value(
            'ENABLE_PAID_COURSE_REGISTRATION',
            settings.FEATURES.get('ENABLE_PAID_COURSE_REGISTRATION')
        ) and
        # settings enable shopping cart
        microsite.get_value(
            'ENABLE_SHOPPING_CART',
            settings.FEATURES.get('ENABLE_SHOPPING_CART')
        ) and
        # user's cart has PaidCourseRegistrations
        shoppingcart.models.Order.user_cart_has_items(
            request.user,
            [shoppingcart.models.PaidCourseRegistration, shoppingcart.models.CourseRegCodeItem]
        )
    )

    return {'display_shopping_cart': display_shopping_cart}
