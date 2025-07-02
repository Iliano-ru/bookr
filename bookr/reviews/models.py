from django.db import models
from django.contrib import auth


class Publisher(models.Model):
    name = models.CharField(
        max_length=50,
        help_text='The name of the Publisher'
    )
    website = models.URLField(
        help_text='The Publisher`s website'
    )
    email = models.EmailField(
        help_text='The Publisher email address'
    )
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='The title of the book'
    )
    publication_date = models.DateField(
        verbose_name='The date the book was published'
    )
    isbn = models.CharField(
        max_length=20,
        verbose_name='ISBN number of the book'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE
    )
    contributors = models.ManyToManyField(
        'Contributor',
        through='BookContributor'
    )
    def __str__(self):
        return self.title

class Contributor(models.Model):
    first_names = models.CharField(
        max_length=50,
        help_text='The first name or names'
    )
    last_names = models.CharField(
        max_length=50,
        help_text='The last name or names'
    )
    email = models.EmailField(
        help_text='The contact email for the contributor'
    )
    def __str__(self):
        return self.first_names

class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = 'AUTHOR', 'Author'
        CO_AUTHOR = 'CO_AUTHOR', 'Co-Author'
        EDITOR = 'EDITOR', 'Editor'

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    contributors = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        verbose_name='The role this contributor had in the book',
        choices=ContributionRole.choices,
        max_length=20
    )

class Review(models.Model):
    content = models.TextField(
        help_text='The Review text'
    )
    rating = models.IntegerField(
        help_text='The rating the Reviewer has given'
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text='The Date and the Review was created'
    )
    date_edited = models.DateTimeField(
        null=True,
        help_text='The date and time the Review was last edited'
    )
    creator = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
        help_text='The Creator of the Review'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        help_text='The Book that this review is for'
    )