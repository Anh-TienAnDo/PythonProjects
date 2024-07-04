import re
from .models import Account, Address, Name, User
from .serializers import UserSerializer, NameSerializer, AccountSerializer, AddressSerializer

class UserValidation:
    def __init__(self, data):
        self.data = data
        self.validation_errors = {}

    def validate_username(self):
        username = self.data.get('username')
        if not username:
            self.validation_errors['username'] = 'Username is required'
        elif not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', username):
            self.validation_errors['username'] = "Username phải bắt đầu bằng chữ cái và chỉ chứa chữ cái và số."
        
    def check_username_exist(self):
        username = self.data.get('username')
        if Account.objects.filter(username=username).exists():
            self.validation_errors['username'] = "Username đã tồn tại."
        
    def validate_email(self):
        email = self.data.get('email')
        if not email:
            self.validation_errors['email'] = "Email không được để trống."
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.validation_errors['email'] = "Email không hợp lệ."
    
    def check_email_exist(self):
        email = self.data.get('email')
        if Account.objects.filter(email=email).exists():
            self.validation_errors['email'] = "Email đã tồn tại."

    def validate_phone(self):
        phone = self.data.get('phone')
        if not phone:
            self.validation_errors['phone'] = "Phone không được để trống."
        elif len(phone) != 10:
            self.validation_errors['phone'] = "Phone phải có 10 ký tự."
        elif not phone.isdigit():
            self.validation_errors['phone'] = "Phone chỉ được chứa ký tự số."

    def validate_street(self):
        street = self.data.get('street')
        if not street:
            self.validation_errors['street'] = "Street không được để trống."
    
    def validate_district(self):
        district = self.data.get('district')
        if not district:
            self.validation_errors['district'] = "District không được để trống."
    
    def validate_city(self):
        city = self.data.get('city')
        if not city:
            self.validation_errors['city'] = "City không được để trống."

    def validate_fname(self):
        fname = self.data.get('fname')
        if fname and not re.match(r'^[a-zA-Z0-9\s]+$', fname):
            self.validation_errors['fname'] = "First name chỉ được chứa ký tự chữ, số và dấu space."
    
    def validate_lname(self):
        lname = self.data.get('lname')
        if lname and not re.match(r'^[a-zA-Z0-9\s]+$', lname):
            self.validation_errors['lname'] = "Last name chỉ được chứa ký tự chữ, số và dấu space."

    def check_old_password(self):
        username = self.data.get('username')
        old_password = self.data.get('old_password')
        account = Account.objects.get(username=username)
        if account.check_password(old_password) == False:
            self.validation_errors['old_password'] = "Old password không đúng."

    def validate_password(self):
        password = self.data.get('password')
        if not password:
            self.validation_errors['password'] = "Password không được để trống."
        elif len(password) < 8:
            self.validation_errors['password'] = "Password phải có ít nhất 8 ký tự."
        elif not any(c.isupper() for c in password):
            self.validation_errors['password'] = "Password phải chứa ít nhất 1 ký tự in hoa."
        elif not any(c.islower() for c in password):
            self.validation_errors['password'] = "Password phải chứa ít nhất 1 ký tự in thường."
        elif not any(c.isdigit() for c in password):
            self.validation_errors['password'] = "Password phải chứa ít nhất 1 số."

    def validate_2password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        self.validate_password()
        if (not self.validation_errors) and password != confirm_password:
            self.validation_errors['password'] = "Confirm Password phải giống Password."
        
    def validate_data_register(self):
        self.validate_username()
        self.validate_password()
        self.validate_email()
        self.validate_fname()
        self.validate_lname()
        self.validate_2password()
        self.check_username_exist()
        self.check_email_exist()
        return self.validation_errors
    
    def validate_data_login(self):
        self.validate_username()
        self.validate_password()
        return self.validation_errors
    
    def validate_data_update(self):
        self.validate_username()
        self.validate_email()
        self.validate_phone()
        self.validate_street()
        self.validate_district()
        self.validate_city()
        self.validate_fname()
        self.validate_lname()
        return self.validation_errors
    
    def validate_data_change_password(self):
        self.check_old_password()
        self.validate_password()
        self.validate_2password()
        return self.validation_errors
 
