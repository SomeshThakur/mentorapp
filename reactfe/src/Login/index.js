import React, { Component } from 'react'
import { getCookieValue } from '../Functions';

export default class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        };
    }

    validateForm() {
        return this.state.username.length > 0 && this.state.password.length > 0;
    }
    handleChange = event => {
        this.setState({
            [event.target.id]: event.target.value
        });
    }

    submit = event => {
        fetch("http://localhost:8000/api-token-auth/", {
            method: "post",
            body: JSON.stringify({ "username": `${this.state.username}`, "password": `${this.props.password}` }),
            headers: {
                "Content-Type": "application/json",
            }
        }
        ).then(result => result.json())
            .then(data => {
                this.props.toggleLogin(data);
                this.props.history.push('/app/');
            }).catch(e => {
                console.log(e);
            })
        event.preventDefault();
    }

    render() {
        return (
            <div>
                <div id="content">
                    <div className="row">
                        <div className="col col-lg-3"></div>
                        <div className="col col-lg-6">
                            <form>
                                <label>Username</label>
                                <input className="form-control" id="username" autoFocus
                                    onChange={this.handleChange}
                                />
                                <br />
                                <label>Password</label>
                                <input className="form-control" id="password" value={this.state.password}
                                    onChange={this.handleChange}
                                    type="password" />
                                <br />
                                <center>
                                    <button
                                        onClick={this.submit}
                                        className="btn btn-primary"
                                        disabled={!this.validateForm()}
                                    >Login
                        </button>
                                </center>
                            </form></div>
                    </div>
                    <div className="col col-lg-3"></div>
                </div>
            </div>)
    }
}
