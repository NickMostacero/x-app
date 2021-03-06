import React, { Component } from 'react';
import ReactDOM from 'react-dom';
//import axios from 'axios';
import * as axios from 'axios';
import UsersList from './components/UsersList';
import AddUser from './components/AddUser';

 
class App extends Component {
  //nuevo
  constructor() {
    super();
    //nuevo
    this.state = {
      users: [],
      username: 'justatest',
      email: '',
    };
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);  // nuevo
  };
  //nuevo
  componentDidMount(){
    this.getUsers();
  };
  // nuevo
  getUsers() {
    axios.get(`http://localhost/users`)
    .then((res) => { this.setState({users: res.data.data.users});})
    .catch((err) => { console.log(err); });
  }
  addUser(event) {
    event.preventDefault();
    // nuevo
    const data = {
      username: this.state.username,
      email: this.state.email
    };
    axios.post(`http://localhost/users`,data)
    .then((res)=>{
      this.getUsers();  // nuevo
      this.setState({username: '', email:'' })  //nuevo
    })
    .catch((err) => { console.log(err); });
  };  
  handleChange(event){
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };
  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-half">{/* nuevo */}
              <br/>
              <h1 className="title is-1">Todos los usuarios</h1>
              <hr/><br/>
              <AddUser 
                username={this.state.username}
                email={this.state.email}
                addUser={this.addUser}
                handleChange={this.handleChange}
              />
              <br></br>{/* nuevo */}
              {/* nuevo */}
              <UsersList users={this.state.users}/>
            </div>
          </div>
        </div>
      </section>
    )
  }
};
 
ReactDOM.render( <App />, document.getElementById('root'));