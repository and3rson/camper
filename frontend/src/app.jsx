import React from 'react';
import ReactDOM from 'react-dom';
import AppBar from 'material-ui/AppBar';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import { Card, CardHeader, CardTitle, CardText, CardMedia, CardActions } from 'material-ui/Card';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { Container, Row, Col } from 'react-grid-system';
import FlatButton from 'material-ui/FlatButton';
//import SvgIcon, WbSunny from 'material-ui/SvgIcon';
import ImageWbSunny from 'material-ui/svg-icons/image/wb-sunny.js';
import DashboardIcon from 'material-ui/svg-icons/action/dashboard.js';
import ChannelsIcon from 'material-ui/svg-icons/communication/call-split.js';
//import ChannelsIcon from 'material-ui/svg-icons/action/settings-input-component.js';
import ValuesIcon from 'material-ui/svg-icons/editor/insert-drive-file.js';
import ThingsIcon from 'material-ui/svg-icons/device/nfc.js';
import { yellow500 } from 'material-ui/styles/colors';
//import { Table, TableHeader, TableHeaderColumn, TableBody, TableRow, TableRowColumn } from 'material-ui/Table';
import { List, ListItem } from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import Divider from 'material-ui/Divider';

import { API } from './api';

const api = new API(window.location.protocol + '//' + window.location.hostname + ':9090');
window.api = api;