def check_user_login(data):
    user_validation = UserValidation(data)
    validation_errors = user_validation.validate_data_login()
    if validation_errors:
        return  {
                    'status'     : 'Failed',
                    'status_code': '400',
                    'message'    : validation_errors
                }
    else:
        username = data['username']
        password = data['password']
        account = Account.objects.filter(username=username).first()
        if account is None and account.check_password(password) == False:
            return {
                    'status'     : 'Failed',
                    'status_code': '400',
                    'message'    : 'Username or password is incorrect'
                }
        return {
                    'status'     : 'Success',
                    'status_code': '200',
                    'message'    : 'Login successfully',
                    'account'       :  AccountSerializer(account).data
                }
    
class UserAction():

    def __innit__(self):
        pass

    def create_user(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        fname = data.get('fname')
        lname = data.get('lname')

        account = Account.objects.create(
            username=username,
            email=email,
        )
        account.set_password(password)
        account.save()

        name = Name.objects.create(
            fname=fname,
            lname=lname
        ); name.save() 

        user = User.objects.create(
            account=account,
            name=name
        ); user.save()

        return True

    def update_user(self, data):
        username = data.get('username')
        email = data.get('email')
        fname = data.get('fname')
        lname = data.get('lname')
        phone = data.get('phone')
        street = data.get('street')
        district = data.get('district')
        city = data.get('city')

        account = Account.objects.get(username=username).update(
            username=username,
            email=email,
        ); account.save()
        
        user = User.objects.get(account__username=username)

        try:
            address = Address.objects.get(user=user)
            address.street = street
            address.district = district
            address.city = city
            address.phone = phone
        except Address.DoesNotExist:
            address = Address.objects.create(
                user=user,
                street=street,
                district=district,
                city=city,
                phone=phone
            )
        address.save()

        name = Name.objects.get(id=user.name.id).update(
            fname=fname,
            lname=lname
        ); name.save()

        return True

    def change_password(self, data):
        username = data.get('username')
        password = data.get('password')

        account = Account.objects.get(username=username)
        account.set_password(password)
        account.save()
        return True
    
    def delete_user(self, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return True

def create_user(data):
    user_validation = UserValidation(data)
    validation_errors = user_validation.validate_data_register()
    if validation_errors:
        return  {
                    'status'     : 'Failed',
                    'status_code': '400',
                    'message'    : validation_errors
                }
    user_action = UserAction()
    result = user_action.create_user(data)
    if result:
        return {
                    'status'     : 'Success',
                    'status_code': '200',
                    'message'    : 'Register successfully'
                } 

def update_user(data):
    user_validation = UserValidation(data)
    validation_errors = user_validation.validate_data_update()
    if validation_errors:
        return  {
                    'status'     : 'Failed',
                    'status_code': '400',
                    'message'    : validation_errors
                }
    user_action = UserAction()
    result = user_action.update_user(data)
    if result:
        return {
                    'status'     : 'Success',
                    'status_code': '200',
                    'message'    : 'Update successfully'
                }
    
def change_password_user(data):
    user_validation = UserValidation(data)
    validation_errors = user_validation.validate_data_change_password()
    if validation_errors:
        return  {
                    'status'     : 'Failed',
                    'status_code': '400',
                    'message'    : validation_errors
                }
    user_action = UserAction()
    result = user_action.change_password(data)
    if result:
        return {
                    'status'     : 'Success',
                    'status_code': '200',
                    'message'    : 'Change password successfully'
                }
    
def delete_user(user_id):
    user_action = UserAction()
    result = user_action.delete_user(user_id)
    if result:
        return {
                    'status'     : 'Success',
                    'status_code': '200',
                    'message'    : 'Delete user successfully'
                }
    

