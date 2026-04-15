console.log('detector started');

const checked = new WeakSet();

function getSite() {
  if (window.location.hostname.includes('claude.ai')) return 'claude';
  if (window.location.hostname.includes('chatgpt.com') || window.location.hostname.includes('chat.openai.com')) return 'chatgpt';
  return null;
}

function getLastResponse() {
  const site = getSite();
  if (site === 'chatgpt') {
    const responses = document.querySelectorAll('[data-message-author-role="assistant"]');
    return responses.length ? responses[responses.length - 1] : null;
  }
  if (site === 'claude') {
    const responses = document.querySelectorAll('.standard-markdown');
    return responses.length ? responses[responses.length - 1] : null;
  }
  return null;
}

function sendToAPI(text, element) {
  console.log('sending to api...');
  fetch('http://localhost:5001/detect', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ query: 'test query', response: text })
  })
  .then(r => r.json())
  .then(result => {
    console.log('got result:', result);
    const score = result.risk_score;
    let color = '#22c55e';
    if (score >= 30 && score < 60) color = '#f59e0b';
    if (score >= 60) color = '#ef4444';

    const badge = document.createElement('div');
    badge.className = 'hallucination-badge';
    badge.style = `background:${color};color:white;padding:10px;margin:10px 0;border-radius:5px;font-weight:bold;`;
    badge.textContent = `Risk: ${score}/100 - ${result.message}`;
    element.appendChild(badge);
    console.log('badge added!');
  })
  .catch(err => {
    console.error('error:', err);
    checked.delete(element);
  });
}

// per-element stability tracking
const elementSnapshots = new WeakMap();

function runCheck() {
  const last = getLastResponse();
  if (!last) return;
  if (checked.has(last)) return;
  if (last.querySelector('.hallucination-badge')) return;

  const text = last.textContent.trim();
  if (text.length < 50) return;

  const prev = elementSnapshots.get(last);

  if (prev === text) {
    // text is stable — send it
    checked.add(last);
    sendToAPI(text, last);
  } else {
    // store snapshot and wait for next check
    elementSnapshots.set(last, text);
  }
}

// poll every 2 seconds
setInterval(runCheck, 2000);

// also trigger on DOM changes
let debounceTimer;
const observer = new MutationObserver(() => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(runCheck, 1000);
});
observer.observe(document.body, { childList: true, subtree: true });