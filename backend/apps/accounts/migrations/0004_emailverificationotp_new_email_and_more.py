# Generated for EmailVerificationOTP new_email and purpose fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_emailverificationotp'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverificationotp',
            name='new_email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='emailverificationotp',
            name='purpose',
            field=models.CharField(default='registration', max_length=20),
        ),
        migrations.AddIndex(
            model_name='emailverificationotp',
            index=models.Index(fields=['user', 'purpose', 'is_used'], name='accounts_em_user_id_c91823_idx'),
        ),
    ]

