# Generated by Django 2.1.1 on 2019-01-21 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0002_article_edit_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_flag', models.BooleanField(default=False, verbose_name='是否被删除')),
                ('delete_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('open_code', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('content', models.CharField(default='', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleCommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_flag', models.BooleanField(default=False, verbose_name='是否被删除')),
                ('delete_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('open_code', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('content', models.CharField(default='', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LikeArticleRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('article_id', models.IntegerField()),
                ('like_datetime', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='comment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='like',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='visit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='articlecommentreply',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reply_article_comment_set', to='article.Article'),
        ),
        migrations.AddField(
            model_name='articlecommentreply',
            name='comment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_in_comment_reply_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articlecommentreply',
            name='original_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reply_comment_set', to='article.ArticleComment'),
        ),
        migrations.AddField(
            model_name='articlecommentreply',
            name='reply_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_article_comment_reply_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_article_set', to='article.Article'),
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_article_comment_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
