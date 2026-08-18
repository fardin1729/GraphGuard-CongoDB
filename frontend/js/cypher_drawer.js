const CypherDrawer = {
  isOpen: false,
  traceCount: 0,
  currentQuery: '',

  init() {
    const drawer = document.getElementById('cypherInspectorDrawer');
    const btnToggle = document.getElementById('btnToggleCypherDrawer');
    const btnClose = document.getElementById('btnCloseCypherDrawer');
    const btnCopy = document.getElementById('btnCopyCypher');

    if (btnToggle) {
      btnToggle.addEventListener('click', () => this.toggle());
    }

    if (btnClose) {
      btnClose.addEventListener('click', () => this.close());
    }

    if (btnCopy) {
      btnCopy.addEventListener('click', () => this.copyQueryToClipboard());
    }
  },

  toggle() {
    this.isOpen ? this.close() : this.open();
  },

  open() {
    const drawer = document.getElementById('cypherInspectorDrawer');
    if (drawer) {
      drawer.classList.add('open');
      this.isOpen = true;
    }
  },

  close() {
    const drawer = document.getElementById('cypherInspectorDrawer');
    if (drawer) {
      drawer.classList.remove('open');
      this.isOpen = false;
    }
  },

  updateTrace(trace) {
    if (!trace) return;

    this.traceCount++;
    this.currentQuery = trace.query;

    const badge = document.getElementById('cypherBadgeCount');
    if (badge) badge.innerText = this.traceCount;

    const executedOn = document.getElementById('cypherExecutedOn');
    if (executedOn) executedOn.innerText = `Target: ${trace.executed_on || 'CognoDB'}`;

    const latencyBadge = document.getElementById('cypherLatencyBadge');
    if (latencyBadge) latencyBadge.innerText = `Latency: ${trace.execution_time_ms} ms`;

    const recordCount = document.getElementById('cypherRecordCount');
    if (recordCount) recordCount.innerText = `Records: ${trace.record_count}`;

    const queryCode = document.getElementById('cypherQueryCode');
    if (queryCode) queryCode.innerText = trace.query;

    const paramsCode = document.getElementById('cypherParamsCode');
    if (paramsCode) {
      paramsCode.innerText = JSON.stringify(trace.parameters || {}, null, 2);
    }
  },

  async copyQueryToClipboard() {
    if (!this.currentQuery) {
      showToast('No Cypher query available to copy', 'error');
      return;
    }

    try {
      await navigator.clipboard.writeText(this.currentQuery);
      showToast('Parameterized openCypher query copied to clipboard!', 'success');
    } catch (err) {
      showToast('Failed to copy to clipboard', 'error');
    }
  }
};
