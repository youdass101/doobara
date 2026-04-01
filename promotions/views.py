from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .services import remove_coupon_from_session, set_coupon_feedback, store_coupon_in_session


@require_POST
def apply_coupon(request):
    form = CouponApplyForm(request.POST)
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/cart"
    if not form.is_valid():
        set_coupon_feedback(request, "Please enter a valid coupon code.", "error")
        return redirect(next_url)

    store_coupon_in_session(request, form.cleaned_data["code"])
    set_coupon_feedback(request, "Coupon code was applied and will be validated against your cart.", "success")
    return redirect(form.cleaned_data.get("next") or next_url)


@require_POST
def remove_coupon(request):
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/cart"
    remove_coupon_from_session(request)
    set_coupon_feedback(request, "Coupon removed.", "success")
    return redirect(next_url)
