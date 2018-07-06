import React, { Component } from 'react';
import './App.css';

import AppHeader from './HeaderComponent';
import CollegeList from './CollegesComponent'
import CollegeDetails from './CollegeDetails'
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Login from './Login';

class App extends Component {

  state = {
    token:null
  }

  componentDidMount() {

    fetch("http://localhost:8000/api-token-auth/", {
      method: "post",
      body: JSON.stringify({ "username": "SomeshThakur", "password": "iamsomesh@33" }),
      headers: {
        "Content-Type": "application/json",
      }
    }
    ).then(result => result.json())
      .then(data => {
      console.log(data.token )
      })
  }


  render() {
    return (
      <div className="App">
        <AppHeader />
        <Router>
          <Switch>
            <Route exact path="/app/"  component={CollegeList} />
            <Route exact path="/app/college/:id/" component={CollegeDetails} />
            <Route exact path="/app/login/" component={(props)=><Login toggleLogin={AppHeader.toggleLogin} /> }/>
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
