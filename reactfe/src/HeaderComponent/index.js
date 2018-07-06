import React, { Component } from "react";

export default class AppHeader extends Component {

    state = {
        login: this.props.login
    }

    toggleLogin = (token) => {
        this.setState(prev => ({ login: !prev.login }))
    }
    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-dark bg-primary ">
                <a className="navbar-brand" href="/app/">Online College App</a>
                <ul>
                    <button className="btn btn-danger" id="logout_btn" onClick={this.toggleLogin} type="button">{this.state.login ? "Login" : "Logout"}</button>
                </ul>
            </nav>
        );
    }
}