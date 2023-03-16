from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=150)
    product_type = models.CharField(max_length=25)
    product_description = models.TextField()
    affiliate_url = models.SlugField(blank=True, null=True)
    product_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product_name
    
class Tag(models.Model):
	tag_name = models.CharField(max_length=15)
	tag_slug = models.SlugField()
    
	def __str__(self):
		return self.tag_name
    
class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_published = models.DateTimeField('date published')
    article_image = models.ImageField(upload_to='images/')
    article_content = HTMLField()
    article_slug = models.SlugField()
    article_tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.article_title
    
class Profile(models.Model):   
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product)

	@receiver(post_save, sender=User) #add this
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User) #add this
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()


