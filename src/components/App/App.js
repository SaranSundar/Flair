import React from 'react';
import './App.css';
import {Route, Switch} from "react-router-dom";
import WebSocketExample from "../WebSocketExample/WebSocketExample";
import NoMatch from "../NoMatch/NoMatch";

function App() {
    return (
        <div className="App">
            {/*<NavBar/>*/}
            <Switch>
                <Route exact path="/" component={WebSocketExample}/>
                <Route component={NoMatch}/>
            </Switch>
        </div>
    );
}

export default App;
