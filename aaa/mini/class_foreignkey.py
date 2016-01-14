#coding:utf-8
from django.db import models
import datetime
from models import Fileinfo_up,Fileinfo_down

	

class UserForeignKey_FileUp(models.ForeignKey):
	def __init__(self, to_field=None, **kwargs):
		super(UserForeignKey_FileUp, self).__init__(Fileinfo_up, to_field=to_field, **kwargs)

class UserForeignKey_FileDw(models.ForeignKey):
	def __init__(self, to_field=None, **kwargs):
		super(UserForeignKey_FileDw, self).__init__(Fileinfo_down, to_field=to_field, **kwargs)












