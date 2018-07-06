import React, { Component } from 'react';
import { getCookieValue } from '../Functions';
import { Link } from "react-router-dom";

export default class CollegesComponent extends Component {
    state = {
        colleges: null
    }

    token = getCookieValue("jwt");
    header = {
        "Authorization": `JWT ${this.token}`,
    }

    componentDidMount() {

        console.log(this.token);
        console.log("Header", this.header);
        
        fetch("http://localhost:8000/api/v1/colleges/",
            {
                headers:new Headers ({
                    Authorization: `JWT ${getCookieValue("jwt")}`,
                })
            }
        ).then(result => result.json())
            .then(data => { this.setState({ colleges: data }) })
            .catch(e => { console.log("Error "+e); });
    }
    render() {
        return (
            <div>
                <h2 align="center">Colleges List</h2>
                <table className="table table-bordered table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th >Name</th>
                            <th>Acronym</th>
                            <th>Location</th>
                            <th>Contact</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.state.colleges &&
                            this.state.colleges.map(college => {
                                return (
                                    <tr key={college.name}>
                                        <td>{college.id}</td>
                                        <td><Link to={`college/${college.id}/`}>{college.name}</Link></td>
                                        <td>{college.acronym}</td>
                                        <td>{college.location}</td>
                                        <td>{college.contact}</td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </table>
            </div>
        )
    }
}