const getHash = () => window.location.hash.replace(/^#/, '');

class Header extends React.Component {
    render() {
        return <AppBar title="Camper" showMenuIconButton={false} />;
    }
}

class Sidebar extends React.Component {
    constructor () {
        super();

        window.addEventListener('hashchange', (e) => {
            this.onMenuItemChange(e, getHash());
        });
    }

    getStyle(value) {
        if (value == (getHash() || 'things')) {
            return {backgroundColor: '#E8E8E8'};
        }
        return {};
    }

    render() {
        // <MenuItem primaryText="Dashboard" value="dashboard" leftIcon={<DashboardIcon />} style={this.getStyle('dashboard')} />
        return (
            <Menu autoWidth={true} onChange={this.onMenuItemChange.bind(this)}>
                <MenuItem primaryText="Things" value="things" leftIcon={<ThingsIcon />} style={this.getStyle('things')} />
                <MenuItem primaryText="Values" value="values" leftIcon={<ValuesIcon />} style={this.getStyle('values')} />
                <MenuItem primaryText="Channels" value="channels" leftIcon={<ChannelsIcon />} style={this.getStyle('channels')} />
            </Menu>
        );
    }

    onMenuItemChange(e, value) {
        window.location.hash = value;
        this.props.onMenuItemChange(e, value);
    }
}

class DashboardPage extends React.Component {
    constructor() {
        super();

        this.state = {
            thingsCount: api.data.things.length,
            valuesCount: api.data.values.length,
            channelsCount: api.data.channels.length
        };
        this.updateThingsCount = this.updateThingsCount.bind(this);
        this.updateValuesCount = this.updateValuesCount.bind(this);
        this.updateChannelsCount = this.updateChannelsCount.bind(this);
    }

    componentDidMount() {
        api.on('things:change', this.updateThingsCount);
        api.on('values:change', this.updateValuesCount);
        api.on('channels:change', this.updateChannelsCount);
    }

    componentWillUnmount() {
        api.removeListener('things:change', this.updateThingsCount);
        api.removeListener('values:change', this.updateValuesCount);
        api.removeListener('channels:change', this.updateChannelsCount);
    }

    updateThingsCount(things) {
        this.setState({thingsCount: things.length});
    }

    updateValuesCount(values) {
        this.setState({valuesCount: values.length});
    }

    updateChannelsCount(channels) {
        this.setState({channelsCount: channels.length});
    }

    render() {
        return (
            <Row>
                <Col xs={12} md={4} style={{textAlign: 'center'}}>
                    <h1>{this.state.thingsCount}</h1>
                    <div>Things</div>
                </Col>
                <Col xs={12} md={4} style={{textAlign: 'center'}}>
                    <h1>{this.state.valuesCount}</h1>
                    <div>Values</div>
                </Col>
                <Col xs={12} md={4} style={{textAlign: 'center'}}>
                    <h1>{this.state.channelsCount}</h1>
                    <div>Channels</div>
                </Col>
            </Row>
        );
    }
}

class ChannelsPage extends React.Component {
    constructor() {
        super();

        this.state = {
            channels: api.data.channels
        };
        this.updateChannels = this.updateChannels.bind(this);
    }
    componentDidMount() {
        api.on('channels:change', this.updateChannels);
    }
    componentWillUnmount() {
        api.removeListener('channels:change', this.updateChannels);
    }
    updateChannels(channels) {
        this.setState({channels: channels});
    }
    render() {
        return (
            <List>
                <Subheader>Channels</Subheader>
                <ListItem disabled={true}>
                    <Row>
                        <Col xs={4} md={3}>ID</Col>
                        <Col xs={8} md={9}>URL</Col>
                    </Row>
                </ListItem>
                {this.state.channels.map((channel, i) => (
                    <ChannelView model={channel} key={i} />
                ))}
            </List>
        );
    }
}

class ChannelView extends React.Component {
    render() {
        return (
            <div>
                <Divider />
                <ListItem>
                    <Row>
                        <Col xs={4} md={3}>
                            {this.props.model.id}
                        </Col>
                        <Col xs={8} md={9}>
                            {this.props.model.url}
                        </Col>
                    </Row>
                </ListItem>
            </div>
        );
    }
}

class ValuesPage extends React.Component {
    constructor() {
        super();

        this.state = {
            values: api.data.values
        };
        this.updateValues = this.updateValues.bind(this);
    }
    componentDidMount() {
        api.on('values:change', this.updateValues);
    }
    componentWillUnmount() {
        api.removeListener('values:change', this.updateValues);
    }
    updateValues(values) {
        this.setState({values: values});
    }
    render() {
        return (
            <List>
                <Subheader>Values</Subheader>
                <ListItem disabled={true}>
                    <Row>
                        <Col xs={2} md={2}>ID</Col>
                        <Col xs={2} md={2}>Type</Col>
                        <Col xs={1} md={1}>State</Col>
                        <Col xs={2} md={2}>Description</Col>
                        <Col xs={2} md={2}>Channel</Col>
                        <Col xs={1} md={1}>JSON path</Col>
                        <Col xs={2} md={2}>data</Col>
                    </Row>
                </ListItem>
                {this.state.values.map((value, i) => (
                    <ValueView model={value} key={i} />
                ))}
            </List>
        );
    }
}

class ValueView extends React.Component {
    render() {
        return (
            <div>
                <Divider />
                <ListItem>
                    <Row>
                        <Col xs={2} md={2}>
                            {this.props.model.id}
                        </Col>
                        <Col xs={2} md={2}>
                            {this.props.model.value_type}
                        </Col>
                        <Col xs={1} md={1}>
                            {this.props.model.is_alive ? (<span style={{color: '#44AA00'}}>Alive</span>) : (<span style={{color: '#AA0000'}}>Dead</span>)}
                        </Col>
                        <Col xs={2} md={2}>
                            {this.props.model.description}
                        </Col>
                        <Col xs={2} md={2}>
                            {this.props.model.channel}
                        </Col>
                        <Col xs={1} md={1}>
                            {this.props.model.json_path}
                        </Col>
                        <Col xs={2} md={2}>
                            {this.props.model.data}
                        </Col>
                    </Row>
                </ListItem>
            </div>
        );
    }
}

class ThingsPage extends React.Component {
    constructor() {
        super();

        this.state = {
            things: api.data.things
        };
        this.updateThings = this.updateThings.bind(this);
    }
    componentDidMount() {
        api.on('things:change', this.updateThings);
    }
    componentWillUnmount() {
        api.removeListener('things:change', this.updateThings);
    }
    updateThings(things) {
        console.log('Things changed');
        this.setState({things: things});
    }
    render() {
        return (
            <div>
                <Subheader>Things</Subheader>
                <Row>
                    {this.state.things.map((thing, i) => (
                        <Col xs={12} md={6} lg={4} key={i}>
                            <ThingView model={thing} key={i} />
                        </Col>
                    ))}
                </Row>
            </div>
        );
    }
}

class ThingView extends React.Component {
    constructor() {
        super();
        this.types = {
            temperature: 'thermometer',
            humidity: 'swimming-pool',
            brightness: 'light-bulb'
        };
        this.units = {
            temperature: '\u2103',
            humidity: '%',
            brightness: '%'
        };
        this.state = {
            //lastUpdated: this.props.model.date_last_updated
            timePassed: 0
        };
    }

    componentDidMount() {
        this.interval = window.setInterval(function() {
            this.setState({timePassed: this.state.timePassed + 1});
        }.bind(this), 1000);
    }

    componentWillUnmount() {
        window.clearInterval(this.interval);
    }

    render() {
        //<CardActions>
        //    <FlatButton label="Reset" />
        //</CardActions>
        //avatar={
        //    this.props.model.is_alive
        //    ? 'https://www.colorcombos.com/images/colors/44AA00.png'
        //    : 'https://www.colorcombos.com/images/colors/AA0000.png'
        //}
        return (
            <Card style={{marginTop: '16px', marginBottom: '16px'}}>
                <CardHeader
                    title={this.props.model.name} subtitle={this.props.model.type} />
                {this.props.model.values.map((value, i) => (
                    <CardText key={i}>
                        <div style={{display: 'flex', flexDirection: 'columns', color: value.is_alive ? '#44AA00' : '#AA0000'}}>
                            <i className={ 'flaticon-' + this.types[value.value_type] } style={{width: '48px', textAlign: 'center'}}></i>
                            <div style={{ fontSize: '24px', flex: 1 }}>{value.data}{this.units[value.value_type]}</div>
                            <div style={{ fontSize: '14px', lineHeight: '24px', textAlign: 'right' }}>{this.formatDelta(this.getSecondsSinceLastUpdate(value))}</div>
                        </div>
                    </CardText>
                ))}
            </Card>
        );
    }

    getSecondsSinceLastUpdate(value) {
        return parseInt((new Date() - new Date(value.date_last_updated)) / 1000);
    }

    formatDelta(delta) {
        if (delta < 60) {
            return `${parseInt(delta)}s ago`;
        } else if (delta < 3600) {
            return `${parseInt(delta / 60)}m ${parseInt(delta % 60)}s ago`;
        } else {
            return `> ${parseInt(delta / 3600)}h ago`;
        }
    }
}

class App extends React.Component {
    constructor() {
        super();
        this.state = {
            page: getHash() || 'things'
        };
        this.pageMap = {
            'dashboard': <DashboardPage />,
            'channels': <ChannelsPage />,
            'values': <ValuesPage />,
            'things': <ThingsPage />
        };
    }

    render() {
        return (
            <MuiThemeProvider>
                <div>
                    <Header />
                    <Container fluid={true}>
                        <Row>
                            <Col xs={12} md={3}>
                                <Sidebar onMenuItemChange={this.loadPage.bind(this)} />
                            </Col>
                            <Col xs={12} md={9}>
                                {this.pageMap[this.state.page]}
                            </Col>
                        </Row>
                    </Container>
                </div>
            </MuiThemeProvider>
        );
    }

    loadPage(event, value) {
        this.setState({
            page: value
        });
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);

