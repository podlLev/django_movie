from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', 'name', 'url')
    list_display_links = ('id', 'name')


class ReviewInline(admin.TabularInline):
    """Инлайн для отзывов  на странице фильма"""
    model = Reviews
    extra = 1
    fields = (('name', 'email'), 'text', 'parent')
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='125'")

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    readonly_fields = ('get_image', )
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'), )
        }),
        ('Actors', {
            'classes': ('collapse', ),
            'fields': (('actors', 'directors', 'genres', 'category'), )
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'), )
        }),
        ('Options', {
            'fields': (('url', 'draft'), )
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.poster.url} width='150'")

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    fields = ('name', 'email', 'text', 'parent', 'movie')
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    list_display_links = ('id', 'name')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Акторы"""
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50'")

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('star', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50'")

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
