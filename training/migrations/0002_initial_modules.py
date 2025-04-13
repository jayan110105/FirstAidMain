from django.db import migrations


def create_initial_modules(apps, schema_editor):
    Module = apps.get_model('training', 'Module')
    
    modules = [
        {
            'title': 'Allergic Reactions First Aid Quiz',
            'slug': 'allergy_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Burns First Aid Quiz',
            'slug': 'burns_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Cardiac Emergencies First Aid Quiz',
            'slug': 'cardiac_emergencies_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Choking First Aid Quiz',
            'slug': 'choking_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Cold First Aid Quiz',
            'slug': 'cold_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Fractures and Sprains First Aid Quiz',
            'slug': 'fractures_and_sprains_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Heat First Aid Quiz',
            'slug': 'heat_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Poison First Aid Quiz',
            'slug': 'poison_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Venom First Aid Quiz',
            'slug': 'venom_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
        {
            'title': 'Wounds First Aid Quiz',
            'slug': 'wounds_quiz',
            'max_score': 100,  # 5 questions × 10 points
            'passing_score': 60
        },
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