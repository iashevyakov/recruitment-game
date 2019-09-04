from django.core.validators import MinValueValidator, RegexValidator
from django.db import models



class Planet(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Sith(models.Model):
    planet = models.ForeignKey(Planet, related_name='planet_siths', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, validators=[
        RegexValidator('^[A-Z][a-z]{2,}$', 'Name must contain only letters (at least 3, 1st - uppercase)',
                       'invalid_name')])

    def __str__(self):
        return "%s (%s)" % (self.name, self.planet)

    class Meta:
        unique_together = (('planet', 'name'),)


class Recruit(models.Model):
    planet = models.ForeignKey(Planet, related_name='planet_recruits', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, validators=[
        RegexValidator('^[A-Z][a-z]{2,}$', 'Name must contain only letters (at least 3, 1st - uppercase)',
                       'invalid_name')])
    age = models.IntegerField(validators=[MinValueValidator(0, 'Age must be a positive number!')])
    email = models.EmailField()
    sith = models.ForeignKey(Sith, related_name='shadow_hands', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.planet)

    class Meta:
        unique_together = (('planet', 'name'),)


class Question(models.Model):
    text = models.TextField(unique=True)

    def __str__(self):
        return self.text


class Test(models.Model):
    order_code = models.CharField(max_length=20, unique=True)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.order_code


class Answers(models.Model):
    recruit = models.ForeignKey(Recruit, related_name='recruit_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question_recruit_answers', on_delete=models.CASCADE)
    answer = models.BooleanField()

    def __str__(self):
        return '%s : %s - %s' % (self.recruit, self.question, self.answer)

    class Meta:
        unique_together = (('recruit', 'question'),)
