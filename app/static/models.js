clients = [
    'Client A',
    'Client B',
    'Client C'
];

areas = [
    'Policies',
    'Billing',
    'Claims',
    'Reports'
];

function get_current_date() {
    var d = new Date();
    return (new Date(d.getTime() + (d.getTimezoneOffset()*60*1000*-1))).toISOString().split('T')[0];
}

ko.validation.rules.mustBeIn = {
    validator: function (val, arr) {
        return arr.indexOf(val) > -1;
    },
    message: 'A valid selection is required'
};
ko.validation.registerExtenders();

function Feature(data) {
    var self = this;

    if (data === undefined) { // defaults
        self.done = ko.observable(false);
        self.counts = ko.observableArray([]);
        self.title = ko.observable('').extend({ required: true, maxLength: 200 });
        self.desc = ko.observable('');
        self.client = ko.observable('').extend({ required: true, mustBeIn: clients });
        self.priority = ko.observable('').extend({ required: true });
        self.disablePriority = ko.computed(function() {
            disable = clients.indexOf(self.client()) === -1;
            if (disable) self.priority('');
            return disable;
        }, self);
        self.priorityOptions = ko.computed(function() {
            count = self.counts().find(function(client_count) {
                return client_count.client == self.client();
            });
            if (typeof count === 'undefined') {
                return [1];
            } else {
                var possible = [];
                for (var i = 1; i <= count.count+1; i++) {
                    possible.push(i);
                }

                return possible;
            }
        }, self);
        self.target_date = ko.observable(get_current_date()).extend({ required: true, date: true});
        self.area = ko.observable('').extend({ required: true, mustBeIn: areas });
        $.getJSON('/request-counts', function(counts) {
            var mappedCounts = $.map(counts, function(count, client) {
                return { client: client, count: count };
            });
            self.counts(mappedCounts);
            self.done(true);
        });

        self.checkValidity = function() {
            var valid = self.title.isValid() &&
                self.client.isValid() &&
                self.priority.isValid() &&
                self.target_date.isValid() &&
                self.area.isValid();
            if (!valid) {
                ko.validation.group(self).showAllMessages(true);
                return false;
            } else {
                return true;
            }
        };
    } else { // passed values
        self.title = data.title;
        self.desc = data.desc;
        self.client = data.client;
        self.priority = data.priority;
        self.target_date = data.target_date;
        self.area = data.area;
        self.id = data.id;
    }
}

function FeatureBoardViewModel() {
    self.features = ko.observableArray([]);
    self.done = ko.observable(false);

    $.getJSON('/requests', function(requests) {
        var mappedRequests = $.map(requests, function(r) {
            return new Feature(r);
        });
        self.features(mappedRequests);
        self.done(true);
    });
}

element = document.getElementById('feature-board');
if (element === null) {
    ko.applyBindings(new Feature(), document.getElementById('feature-form'));
} else {
    ko.applyBindings(new FeatureBoardViewModel(), element);
}
