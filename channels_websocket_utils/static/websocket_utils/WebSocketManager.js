class WebSocketManager {
    /*
    To use the WebSocket Manager:
    1) instanciate this object with path and (optional: token_str)
    for logged in user only connections (optional):
        a) call utils.get_websocket_token in views to obtain token_str and pass it to html template
        b) pass token_str into the constructor if this object
        c) in consumer.connect method call utils.validate_websocket_token to validate and accept the connection


    2) call sendJSON(message, reply handler callback) to send message. if a reply handler is provided
     it will be called with the reply message when it is received from ws.

    3) To receive server side data, write a message handler function and pass it to addMessageListener(key,reply handler)
     */
    constructor(path,token = null) {
        this.routingTable  = {
            "messageKey": () => ("messageHandler")
        }
        this.sendJSON             = this.sendJSON.bind(this)
        this.messageSwitcher      = this.messageSwitcher.bind(this)
        this.addMessageListener   = this.addMessageListener.bind(this)

        let target_url            = "ws://" + window.location.hostname + ":" + window.location.port + path + token
        console.log(target_url)
        this.ws                   = new WebSocket(target_url)
        this.ws.addEventListener('message', this.messageSwitcher)
    }

    addMessageListener (key, method) {
        this.routingTable[key] = method
        console.log("ws message listener added wit key" + key)
        console.log(this.routingTable)
    }

    sendJSON (message,replyHandler) {
        /*
        New feature in type19:
        Now components can call sendJSON and give it an callback to handle returned data
         */
        if (replyHandler !== null) {
            let reply_key         = this.makeUUID4()
            message.reply_key     = reply_key
            // decorate reply handler and add it to routing table
            let replayHanderWrapped = function (event) {
                // remove message listener
                delete this.routingTable[reply_key]
                // pass event along to replyhandler
                replyHandler(event)
            }
            replayHanderWrapped = replyHandler.bind(this)
            this.addMessageListener(reply_key,replayHanderWrapped)
        }

        let data                  = JSON.stringify(message)
        this.ws.send(data)
    }

    makeUUID4 ( ) {
        return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
            (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16))
    }

    messageSwitcher (event) {
        let obj                   = JSON.parse(event.data)
        console.log(obj)
        this.routingTable[obj.key](obj)
    }

}