// State
let isAttacking = false;
let defencesEnabled = false;

let rpsHistory = [];
let timeLabels = [];

// Chart setup
const canvas = document.getElementById("trafficChart");
let trafficChart = null;

if (canvas) {
  const ctx = canvas.getContext("2d");

  trafficChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: timeLabels,
      datasets: [{
        label: "Requests / Second",
        data: rpsHistory,
        borderWidth: 2,
        tension: 0.4,
        borderColor: "#60a5fa"
      }]
    },
    options: {
      responsive: true,
      animation: false,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

// Button handlers
async function toggleAttack() {
  const res = await fetch("/toggle-attack", { method: "POST" });
  const data = await res.json();

  isAttacking = data.attacking;

  document.getElementById("attackBtn").textContent =
    isAttacking ? "Stop Attack" : "Start Attack";
}

async function toggleDefences() {
  const res = await fetch("/toggle-defences", { method: "POST" });
  const data = await res.json();

  defencesEnabled = data.defences;

  document.getElementById("defenceBtn").textContent =
    defencesEnabled ? "Disable Defences" : "Enable Defences";
}

// Traffic polling
async function fetchTraffic() {
  try {
    const res = await fetch("/traffic");
    const data = await res.json();

    // Pretty print traffic
    document.getElementById("traffic").textContent =
      JSON.stringify(data.traffic, null, 2);

    // Status banner logic
    const status = document.getElementById("status");

    if (data.alert && !data.defences) {
      status.textContent = "🚨 UNDER ATTACK";
      status.className = "status alert";
    } else if (data.alert && data.defences) {
      status.textContent = "🛡️ ATTACK MITIGATED";
      status.className = "status normal";
    } else {
      status.textContent = "Status: Stable";
      status.className = "status normal";
    }

    // Sync button text (important on refresh)
    document.getElementById("attackBtn").textContent =
      data.attacking ? "Stop Attack" : "Start Attack";

    document.getElementById("defenceBtn").textContent =
      data.defences ? "Disable Defences" : "Enable Defences";

    // Graph update
    if (trafficChart) {
      const now = new Date().toLocaleTimeString();
      timeLabels.push(now);
      rpsHistory.push(data.traffic.requests_per_second);

      if (rpsHistory.length > 25) {
        rpsHistory.shift();
        timeLabels.shift();
      }

      trafficChart.update();
    }

  } catch (err) {
    console.error("Traffic fetch failed:", err);
  }
}

// Polling loop
setInterval(fetchTraffic, 2000);
fetchTraffic(); // initial call