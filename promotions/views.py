from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .services import remove_coupon_from_session, set_coupon_feedback, store_coupon_in_session


def _get_safe_redirect_url(request, candidate_url):
    # Guard user-controlled redirect targets (next/referer) to avoid open redirects.
    # We only allow local URLs on the current host (or configured allowed hosts).
    if candidate_url and url_has_allowed_host_and_scheme(
        candidate_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate_url
    return "/cart"


@require_POST
def apply_coupon(request):
    form = CouponApplyForm(request.POST)
    next_url = _get_safe_redirect_url(
        request, request.POST.get("next") or request.META.get("HTTP_REFERER")
    )
    if not form.is_valid():
        set_coupon_feedback(request, "Please enter a valid coupon code.", "error")
        return redirect(next_url)

    store_coupon_in_session(request, form.cleaned_data["code"])
    set_coupon_feedback(request, "Coupon code was applied and will be validated against your cart.", "success")
    return redirect(_get_safe_redirect_url(request, form.cleaned_data.get("next") or next_url))


@require_POST
def remove_coupon(request):
    next_url = _get_safe_redirect_url(
        request, request.POST.get("next") or request.META.get("HTTP_REFERER")
    )
    remove_coupon_from_session(request)
    set_coupon_feedback(request, "Coupon removed.", "success")
    return redirect(next_url)
