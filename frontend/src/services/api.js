let activeBase = "http://localhost:8001/api";

const CANDIDATE_HOSTS = [
  "http://localhost:8001/api",
  "http://localhost:8000/api"
];

export async function checkHealth() {
  for (const host of CANDIDATE_HOSTS) {
    try {
      const res = await fetch(`${host}/health`, { cache: 'no-store' });
      if (res.ok) {
        const data = await res.json();
        if (data.agent && data.agent.includes("RAKSHAK")) {
          activeBase = host;
          return data;
        }
      }
    } catch {
      // Continue to next host
    }
  }
  return { status: "offline", error: "Backend not reachable on port 8001 or 8000." };
}

export async function sendChatMessage(message) {
  try {
    const res = await fetch(`${activeBase}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server error: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    throw err;
  }
}

export async function fetchDemoEvents() {
  try {
    const res = await fetch(`${activeBase}/demo-events`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Failed to fetch demo events:", err);
    return { demo_events: [] };
  }
}

export async function testNotificationDispatch(data) {
  try {
    const res = await fetch(`${activeBase}/notifications/test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    throw err;
  }
}
