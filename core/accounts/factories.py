import factory
from factory.django import DjangoModelFactory
from accounts.models import Users

class UserFactory(DjangoModelFactory):
    class Meta:
        model = Users

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    national_code = factory.Faker('numerify', text='##########')
    phone_number = factory.Faker('phone_number')
    is_active = True
    is_verified = True
    type = Users.UserTypeModel.customer

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if create:
            self.set_password('defaultpassword')