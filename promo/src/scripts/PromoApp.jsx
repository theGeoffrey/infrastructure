/**
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons'),
    rtbs = require('react-bootstrap'),
    Button = rtbs.Button,
    Input = rtbs.Input;

// Export React so the devtools can find it
(window !== window.top ? window.top : window).React = React;

// CSS
require('../styles/promo.less');

// images
var LOGOS = [require('../img/EVE-3-icon.png'), require('../img/M-O-2-icon.png'),
         require('../img/Wall-E-2-icon.png'), require('../img/e-ric-icon.png'),
         require('../img/eve-icon.png'), require('../img/m-o-full-icon.png'),
         require('../img/m-o-icon.png'), require('../img/wall-e-icon.png')]



var RandomLogo = React.createClass({

  getInitialState: function(){

    var random_logo = LOGOS[Number((Math.random() * LOGOS.length).toFixed())];

    //FIXME: allow for date-based specials
    return {'logo': random_logo};
  },

  render: function() {
    return (<img src={this.state.logo} alt="How can I be of service today?" />);
  }
});

React.render(<RandomLogo />,
    document.getElementById('logo-wrap'));

