document.addEventListener('DOMContentLoaded', async () => {
  CypherDrawer.init();
  GraphViz.init('visGraphNetwork');
  Simulation.init();
  SPOF.init();
  Vendors.init();

  setupTabNavigation();
  setupHeaderActions();
  setupFilters();

  await checkDatabaseHealth();
  await loadEntities();
  await loadMainGraph();
});

function setupTabNavigation() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTabId = btn.getAttribute('data-tab');

      tabButtons.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      document.getElementById(targetTabId)?.classList.add('active');

      if (targetTabId === 'tab-spof' && !SPOF.data) {
        SPOF.load();
      }
    });
  });
}

async function checkDatabaseHealth() {
  const badge = document.getElementById('dbStatusBadge');
  const statusText = document.getElementById('dbStatusText');
  const latencyText = document.getElementById('dbLatencyText');

  try {
    const health = await API.getHealth();
    
    badge.className = `status-badge status-${health.status}`;
    if (health.status === 'healthy') {
      statusText.innerText = 'CognoDB Cloud Connected';
      latencyText.innerText = `(${health.latency_ms} ms)`;
    } else if (health.status === 'mock_mode') {
      statusText.innerText = 'In-Memory Simulation Mode';
      latencyText.innerText = `(${health.latency_ms} ms)`;
    } else {
      statusText.innerText = 'DB Disconnected';
      latencyText.innerText = '';
    }
  } catch (err) {
    if (badge) {
      badge.className = 'status-badge status-connecting';
      statusText.innerText = 'DB Unreachable';
    }
  }
}

async function loadEntities() {
  try {
    const data = await API.getEntities();

    const supplierSelect = document.getElementById('supplierSelect');
    if (supplierSelect) {
      supplierSelect.innerHTML = '<option value="">-- Choose a Supplier to Disrupt --</option>' +
        data.suppliers.map(s => `<option value="${s.id}">${s.name} (${s.country}, Risk: ${s.risk_score})</option>`).join('');
    }

    const regionSelect = document.getElementById('regionSelect');
    if (regionSelect) {
      regionSelect.innerHTML = '<option value="">-- Choose a Region to Disrupt --</option>' +
        data.regions.map(r => `<option value="${r.id}">${r.name} (Risk Index: ${r.risk_index})</option>`).join('');
    }

    const vendorCmpSelect = document.getElementById('vendorComponentSelect');
    if (vendorCmpSelect) {
      vendorCmpSelect.innerHTML = '<option value="">-- Select Component --</option>' +
        data.components.map(c => `<option value="${c.id}">${c.name} [${c.criticality}]</option>`).join('');
    }
  } catch (err) {
    console.error('Failed to load dropdown entities:', err);
  }
}

async function loadMainGraph(nodeType = null, search = null) {
  try {
    const res = await API.getGraph(nodeType, search);
    GraphViz.loadGraph(res.graph);
  } catch (err) {
    console.error('Failed to load main graph data:', err);
  }
}

function setupHeaderActions() {
  document.getElementById('dbStatusBadge')?.addEventListener('click', async () => {
    showToast('Reconnecting to CognoDB Cloud...', 'info');
    await API.reconnect();
    await checkDatabaseHealth();
  });

  document.getElementById('btnSeedData')?.addEventListener('click', async () => {
    const btn = document.getElementById('btnSeedData');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Seeding...';
    btn.disabled = true;

    try {
      const res = await API.seedDatabase();
      showToast(res.message, 'success');
      await loadEntities();
      await loadMainGraph();
      if (SPOF.data) await SPOF.load();
    } catch (err) {
      showToast('Seeding failed', 'error');
    } finally {
      btn.innerHTML = '<i class="fa-solid fa-database"></i> Seed Graph';
      btn.disabled = false;
    }
  });
}

function setupFilters() {
  document.getElementById('btnApplyFilter')?.addEventListener('click', () => {
    const nodeType = document.getElementById('filterNodeType')?.value || null;
    const search = document.getElementById('filterSearchInput')?.value.trim() || null;
    loadMainGraph(nodeType, search);
    showToast('Filters applied to graph canvas', 'info');
  });

  document.getElementById('btnResetFilter')?.addEventListener('click', () => {
    const typeSelect = document.getElementById('filterNodeType');
    const searchInput = document.getElementById('filterSearchInput');
    if (typeSelect) typeSelect.value = '';
    if (searchInput) searchInput.value = '';
    loadMainGraph();
    showToast('Filters reset', 'info');
  });
}
