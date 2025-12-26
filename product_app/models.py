from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError 


class Product(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    image = models.ImageField(upload_to='product_image')
    
    size = models.ManyToManyField('Size', related_name='products', blank=True)
    color = models.ManyToManyField('Color', related_name='products', blank=True)
    
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        return self.price - (self.price * self.discount / 100)
    
    def clean(self):
        if not 0 <= self.discount <= 100:
            raise ValidationError("درصد تخفیف باید بین 0 تا 100 باشد.")
    
    def short_description(self):
        return self.description[:80] + "..."
    
class Size(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    
    @property
    def sizes_list(self):
        return [size.title for size in self.size.all()]
    
    @property
    def price_display(self):
        return f"{self.price:,}"

    @property
    def final_price_display(self):
        return f"{self.final_price:,}"

class Color(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    
    @property
    def colors_list(self):
        return [color.title for color in self.color.all()]
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')
    alt_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.product.title} Image"


# --------------------------------Comment---------------------------------

from django.conf import settings

class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    text = models.TextField()

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_comments",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.product.title}"

    def likes_count(self):
        return self.likes.count()

class  Information(models.Model)    : 
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='informations',null=True) 
    text=models.TextField() 
    def __str__(self): 
        return self.text[:30] 








