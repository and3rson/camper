var EventEmitter = require('events').EventEmitter;

export class API extends EventEmitter {
    constructor(apiRoot) {
        super();
        this.apiRoot = apiRoot.replace(/\/$/, '');
        this.data = {
            channels: [],
            values: [],
            things: [],
            lastEvent: null,
            isEventsInitialized: false
            //events: []
        };

        this.updateChannels();
        this.updateValues();
        this.updateThings();
        this.startEventPolling();
    }

    request(args) {
        const method = args.method || 'GET';
        const url = args.url;
        const data = args.data;

        const opts = {
            method: method,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        };
        if (data) {
            opts.data = JSON.stringify(data);
        }
        return fetch(this.apiRoot + '/' + url.replace(/^\//, ''), opts).then(response => response.json());
    }

    updateChannels() {
        return this.request({url: '/api/channels/'}).then(channels => {
            this.data.channels = channels;
            this.emit('channels:change', channels);
        });
    }

    updateValues() {
        return this.request({url: '/api/values/'}).then(values => {
            this.data.values = values;
            this.emit('values:change', values);
        });
    }

    updateThings() {
        return this.request({url: '/api/things/'}).then(things => {
            this.data.things = things;
            this.emit('things:change', things);
        });
    }

    startEventPolling() {
        this.pollEvents().then(() => {
            window.setTimeout(this.startEventPolling.bind(this), 5000);
        });
    }

    pollEvents() {
        return this.request({
            url: '/api/events/?since=' + encodeURIComponent(this.data.lastEvent ? this.data.lastEvent.date_created : '')
        }).then(events => {
            if (this.data.isEventsInitialized) {
                //let changedValues = [];
                //let changedThings = [];
                //events.forEach(event => {
                //    if (event.type == 'thing-value-changed') {
                //        this.data.values.filter(value => value.id == event.object_id).forEach(value => {
                //            value.date_last_updated = event.date_created;
                //            value.data = event.data;
                //            changedValues.push(value);
                //            this.data.things.forEach(thing => {
                //                thing.values.forEach(thingValue => {
                //                    if (thingValue.id == value.id) {
                //                        thingValue.date_last_updated = event.date_created;
                //                        thingValue.data = event.data;
                //                        changedThings.push(thing);
                //                    }
                //                });
                //            });
                //        });
                //    } else if (event.type == 'thing-alive-state-changed') {
                //        this.data.things.filter(thing => thing.id == event.object_id).forEach(thing => {
                //            thing.is_alive = event.data;
                //            changedThings.push(thing);
                //        });
                //    } else {
                //        console.error('Received unknown event from server:', event);
                //    }
                //});
                //if (changedValues.length) {
                //    console.log('changedValues:', changedValues);
                //    this.emit('values:change', this.data.values);
                //}
                //if (changedThings.length) {
                //    console.log('changedThings:', changedThings);
                //    this.emit('things:change', this.data.things);
                //}
                if (events.length) {
                    this.updateThings();
                    this.updateValues();
                }
            }
            if (events.length) {
                this.data.lastEvent = events[0];
                console.log('Set last event to', this.data.lastEvent);
            }
            this.data.isEventsInitialized = true;
        });
    }
}

