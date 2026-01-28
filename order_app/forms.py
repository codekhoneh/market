from django import forms 
 
class CheckoutForm(forms.Form): 
    full_name = forms.CharField( 
        max_length=100, 
        label='نام و نام خانوادگی', 
        widget=forms.TextInput(attrs={ 
            'placeholder': 'تیم کد خونه'
        }) 
    ) 
    phone = forms.CharField( 
        max_length=20, 
        label='شماره تماس', 
        widget=forms.TextInput(attrs={ 
            'placeholder': '09xxxxxxxxx' 
        }) 
    ) 
 
    address = forms.CharField( 
        label='آدزس', 
        widget=forms.Textarea(attrs={ 
            'rows': 4, 
            'placeholder': 'آدرس کامل پستی' 
        }) 
    ) 
