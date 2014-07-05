// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Backbone models
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

var ProviderResponse = Backbone.Model.extend({
    urlRoot: '/api/providerresponses/',

    url: function() {
        var base = _.result(this, 'urlRoot') || _.result(this.collection, 'url') || urlError();
        if (this.isNew()) return base;

        // add trailing slash to the URL, Django requirement
        return base.replace(/([^\/])$/, '$1/') + encodeURIComponent(this.id) + '/';
    }

});

var ProviderResponseCol = Backbone.Collection.extend({
    url: '/api/providerresponses/',

    model: ProviderResponse,

    initialize: function (models, options) {
        this.options = options;
    },

    comparator: function (model){
        if (this.options) {
            var status = model.get('status');
            var index = _.findWhere(this.options.status_map, {'status_id': status})
            if (index.index > -1) {
                return index.index;
            } else {
                console.error('WTF index:', model, index, this.options.status_map);
           }
        }
    }
});


var Status = Backbone.Model.extend({});
var Statuses = Backbone.Collection.extend({model: Status});
var Provider = Backbone.Model.extend({});
var Providers = Backbone.Collection.extend({model: Provider});


// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Marionette.js main application definition
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

// make MyApp a global variable (TODO: namespace it to the CIT namespace)
window.MyApp = new Backbone.Marionette.Application({

    // utlity function, useful only in the application context
    _add_empty_provider_responses: function (options) {
        // adds empty models to the collection, as we can only read data
        // which is 'checked' (stored in the database)

        var new_providerresponses = new ProviderResponseCol();

        // extract/flatten live model attributes
        var live_models = [];
        _.each(options.providerresponses.models, function (model) {
            live_models.push(model.attributes);
        });

        _.each(options.providers.models, function (provider) {
            _.each(options.statuses.models, function (status) {
                var _status_id = status.get('id');
                var _provider_id = provider.get('id');

                // check if the model is 'checked'
                var test = _.findWhere(live_models, {
                    'provider': _provider_id,
                    'status': _status_id,
                    'imagery_request': options.imagery_request_id
                });
                // prepare new provider response data
                var tmp_ProviderResponse = new ProviderResponse({
                    'provider': _provider_id,
                    'status': _status_id,
                    'imagery_request': options.imagery_request_id
                })

                if (test === undefined) {
                    // there is no model on the server, set id:undefined
                    tmp_ProviderResponse.set('id', undefined);
                } else {
                    // there is model on the server, reuse id
                    tmp_ProviderResponse.set('id', test['id']);
                }

                // add provider_response model to the new collection
                new_providerresponses.add(tmp_ProviderResponse, {silent:true});
            });
        });
        return new_providerresponses;
    }
});

// define a custom region
var ProviderResponseRegion = Backbone.Marionette.Region.extend({
    el: "#provider-response-list",

    // we are using a table to display data so for this case we actually
    // want to append 'view' children and not the 'view' element
    attachHtml: function(view){
        this.$el.empty().append(view.$el.children());
    }
});

// define regions of the application
MyApp.addRegions({
    statusList: "#status-list",
    providerResponseList: ProviderResponseRegion
});

// an application initializer, an application can have many initializers
MyApp.addInitializer(function(options){

    // instantiate ProviderStatusList view
    var providerStatusListView = new ProviderStatusListView({
        // pass statuses from options
        collection: options.statuses
    });
    // add view to the region and show it
    MyApp.statusList.show(providerStatusListView);


    // create status_map, it will be used to keep ProviderStatus collection
    // in sorted state
    var status_map = _.map(options.statuses.models,
        function (status,idx) {return {status_id: status.id, index: idx}}
    );

    // prepare data, add empty/missing ProviderResponses
    var tmp_providerresponses = this._add_empty_provider_responses(options);

    // for every provider add it's providerresponses as 'responses' attribute
    _.each(options.providers.models, function (provider) {
        var providerresponses_list = _.filter(tmp_providerresponses.models, function (providerresp) {
            return providerresp.get('provider') === provider.id
        });
        provider.set('responses', providerresponses_list, {'silent':true});
    });

    // instantiate ProviderList view
    var providerListView = new ProviderListView({
        collection: options.providers,
        status_map: status_map
    });
    // add view to the region and show it
    MyApp.providerResponseList.show(providerListView);
});


// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Marionette views - ProviderResponse, Provider and ProviderStatus
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

var ProviderItemView = Backbone.Marionette.ItemView.extend({
    // Providers are <tr> elements
    tagName: "tr",
    template: JST.provider_item,

    onRender: function(){
        // after rendering the initial item, prepare ProviderResponse 'row'
        // and append ProviderReponseListView children to the existing row
        var prorespCol = new ProviderResponseCol(
            this.model.get('responses'),
            {status_map: this.options.status_map}
        );

        var rspcolview = new ProviderResponseListView({
            collection: prorespCol
        });
        // append ProviderResponseListView children
        this.$el.append(rspcolview.render().$el.children())
    }
});

var ProviderListView = Backbone.Marionette.CollectionView.extend({
    // this view will be added to the providerResponseList region, using a
    // special a region handler, so we use non existent 'dummy-tag'
    tagName: "dummy-tag",
    childView: ProviderItemView,

    childViewOptions: function () {
        // pass on 'status_map' to every childView
        return {status_map: this.options.status_map}
    }
});

// simple view, render every ProviderStatus as a <th> element
var ProviderStatusItemView = Backbone.Marionette.ItemView.extend({
    template: JST.provider_status,
    tagName: 'th',
    className: 'provider-status',
});

var ProviderStatusListView = Backbone.Marionette.CollectionView.extend({
    tagName: "tr",
    childView: ProviderStatusItemView,

    onBeforeRender: function () {
        // before actually rendering the collection, append information
        this.$el.append('<th>Providers</th>');
    }
});

// every ProviderResponse is a <td> element
var ProviderResponseItemView = Backbone.Marionette.ItemView.extend({
    template: JST.provider_response_item,
    tagName: "td",
    className: 'provider-status',

    modelEvents: {
        // call render on backbone sync event
        'sync': 'render'
    },

    events: {
        'click': '_handleClick'
    },

    _handleClick : function (evt) {
        var self=this;
        if (this.model.get('id')){
            // if the model exists, remove the model and add an empty
            // provider response
            this.model.destroy({
                wait:true,
                success: function (model) {
                // collection 'add' will automatically trigger collection render
                    self.options.parentCollection.add({
                        'provider': self.model.get('provider'),
                        'status': self.model.get('status'),
                        'imagery_request': self.model.get('imagery_request'),
                        'id': undefined
                    });
                }
            });

        } else {
            // if the model does not exist, save the model to the server
            this.model.save({}, {'wait':true});
        }
    }
});

var ProviderResponseListView = Backbone.Marionette.CollectionView.extend({
    // this collection will be appended to already existing Provider <tr>
    // so we use an arbitrary <dummy-tag>
    tagName: "dummy-tag",
    childView: ProviderResponseItemView,

    childViewOptions: function () {
        // in order to handle click events on the model level we pass
        // collection object
        return {parentCollection: this.collection}
    }
});