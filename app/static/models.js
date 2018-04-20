function Feature(title, desc, client, priority, target_date, area, id) {
    var self = this;
    self.title = title;
    self.desc = desc;
    self.client = client;
    self.priority = priority;
    self.target_date = target_date;
    self.area = area;
    self.id = id;
}

function FeatureBoardViewModel() {
    self.features = ko.observableArray([]);

    $.getJSON("/requests", function(requests) {
        var mappedRequests = $.map(requests, function(r) {
            return new Feature(r.title, r.desc, r.client, r.priority, r.target_date, r.area, r.id);
        });
        self.features(mappedRequests);
    });
}

ko.applyBindings(new FeatureBoardViewModel(), document.getElementById('feature-board'));
