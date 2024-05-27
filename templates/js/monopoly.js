let ws;

function connectWebSocket(session_id) {
    ws = new WebSocket(`ws://localhost:8080/ws/${session_id}`);

    ws.onopen = function() {
        console.log("WebSocket connection opened");
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'update') {
            updatePlayers(data.players);
        } else if (data.type === 'message') {
            console.log(data.message);
        } else if (data.type === 'error') {
            console.log(data.error);
        } else if (data.type === 'roll') {
            rollDice();
        } else {
            console.log("Unknown message type", data);
        }
    };

    ws.onclose = function(event) {
        console.log("WebSocket connection closed", event);
    };

    ws.onerror = function(error) {
        console.log("WebSocket error", error);
    };
}

function joinGame(event) {
    event.preventDefault();
    const playerName = document.getElementById("playerName").value;
    const session_id = document.getElementById("sessionNum").value;

    if (session_id && playerName) {
        connectWebSocket(session_id);
        ws.onopen = function() {
            console.log("WebSocket connection opened");
            ws.send(JSON.stringify({ action: 'join', name: playerName }));
        };
    } else {
        console.log("Invalid session id or player name");
    }
}

function rollDice() {
    console.log("Rolling dice");
    const playerId = document.getElementById("playerId").value;
    const sessionId = 1;
    console.log("Rolling dice", playerId, sessionId);
    if (sessionId && playerId) {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            connectWebSocket(sessionId);
            ws.onopen = function() {
                console.log("WebSocket connection opened");
                ws.send(JSON.stringify({ action: 'roll', id: playerId }));
            };
        } else {
            ws.send(JSON.stringify({ action: 'roll', id: playerId }));
        }
    } else {
        console.log("Invalid session id or player name");
    }
}

function updatePlayers(players) {
    const playersTable = document.getElementById("players");
    playersTable.innerHTML = "";
    players.forEach(player => {
        const row = playersTable.insertRow();
        row.insertCell(0).innerText = player.id;
        row.insertCell(1).innerText = player.name;
        row.insertCell(2).innerText = player.money;
        row.insertCell(3).innerText = player.queue;
        row.insertCell(4).innerText = player.position;
    });
}

window.addEventListener("beforeunload", () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
    }
});