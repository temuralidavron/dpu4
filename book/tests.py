from .models import *
from django.db import connection
# connection.queries

News.objects.all()[:2] kesib olish
News.objects.order_by('pk')  tartiblash
News.objects.all().reverse teskari tartib
News.objects.filter(pk__lte=2)
News.objects.filter(pk__gte=2)
w=News.objects.get(pk=2)
w.cat
w.cat.name


#qayata aloqa qilish uchun

c=Category.objects.get(pk=2)   # modelga related_name='get_posts'
c.news_set.all()
News.objects.filter(title__contains='li')
News.objects.filter(title__icontains='LI')
News.objects.filter(pk__in=[2,3,4,5], is_published=True)
News.objects.filter(cat_id__in=[1,2])
c=Category.objects.all()
News.objects.filter(cat__in=c)
from django.db.models import Q
News.objects.filter(pk__lt=1, cat_id=2)
News.objects.filter(Q(pk__lt=1)| Q(cat_id=2))




connection.queries

from django.db.models import Q
News.objects.filter(Q(pk__lt=1) | Q(cat_id=1))
News.objects.filter(Q(pk__lt=1) & Q(cat_id=1))  AND
News.objects.filter(~Q(pk__lt=1) | Q(cat_id=1))  ne



News.objects.first()
News.objects.order_by('pk').first()
News.objects.order_by('pk').last()


News.objects.latest('time_update')
News.objects.earliest('time_update')

News.objects.order_by('pk').earliest('time_update')


m=News.objects.get(pk=2)
m.get_previous_by_time_update()
m.get_next_by_time_update()
m.get_next_by_time_update('pk__gt=2')

q=Category.objects.get(pk=3)
q.news_set.exists()
q.news_set.count()



News.objects.filter(pk__lt=10).count()


News.objects.filter(cat_slug='Jahon')



News.objects.filter(cat__name__contains='on')

Category.objects.filter(news__title__contains='mir')
Category.objects.filter(news__title__contains='mir').distinct()


News.objects.count()
News.objects.aggregate(Min('cat_id'), Max('cat_id'))
News.objects.aggregate(cat_min=Min('cat_id'), cat_max=Max('cat_id'))



News.objects.aggregate(res=Sum('cat_id') )


News.objects.aggregate(res=Avg('cat_id'))


News.objects.values('title', 'cat__name').get(pk=1)
s=News.objects.values('title', 'cat__name')
for p in s:
    print(p['title'], p['cat__name'])




k=Category.objects.annotate(Count('news'))


k[0].news__count

from django.db.models import F
News.objects.filter(pk__gt=F('cat_id'))


from django.db.models.functions import Length

ps=News.objects.annotate(len=Length('title'))
for i in ps:
    print(i.title, i.len)ca