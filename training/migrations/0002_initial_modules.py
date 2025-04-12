from django.db import migrations


def create_initial_modules(apps, schema_editor):
    Module = apps.get_model('training', 'Module')
    
    modules = [
        {
            'title': 'Allergic Reactions First Aid Quiz',
            'slug': 'allergy_quiz',
            'max_score': 200,  # 5 questions × 10 points
            'passing_score': 30
        },
        # Add other modules here
    ]
    
    for module_data in modules:
        Module.objects.create(**module_data)


class Migration(migrations.Migration):
    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_modules),
    ]