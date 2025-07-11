from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    @admin.display(
        ordering='isbn',
        description='ISBN-13',
        empty_value='-/-'
    )
    def isbn13(self):
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(self.isbn[0:3],
                                       self.isbn[3:4], self.isbn[4:6],
                                       self.isbn[6:12], self.isbn[12:13])

    date_hierarchy = 'publication_date'
    list_display = ('title', isbn13)
    list_filter = ('publisher', 'publication_date')
    search_fields = ('title', 'isbn')


# Register your models here.
admin.site.register(Publisher)
admin.site.register(Contributor)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review)