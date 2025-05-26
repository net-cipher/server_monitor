function updateStats() {
    fetch('/api/stats')
    .then(res => res.json())
    .then(data => {
        console.log("Received data:", data);  // Debug line

        //CPU Updation
        document.getElementById('cpu-value').innerText = `${data.cpu}%`;
        document.querySelector('.cpu-bar').style.width = `${data.cpu}%`;

        //Ram Updation
        document.getElementById('ram-value').innerText = `${data.ram}%`;
        document.querySelector('.ram-bar').style.width = `${data.ram}%`;

        //Network 
        document.getElementById('network-value').innerText = `${data.network} bytes`;

        //Disk
        document.getElementById('disk-value').innerText = `${data.disk}%`;
        document.querySelector('.disk-bar').style.width = `${data.disk}%`;

        //Fetching Apps
        const appsHTML = data.top_apps.map(app =>
            `<div class="process">
                <span class="process-name">${app.name || "Unknown"}</span>
                <span class="process-cpu">${app.cpu.toFixed(2)}%</span>
                <span class="process-ram">${app.memory.toFixed(2)}%</span>
            </div>`
        ).join('');

        document.querySelector('.processes').innerHTML = appsHTML;
    })
    .catch(err => {
        console.error("Error fetching stats:", err);
    });
}

setInterval(updateStats, 1000);
updateStats();
