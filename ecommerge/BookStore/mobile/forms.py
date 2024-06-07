from django import forms
from .models import *

class MobileAdminForm(forms.ModelForm):
    class Meta:
        model = Phone
        #  tất cả các trường của model Phone
        fields = '__all__'
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.') #thông báo lỗi
        return self.cleaned_data['price']