import React from 'react';
import './WebSocketExample.css';
import WebSocketWrapper from "../WebSocketWrapper/WebSocketWrapper";


class WebSocketExample extends React.Component {
    constructor(props) {
        super(props);
        this.SERVER_URL = "ws://localhost:43968/example_ws/echo-example";
    }

    handleData = (data) => {
        console.log("Data received");
        console.log(data);
    };

    handleOpen = () => {
        console.log("Connected to Server");
    };

    handleClose = () => {
        console.log("Disconnected from Server");
    };

    sendMessage = (message) => {
        this.refWebSocket.sendMessage(message);
    };

    render() {
        return (
            <div className="WebSocketExample">
                <button onClick={() => this.sendMessage("Hello World!")}>Send Message</button>
                <WebSocketWrapper
                    url={this.SERVER_URL} onMessage={this.handleData}
                    onOpen={this.handleOpen} onClose={this.handleClose}
                    reconnect={true} debug={true}
                    ref={Websocket => {
                        this.refWebSocket = Websocket;
                    }}/>
            </div>
        );
    }
}

export default WebSocketExample;