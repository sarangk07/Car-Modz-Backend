from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, fullname=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            fullname=fullname,
        )
        user.is_active = True  
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fullname="superadmin", password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            fullname=fullname,
        )
        user.is_admin = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class UserData(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=150, unique=True, null=False, blank=False)
    fullname = models.CharField(max_length=80, null=True, blank=True)
    car = models.CharField(max_length=150, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_shopOwner = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def is_shop_owner(self):
        return hasattr(self, 'shopowner')


class ShopOwner(models.Model):
    user = models.OneToOneField(UserData, on_delete=models.CASCADE, related_name='shopowner')
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    shop_image = models.ImageField(upload_to='shop_images/', blank=True, null=True)
    shop_bg_img = models.ImageField(upload_to='shop_bg_images/', blank=True, null=True)
    rating = models.FloatField(
        blank=True, 
        null=True, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.shop_name if self.shop_name else "Unnamed Shop"




class Follow(models.Model):
    follower = models.ForeignKey(UserData, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(UserData, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
























class Product(models.Model):
    owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return self.product_name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    
    author = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='posts')
    author_type = models.CharField(max_length=20, choices=[('user', 'User'), ('shop_owner', 'Shop Owner')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"