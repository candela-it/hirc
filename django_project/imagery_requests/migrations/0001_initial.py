# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestStatus'
        db.create_table(u'imagery_requests_requeststatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'imagery_requests', ['RequestStatus'])

        # Adding model 'RequestDate'
        db.create_table(u'imagery_requests_requestdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('imagery_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['imagery_requests.ImageryRequest'])),
        ))
        db.send_create_signal(u'imagery_requests', ['RequestDate'])

        # Adding model 'ImageryRequest'
        db.create_table(u'imagery_requests_imageryrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created', to=orm['auth.User'])),
            ('area_of_interest', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['imagery_requests.RequestStatus'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('project_lead', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_lead', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'imagery_requests', ['ImageryRequest'])


    def backwards(self, orm):
        # Deleting model 'RequestStatus'
        db.delete_table(u'imagery_requests_requeststatus')

        # Deleting model 'RequestDate'
        db.delete_table(u'imagery_requests_requestdate')

        # Deleting model 'ImageryRequest'
        db.delete_table(u'imagery_requests_imageryrequest')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'imagery_requests.imageryrequest': {
            'Meta': {'object_name': 'ImageryRequest'},
            'area_of_interest': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_lead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_lead'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['imagery_requests.RequestStatus']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'imagery_requests.requestdate': {
            'Meta': {'object_name': 'RequestDate'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagery_request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['imagery_requests.ImageryRequest']"}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'imagery_requests.requeststatus': {
            'Meta': {'object_name': 'RequestStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['imagery_requests']