const url = `ws://${window.location.host}/ws/${sessionId}`;
const ws = new WebSocket(url);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    updatePlayersTable(data.players);
    updatePropertiesTable(data.properties);
};

function updatePlayersTable(players) {
    const playersTableBody = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
    playersTableBody.innerHTML = '';
    players.forEach(player => {
        const row = playersTableBody.insertRow();
        row.insertCell(0).textContent = player.id;
        row.insertCell(1).textContent = player.name;
        row.insertCell(2).textContent = player.balance;
        row.insertCell(3).textContent = player.position;
    });
}

function updatePropertiesTable(properties) {
    const propertiesTableBody = document.getElementById('propertiesTable').getElementsByTagName('tbody')[0];
    propertiesTableBody.innerHTML = '';
    properties.forEach(property => {
        const row = propertiesTableBody.insertRow();
        row.insertCell(0).textContent = property.number;
        row.insertCell(1).textContent = property.name;
        row.insertCell(2).textContent = property.type;
        row.insertCell(3).textContent = property.price;
        row.insertCell(4).textContent = property.owner_id;
        row.insertCell(5).textContent = property.street_color;
        row.insertCell(6).textContent = property.hotel_level;
        row.insertCell(7).textContent = property.mortgage;
    });
}

function rollDice() {
        const result = Math.floor(Math.random() * 6) + 1;
        document.getElementById('diceResult').textContent = result;
    }