# Generated by Django 5.1.7 on 2025-05-22 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
        ('menuItemIngredients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('price', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('starters', 'Starters'), ('main_course', 'Main Course'), ('desserts', 'Desserts')], max_length=20)),
                ('image_item', models.ImageField(blank=True, null=True, upload_to='menu_images/')),
                ('ingredients', models.ManyToManyField(through='menuItemIngredients.MenuItemIngredient', to='ingredients.ingredient')),
            ],
        ),
    ]
