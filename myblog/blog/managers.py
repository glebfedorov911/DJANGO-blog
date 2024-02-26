from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email or not phone:
            return ValueError("Заполните обязательные поля")

        if email and phone:
            email = self.normalize_email(email)

            user = self.model(
                email=email,
                phone=phone,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        return self._create_user(
            email=email,
            phone=phone,
            password=password,
            **extra_fields
        )

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError("You're not a superuser")

        return self._create_user(
            email=email,
            phone=phone,
            password=password,
            **extra_fields
        )