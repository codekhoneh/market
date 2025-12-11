from django.contrib.auth.backends import ModelBackend 
from django.contrib.auth import get_user_model 
 
User = get_user_model() 
 
class EmailOrPhoneBackend(ModelBackend): 
    
    def authenticate(self, request, username=None, password=None, **kwargs): 
        user = None 
        if not username: 
            return None 
 
        # لامرن یدورو یزاس 
        username = str(username).strip() 
 
        #  ،دوب لیمیا یدورو رگا میهدن ماجنا گرزب/کچوک فورح هب تیساسح اب ار وجتسج 
        if "@" in username: 
            try: 
                user = User.objects.get(email__iexact=username) 
            except User.DoesNotExist: 
                return None 
        else: 
            # لامرن و اضف فذح( نفلت هرامش یزاس-) 
            phone = username.replace('-', '').replace(' ', '') 
            try: 
                user = User.objects.get(phone=phone) 
            except User.DoesNotExist: 
                return None 
        # روبع زمر یسررب 
        if user and user.check_password(password): 
            return user 
        return None 