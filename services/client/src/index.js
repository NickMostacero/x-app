import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
 
class App extends Component {
  //nuevo
  constructor() {
    super();
    //nuevo
    this.state = {
      users: []
    };
  };
  //nuevo
  componentDidMount(){
    this.getUsers();
  };
  // nuevo
  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
    .then((res) => { this.setState({users: res.data.data.users});})
    .catch((err) => { console.log(err); });
  }
  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br/>
              <h1 className="title is-1">Todos los usuarios</h1>
              <hr/><br/>
              {/* new */}
              {
                this.state.users.map((user) => {
                  return (
                    <h4
                      key={user.id}
                      className="box title is-4"
                    >{ user.username }
                    </h4>
                  )
                })
              }
            </div>
          </div>
        </div>
      </section>
    )
  }
};
 
ReactDOM.render( <App />, document.getElementById('root'));