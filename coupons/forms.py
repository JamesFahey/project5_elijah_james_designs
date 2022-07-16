from django import forms
from coupons.models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField()

    class Meta:
        model = Coupon
        fields = ['code']

    def __init__(self, *args, **kwargs):
        super(CouponApplyForm, self).__init__(*args, **kwargs)
        self.fields['code'].label = ""
