from django import forms

class CouponCodeFrom(forms.Form):
    code = forms.CharField()