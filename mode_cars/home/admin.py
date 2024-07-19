from django.contrib import admin
from .models import UserData, ShopOwner, Product, Post, Comment, Like,Follow

admin.site.register(UserData)
admin.site.register(ShopOwner)
admin.site.register(Product)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)