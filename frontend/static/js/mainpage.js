const ws = new WebSocket(`ws://${location.host}/metrics/ws`);

ws.onopen = () => console.log("connected");

ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    document.getElementById("temperature").innerHTML = `${data.cpu_temperature}`;
    document.getElementById("battery").innerHTML = `${data.battery}`
    document.getElementById("memory-percentage").innerHTML = `${data.memory_percentage}`
    document.getElementById("disk_usage_percentage").innerHTML = `${data.disk_usage_percentage}`
    document.getElementById("total_disk_gigabyte").innerHTML = `${data.total_disk_gigabyte}`
    document.getElementById("disk_usage_gigabyte").innerHTML = `${data.disk_usage_gigabyte}`
    document.getElementById("uptime_system").innerHTML = `${data.uptime_system}`
    console.log(e)
};

ws.onerror = (e) => console.error("error", e);
ws.onclose = (e) => console.log("closed", e.code);

document.querySelectorAll('.metric-card').forEach(card => {
    const valueEl = card.querySelector('.gauge-readout span');
    const fill = card.querySelector('.gauge-fill');
    const max = parseFloat(card.dataset.max) || 100;
    const CIRC = 2 * Math.PI * 52;
    fill.style.strokeDasharray = CIRC;

    const render = () => {
        const raw = parseFloat(valueEl.textContent);
        const pct = isNaN(raw) ? 0 : Math.min(Math.max(raw / max, 0), 1);
        fill.style.strokeDashoffset = CIRC * (1 - pct);
    };

    render();
    new MutationObserver(render).observe(valueEl, { childList: true, characterData: true, subtree: true });
});


document.querySelectorAll('.metric-card--flip').forEach(card => {
    const toggle = () => {
        const flipped = card.classList.toggle('is-flipped');
        card.setAttribute('aria-pressed', flipped);
    };
 
    card.addEventListener('click', toggle);
});