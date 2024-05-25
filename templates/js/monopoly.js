let ws;

function connectWebSocket(session_id) {
    ws = new WebSocket(`ws://localhost:8000/ws/${session_id}`);

    ws.onopen = function() {
        console.log("WebSocket connection opened");
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'update') {
            updatePlayers(data.players);
        } else if (data.type === 'message') {
            console.log(data.message);
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
    const playerId = document.getElementById("playerId").value;
    if (playerId && ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'roll', id:playerId  }));
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