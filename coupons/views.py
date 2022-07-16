from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
                )
            request.session['coupon_id'] = coupon.id
            messages.success(request, (
                        f"Success! {coupon} coupon applied")
                    )
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(
                request,
                "Sorry, that coupon does not exist or is no longer valid"
                )
    return redirect('view_bag')

