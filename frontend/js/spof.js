const SPOF = {
  data: null,

  init() {
    document.getElementById('btnRefreshSpof')?.addEventListener('click', () => this.load());
  },

  async load() {
    const tbody = document.getElementById('spofTableBody');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Scanning Graph for SPOFs...</td></tr>';
    }

    try {
      this.data = await API.getSPOFAnalysis();
      this.render();
    } catch (err) {
      console.error('SPOF analysis failed:', err);
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-crimson">Failed to load SPOF analysis.</td></tr>';
      }
    }
  },

  render() {
    if (!this.data) return;

    const totalEl = document.getElementById('spofTotalCount');
    const critEl = document.getElementById('spofCritCount');
    if (totalEl) totalEl.innerText = this.data.spof_count;
    if (critEl) critEl.innerText = this.data.high_criticality_spof_count;

    const tbody = document.getElementById('spofTableBody');
    if (!tbody) return;

    if (this.data.components.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No single-point-of-failure bottlenecks found.</td></tr>';
      return;
    }

    tbody.innerHTML = this.data.components.map(c => {
      const critBadge = c.criticality === 'Critical' ? 'badge-crimson' :
                        c.criticality === 'High' ? 'badge-amber' : 'badge-cyan';

      return `
        <tr>
          <td>
            <div style="font-weight: 600;">${c.component_name}</div>
            <span class="badge ${critBadge}" style="font-size: 9px;">${c.criticality}</span>
          </td>
          <td>
            <span class="text-emerald" style="font-weight: 600;">${c.suppliers.join(', ')}</span>
          </td>
          <td>
            <span class="text-crimson" style="font-family: var(--font-mono); font-weight: 700;">
              $${c.revenue_at_risk_millions}M
            </span>
          </td>
          <td>
            <div style="display: flex; gap: 4px;">
              <button class="btn btn-secondary btn-sm" onclick="GraphViz.focusNode('${c.component_id}')" title="Locate in Graph">
                <i class="fa-solid fa-crosshairs"></i>
              </button>
              <button class="btn btn-primary btn-sm" onclick="Vendors.findForComponent('${c.component_id}')" title="Find Alternatives">
                <i class="fa-solid fa-handshake"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }
};
