const Simulation = {
  currentMode: 'supplier',
  
  init() {
    this.setupEventListeners();
  },

  setupEventListeners() {
    const segSupplier = document.getElementById('segSupplier');
    const segRegion = document.getElementById('segRegion');
    const groupSupplier = document.getElementById('groupSupplierSelect');
    const groupRegion = document.getElementById('groupRegionSelect');

    segSupplier?.addEventListener('click', () => {
      this.currentMode = 'supplier';
      segSupplier.classList.add('active');
      segRegion.classList.remove('active');
      groupSupplier.classList.remove('hidden');
      groupRegion.classList.add('hidden');
    });

    segRegion?.addEventListener('click', () => {
      this.currentMode = 'region';
      segRegion.classList.add('active');
      segSupplier.classList.remove('active');
      groupRegion.classList.remove('hidden');
      groupSupplier.classList.add('hidden');
    });

    const slider = document.getElementById('maxHopsSlider');
    const sliderBadge = document.getElementById('maxHopsValue');
    slider?.addEventListener('input', (e) => {
      if (sliderBadge) sliderBadge.innerText = `${e.target.value} Hops`;
    });

    document.getElementById('btnRunSimulation')?.addEventListener('click', () => this.run());
    document.getElementById('btnResetSimulation')?.addEventListener('click', () => this.reset());
  },

  async run() {
    const maxHops = parseInt(document.getElementById('maxHopsSlider')?.value || '3', 10);
    let payload = { max_hops: maxHops };

    if (this.currentMode === 'supplier') {
      const supplierId = document.getElementById('supplierSelect')?.value;
      if (!supplierId) {
        showToast('Please select a supplier to simulate outage', 'error');
        return;
      }
      payload.supplier_id = supplierId;
    } else {
      const regionId = document.getElementById('regionSelect')?.value;
      if (!regionId) {
        showToast('Please select a region to simulate disruption', 'error');
        return;
      }
      payload.region_id = regionId;
    }

    const btnRun = document.getElementById('btnRunSimulation');
    if (btnRun) {
      btnRun.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Calculating Blast Radius...';
      btnRun.disabled = true;
    }

    try {
      const result = await API.runDisruption(payload);
      this.displayResults(result);
      showToast(`Simulation completed! $${result.total_revenue_at_risk_millions}M revenue at risk.`, 'success');
    } catch (err) {
      console.error('Simulation execution failed:', err);
    } finally {
      if (btnRun) {
        btnRun.innerHTML = '<i class="fa-solid fa-play"></i> Simulate Cascading Failure';
        btnRun.disabled = false;
      }
    }
  },

  displayResults(result) {
    const card = document.getElementById('simulationResultCard');
    if (!card) return;

    document.getElementById('impactTargetBadge').innerText = result.target_name || result.target_id;
    document.getElementById('metricRevenueAtRisk').innerText = `$${result.total_revenue_at_risk_millions}M`;
    document.getElementById('metricAffectedProducts').innerText = result.affected_product_ids.length;
    document.getElementById('metricAffectedComponents').innerText = result.affected_component_ids.length;
    document.getElementById('metricDirectSuppliers').innerText = result.direct_suppliers_affected.length;
    document.getElementById('pathCountBadge').innerText = `${result.paths.length} Paths`;

    const pathContainer = document.getElementById('pathListContainer');
    if (pathContainer) {
      if (result.paths.length === 0) {
        pathContainer.innerHTML = `
          <div class="path-item">
            <span class="text-muted">No downstream product assembly lines disrupted.</span>
          </div>
        `;
      } else {
        pathContainer.innerHTML = result.paths.map((p) => `
          <div class="path-item">
            <div class="path-flow">
              <span class="path-node text-crimson">${p.supplier_name}</span>
              <i class="fa-solid fa-arrow-right path-arrow"></i>
              ${p.component_path.map(c => `
                <span class="path-node text-cyan">${c}</span>
                <i class="fa-solid fa-arrow-right path-arrow"></i>
              `).join('')}
              <span class="path-node text-purple">${p.product_name}</span>
            </div>
            <div class="path-rev">
              Revenue at Risk: $${p.quarterly_revenue_millions}M / Qtr
            </div>
          </div>
        `).join('');
      }
    }

    card.classList.remove('hidden');

    const allAffected = [
      ...result.affected_component_ids,
      ...result.affected_product_ids
    ];
    GraphViz.highlightBlastRadius(result.target_id, allAffected);
  },

  reset() {
    const card = document.getElementById('simulationResultCard');
    if (card) card.classList.add('hidden');
    GraphViz.resetHighlight();
    showToast('Graph visualization reset to normal state', 'info');
  },

  triggerForEntity(type, entityId) {
    const simTab = document.getElementById('navTabSimulation');
    simTab?.click();

    if (type === 'supplier') {
      const segSupplier = document.getElementById('segSupplier');
      segSupplier?.click();
      const select = document.getElementById('supplierSelect');
      if (select) {
        select.value = entityId;
        this.run();
      }
    } else if (type === 'region') {
      const segRegion = document.getElementById('segRegion');
      segRegion?.click();
      const select = document.getElementById('regionSelect');
      if (select) {
        select.value = entityId;
        this.run();
      }
    }
  }
};
