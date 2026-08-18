const Vendors = {
  init() {
    document.getElementById('btnFindAlternatives')?.addEventListener('click', () => {
      const cmpId = document.getElementById('vendorComponentSelect')?.value;
      if (!cmpId) {
        showToast('Please select a component to evaluate', 'error');
        return;
      }
      this.fetchAlternatives(cmpId);
    });
  },

  findForComponent(componentId) {
    const tab = document.getElementById('navTabVendors');
    tab?.click();

    const select = document.getElementById('vendorComponentSelect');
    if (select) {
      select.value = componentId;
      this.fetchAlternatives(componentId);
    }
  },

  async fetchAlternatives(componentId) {
    const container = document.getElementById('vendorResultsContainer');
    if (container) {
      container.innerHTML = '<div class="empty-placeholder"><i class="fa-solid fa-spinner fa-spin"></i><p>Querying alternative suppliers across global graph...</p></div>';
    }

    try {
      const res = await API.getAlternativeVendors(componentId);
      this.render(res);
      showToast(`Found ${res.alternatives.length} alternative suppliers for ${res.target_component_name}`, 'success');
    } catch (err) {
      console.error('Failed to fetch alternative vendors:', err);
      if (container) {
        container.innerHTML = '<div class="empty-placeholder text-crimson"><i class="fa-solid fa-triangle-exclamation"></i><p>Failed to find alternative vendors.</p></div>';
      }
    }
  },

  render(response) {
    const container = document.getElementById('vendorResultsContainer');
    if (!container) return;

    if (response.alternatives.length === 0) {
      container.innerHTML = `
        <div class="empty-placeholder">
          <i class="fa-solid fa-ban text-amber"></i>
          <p><strong>Zero Alternative Suppliers Found!</strong><br>
          <span style="font-size: 11px;">${response.target_component_name} is a strict Single Point of Failure (SPOF) with no qualified second-source in the active ecosystem.</span></p>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; margin-bottom: 6px;">
        Ranked Alternatives for: <span class="text-cyan">${response.target_component_name}</span>
      </div>
    ` + response.alternatives.map(v => {
      const feasBadge = v.feasibility === 'High' ? 'badge-emerald' :
                        v.feasibility === 'Medium' ? 'badge-amber' : 'badge-crimson';

      return `
        <div class="vendor-card">
          <div class="vendor-header">
            <div>
              <div style="font-weight: 700; font-size: 14px;">${v.supplier_name}</div>
              <div style="font-size: 11px; color: var(--text-secondary);">
                ${v.country} &bull; ${v.region_name} &bull; <span class="badge" style="font-size: 9px;">${v.tier}</span>
              </div>
            </div>
            <div class="vendor-score-box">
              <div class="vendor-score">${v.overall_recommendation_score}</div>
              <div style="font-size: 10px; color: var(--text-muted);">/100</div>
            </div>
          </div>

          <div class="vendor-details-grid">
            <div class="prop-row">
              <span class="prop-key">Reliability:</span>
              <span class="prop-val text-emerald">${(v.reliability_score * 100).toFixed(0)}%</span>
            </div>
            <div class="prop-row">
              <span class="prop-key">Lead Time:</span>
              <span class="prop-val">${v.lead_time_days} days</span>
            </div>
            <div class="prop-row">
              <span class="prop-key">Supplier Risk:</span>
              <span class="prop-val ${v.risk_score > 40 ? 'text-amber' : 'text-emerald'}">${v.risk_score}/100</span>
            </div>
            <div class="prop-row">
              <span class="prop-key">Region Risk:</span>
              <span class="prop-val">${v.region_risk_index}/100</span>
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
            <span class="badge ${feasBadge}">Feasibility: ${v.feasibility}</span>
            <button class="btn btn-secondary btn-sm" onclick="GraphViz.focusNode('${v.supplier_id}')">
              <i class="fa-solid fa-eye"></i> View Supplier
            </button>
          </div>
        </div>
      `;
    }).join('');
  }
};
