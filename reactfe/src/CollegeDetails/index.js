import React, { Component } from 'react';
import { getCookieValue } from '../Functions';

export default class CollegeDetails extends Component {

    state = {
        college: null,
        students: null
    }
    componentDidMount() {
        fetch("http://localhost:8000/api/v1/colleges/" + this.props.match.params.id + "/", {
            headers: new Headers({

                Authorization: `JWT ${getCookieValue("jwt")}`,
            })
        }
        )
            .then(result => result.json())
            .then(data => {
                this.setState({ college: data })
            })
            .catch(e => { console.log("Error") })

        fetch("http://localhost:8000/api/v1/colleges/" + this.props.match.params.id + "/students/", {
            headers: new Headers({
                Authorization: `JWT ${getCookieValue("jwt")}`,
            })
        })
            .then(result => result.json())
            .then(data => {
                this.setState({ students: data })
            })
            .catch(e => { console.log("Error") })
    }
    render() {
        return (
            <div>
                <h3 className="collegeName" align="center">{this.state.college && this.state.college.name} Students</h3>
                <table className="table table-bordered table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Db Folder</th>
                            <th>Dob</th>
                            <th>Dropped Out</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.state.students &&
                            this.state.students.map(student => {
                                return (
                                    <tr key={student.id}>
                                        <td>{student.id}</td>
                                        <td>{student.name}</td>
                                        <td>{student.email}</td>
                                        <td>{student.db_folder}</td>
                                        <td align="center">{student.dob ? String(student.dob) : "-"}</td>
                                        <td>{student.dropped_out ? "True" : "False"}</td>
                                    </tr>
                                )
                            })
                        }</tbody>
                </table>
            </div>
        )
    }
}