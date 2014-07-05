# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProviderStatus'
        db.create_table(u'providers_providerstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'providers', ['ProviderStatus'])

        # Adding model 'Provider'
        db.create_table(u'providers_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['imagery_requests.CustomUser'], null=True, blank=True)),
        ))
        db.send_create_signal(u'providers', ['Provider'])

        # Adding model 'ProviderResponse'
        db.create_table(u'providers_providerresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imagery_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['imagery_requests.ImageryRequest'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['providers.ProviderStatus'])),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['providers.Provider'])),
        ))
        db.send_create_signal(u'providers', ['ProviderResponse'])

        # Adding unique constraint on 'ProviderResponse', fields ['imagery_request', 'status', 'provider']
        db.create_unique(u'providers_providerresponse', ['imagery_request_id', 'status_id', 'provider_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProviderResponse', fields ['imagery_request', 'status', 'provider']
        db.delete_unique(u'providers_providerresponse', ['imagery_request_id', 'status_id', 'provider_id'])

        # Deleting model 'ProviderStatus'
        db.delete_table(u'providers_providerstatus')

        # Deleting model 'Provider'
        db.delete_table(u'providers_provider')

        # Deleting model 'ProviderResponse'
        db.delete_table(u'providers_providerresponse')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'imagery_requests.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'imagery_requests.imageryrequest': {
            'Meta': {'object_name': 'ImageryRequest'},
            'area_of_interest': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created'", 'to': u"orm['imagery_requests.CustomUser']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questions.QuestionSet']", 'null': 'True'}),
            'request_lead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'request_lead'", 'null': 'True', 'to': u"orm['imagery_requests.CustomUser']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['imagery_requests.RequestStatus']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'imagery_requests.requeststatus': {
            'Meta': {'object_name': 'RequestStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'providers.provider': {
            'Meta': {'object_name': 'Provider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['imagery_requests.CustomUser']", 'null': 'True', 'blank': 'True'})
        },
        u'providers.providerresponse': {
            'Meta': {'unique_together': "(('imagery_request', 'status', 'provider'),)", 'object_name': 'ProviderResponse'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagery_request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['imagery_requests.ImageryRequest']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': u"orm['providers.Provider']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['providers.ProviderStatus']"})
        },
        u'providers.providerstatus': {
            'Meta': {'object_name': 'ProviderStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        u'questions.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'questions.questionset': {
            'Meta': {'object_name': 'QuestionSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['questions.Question']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['providers']