/**
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons'),
    rtbs = require('react-bootstrap'),
    $ = require('jquery'),
    OverlayMixin = rtbs.OverlayMixin,
    Modal = rtbs.Modal,
    ProgressBar = rtbs.ProgressBar,
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


var InstallModalTrigger = React.createClass({
  getInitialState: function () {
    return {
      state: false,
      dc_url: '',
      dc_url_valid: false,
      api_key: '',
      api_key_valid: false,
    };
  },

  render: function(){
    if (this.state.state === "failed"){
      return (<Modal title="Setup failed" onRequestHide={false}>
                <div className="modal-body">
                  <p>There was an error creating your setup. If this keeps happening,
                    <a href="http://community.thegeoffrey.co/c/support">please let us know here</a>
                  </p>
                  <hr />
                  <p>{this.state.error}</p>
                </div>
              </Modal>);
    } else if (this.state.state === "done"){
      return (<Modal title="Setup successful" onRequestHide={false}>
                <div className="modal-body">
                  <ProgressBar bsStyle="success" now={100} />
                  <h2>Heureka</h2>
                  <p>your setup was successful.
                     Please not the following public- and api_key
                     and continue <a href='http://community.thegeoffrey.co/t/how-to-install-geoffrey/16/1'>your setup</a>:</p>
                  <Input readonly type="text" addonBefore="API Key" value={this.state.result.api_key} />
                  <Input readonly type="text" addonBefore="Public Key" value={this.state.result.public_key} />
                </div>
              </Modal>);
    } else if (this.state.state === "running") {
      return (<Modal title="Setting up" onRequestHide={false}>
                <div className="modal-body">
                  <ProgressBar bsStyle="success" active now={45} />
                </div>
              </Modal>);
    } else {
      var urlBsStyle = this.state.dc_url.length ? (
                        this.state.dc_url_valid ? 'success' : 'warning') : '',
          keyBsStyle = this.state.api_key.length ? (
                        this.state.api_key_valid ? 'success' : 'warning'): '',
          buttonState = !(this.state.dc_url_valid && this.state.api_key_valid);
      return (
            <Modal title="Beta Setup" onRequestHide={false}>
              <form onSubmit={this.onSubmit}>
                <div className="modal-body">
                  Please provide your information, so we can start setting you up
                  <Input
                    type="text"
                    value={this.state.dc_url}
                    hasFeedback
                    bsStyle={urlBsStyle}
                    onChange={this.onUrlChange}
                    placeholder="http://discourse.example.org"
                    help="Full URL including http:// or https://"
                    label="The Discourse URL"
                    ref="dc_url"/>
                  <Input
                    type="text"
                    placeholder="c62e1c8431ce3aea0eb848cf70da15f"
                    label="The Discourse API-KEY"
                    help="You find this under /admin/key in your discourse"
                    ref="api_key"
                    value={this.state.api_key}
                    hasFeedback
                    bsStyle={keyBsStyle}
                    onChange={this.onKeyChange}/>
                </div>
                <div className="modal-footer">
                  <Button disabled={buttonState} bsStyle="primary" type="submit">Start Setup</Button>
                </div>
              </form>
            </Modal>
          );
    }
  },
  onUrlChange: function(){
    var value = this.refs.dc_url.getValue().trim();
    this.setState({dc_url: value, dc_url_valid: /^https?:\/\/.*$/.test(value)});
  },
  onKeyChange: function(){
    var value = this.refs.api_key.getValue().trim();
    this.setState({api_key: value, api_key_valid: value.length == 64});
  },
  onSubmit: function(evt){
    evt.preventDefault();
    if (!this.state.dc_url_valid || !this.state.api_key_valid) return;

    this.setState({"state": "running"});
    var api_key = this.state.dc_url
        dc_url = this.state.api_key;
    $.getJSON("/api/create_new_instance?api_key=" + api_key + "&dc_url=" + dc_url,
        function(res){
          this.setState({"state": "done", "result": res});
        }.bind(this)).fail(function(res){
          this.setState({"state": "failed", "error": res});
        }.bind(this));
    }
});


if (document.location.hash === "#install"){
  React.render(<InstallModalTrigger />,
      document.getElementById('modalWrap'))
}


