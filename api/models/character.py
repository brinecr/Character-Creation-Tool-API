from django.db import models

from .user import User

# Create your models here.
class Character(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  hit_points = models.IntegerField(default='10')
  attack_power = models.IntegerField(default='4')
  dead = models.BooleanField(default=False)
  description = models.CharField(max_length=100)
  monsters_killed = models.IntegerField(default='0')
  owner = models.ForeignKey(
      User,
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The character named '{self.name}' is described as  '{self.description}'. They have {self.hit_points} hit points. They have {self.attack_power} attack power. It is {self.dead} that they are dead. They have killed {self.monsters_killed} monsters."

  def as_dict(self):
    """Returns dictionary version of Character models"""
    return {
        'id': self.id,
        'name': self.name,
        'dead': self.dead,
        'description': self.description,
        'hit_points': self.hit_points,
        'attack_power': self.attack_power,
        'monsters_killed': self.monsters_killed
    }
