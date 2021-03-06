const EventEmitter = require('events').EventEmitter;

export class API extends EventEmitter {
    constructor(apiRoot) {
        super();
        this.apiRoot = apiRoot.replace(/\/$/, '');
        this.data = {
            channels: [],
            values: [],
            devices: [],
            lastEvent: null,
            isEventsInitialized: false
            //events: []
        };

        this.updateChannels();
        this.updateValues();
        this.updateDevices();
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
        if (localStorage.camperUsername && localStorage.camperPassword) {
            opts.headers['Authorization'] = `Plain ${localStorage.camperUsername}:${localStorage.camperPassword}`;
        }
        return fetch(this.apiRoot + '/' + url.replace(/^\//, ''), opts).then(response => {
            if (response.status < 200 || response.status > 299) {
                throw new Error(`API error ${response.status}`);
            }
            return response.json();
        });
        //.catch(e => {
        //    console.error('API error:', e);
        //});
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

    updateDevices() {
        return this.request({url: '/api/devices/'}).then(devices => {
            this.data.devices = devices;
            this.emit('devices:change', devices);
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
                //let changedDevices = [];
                //events.forEach(event => {
                //    if (event.type == 'thing-value-changed') {
                //        this.data.values.filter(value => value.id == event.object_id).forEach(value => {
                //            value.date_last_updated = event.date_created;
                //            value.data = event.data;
                //            changedValues.push(value);
                //            this.data.devices.forEach(thing => {
                //                thing.values.forEach(thingValue => {
                //                    if (thingValue.id == value.id) {
                //                        thingValue.date_last_updated = event.date_created;
                //                        thingValue.data = event.data;
                //                        changedDevices.push(thing);
                //                    }
                //                });
                //            });
                //        });
                //    } else if (event.type == 'thing-alive-state-changed') {
                //        this.data.devices.filter(thing => thing.id == event.object_id).forEach(thing => {
                //            thing.is_alive = event.data;
                //            changedDevices.push(thing);
                //        });
                //    } else {
                //        console.error('Received unknown event from server:', event);
                //    }
                //});
                //if (changedValues.length) {
                //    console.log('changedValues:', changedValues);
                //    this.emit('values:change', this.data.values);
                //}
                //if (changedDevices.length) {
                //    console.log('changedDevices:', changedDevices);
                //    this.emit('devices:change', this.data.devices);
                //}
                if (events.length) {
                    this.updateDevices();
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

