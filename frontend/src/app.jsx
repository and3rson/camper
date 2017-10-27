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
import { yellow500 } from 'material-ui/styles/colors';
//import { Table, TableHeader, TableHeaderColumn, TableBody, TableRow, TableRowColumn } from 'material-ui/Table';
import { List, ListItem } from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import Divider from 'material-ui/Divider';

import { API } from './api';

const api = new API('http://127.0.0.1:9090');
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

    render() {
        return (
            <Menu autoWidth={true} onChange={this.onMenuItemChange.bind(this)}>
                <MenuItem primaryText="Dashboard" value="dashboard" />
                <MenuItem primaryText="Channels" value="channels" />
                <MenuItem primaryText="Values" value="values" />
                <MenuItem primaryText="Things" value="things" />
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

        this.state = {};
    }

    render() {
        return <h1>Dashboard</h1>;
    }
}

class ChannelsPage extends React.Component {
    constructor() {
        super();

        this.state = {
            channels: api.data.channels
        };
        api.on('channels:change', channels => this.setState({channels: channels}));
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
        api.on('values:change', values => this.setState({values: values}));
    }
    render() {
        return (
            <List>
                <Subheader>Values</Subheader>
                <ListItem disabled={true}>
                    <Row>
                        <Col xs={1} md={1}>ID</Col>
                        <Col xs={1} md={1}>Type</Col>
                        <Col xs={3} md={3}>Description</Col>
                        <Col xs={2} md={2}>Channel</Col>
                        <Col xs={3} md={3}>JSON path</Col>
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
                        <Col xs={1} md={1}>
                            {this.props.model.id}
                        </Col>
                        <Col xs={1} md={1}>
                            {this.props.model.value_type}
                        </Col>
                        <Col xs={3} md={3}>
                            {this.props.model.description}
                        </Col>
                        <Col xs={2} md={2}>
                            {this.props.model.channel}
                        </Col>
                        <Col xs={3} md={3}>
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
        api.on('things:change', things => this.setState({things: things}));
    }

    render() {
        return (
            <Row>
                {this.state.things.map((thing, i) => (
                    <Col xs={12} md={6} lg={4} key={i}>
                        <ThingView model={thing} key={i} />
                    </Col>
                ))}
            </Row>
        );
    }
}

class ThingView extends React.Component {
    constructor() {
        super();
        this.types = {
            temperature: 'thermometer',
            humidity: 'swimming-pool'
        };
    }
    render() {
        return (
            <Card style={{marginTop: '16px', marginBottom: '16px'}}>
                <CardHeader avatar={'http://via.placeholder.com/40x40'} title={this.props.model.name} subtitle={this.props.model.type} />
                {this.props.model.values.map((value, i) => (
                    <CardText key={i}>
                        <Row>
                            <Col xs={2}>
                                <i className={ 'flaticon-' + this.types[value.value_type] }></i>
                            </Col>
                            <Col xs={10}>
                                <div style={{ fontSize: '32px' }}>{value.data}</div>
                            </Col>
                        </Row>
                    </CardText>
                ))}
                <CardActions>
                    <FlatButton label="Reset" />
                </CardActions>
            </Card>
        );
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
                            <Col xs={3}>
                                <Sidebar onMenuItemChange={this.loadPage.bind(this)} />
                            </Col>
                            <Col xs={9}>
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

