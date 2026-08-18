const API = {
  baseURL: '',

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      if (data.cypher_trace) {
        CypherDrawer.updateTrace(data.cypher_trace);
      }

      return data;
    } catch (error) {
      console.error(`API Request Error [${endpoint}]:`, error);
      showToast(error.message, 'error');
      throw error;
    }
  },

  async getHealth() {
    return this.request('/api/health');
  },

  async reconnect() {
    return this.request('/api/health/reconnect', { method: 'POST' });
  },

  async getGraph(nodeType = null, search = null) {
    const params = new URLSearchParams();
    if (nodeType) params.append('node_type', nodeType);
    if (search) params.append('search', search);
    return this.request(`/api/graph?${params.toString()}`);
  },

  async getEntities() {
    return this.request('/api/graph/entities');
  },

  async runDisruption(payload) {
    return this.request('/api/simulation/disrupt', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },

  async getSPOFAnalysis() {
    return this.request('/api/spof');
  },

  async getAlternativeVendors(componentId, disruptedSupplierId = null) {
    const params = new URLSearchParams({ component_id: componentId });
    if (disruptedSupplierId) params.append('disrupted_supplier_id', disruptedSupplierId);
    return this.request(`/api/vendors/alternatives?${params.toString()}`);
  },

  async seedDatabase() {
    return this.request('/api/seed', { method: 'POST' });
  }
};

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icon = type === 'success' ? 'fa-check-circle text-emerald' :
               type === 'error' ? 'fa-triangle-exclamation text-crimson' : 'fa-info-circle text-cyan';
               
  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(30px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
