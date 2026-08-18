const GraphViz = {
  network: null,
  nodesDataSet: null,
  edgesDataSet: null,
  rawGraphData: { nodes: [], edges: [] },
  isPhysicsEnabled: true,

  colors: {
    Supplier: { background: '#10b981', border: '#047857', highlight: '#34d399' },
    Component: { background: '#06b6d4', border: '#0e7490', highlight: '#38bdf8' },
    Product: { background: '#8b5cf6', border: '#6d28d9', highlight: '#a78bfa' },
    Facility: { background: '#f59e0b', border: '#b45309', highlight: '#fbbf24' },
    Region: { background: '#f43f5e', border: '#be123c', highlight: '#fb7185' },
    Disrupted: { background: '#ef4444', border: '#991b1b', highlight: '#f87171' },
    Dimmed: { background: '#1e293b', border: '#334155', highlight: '#475569' }
  },

  init(containerId = 'visGraphNetwork') {
    const container = document.getElementById(containerId);
    if (!container) return;

    this.nodesDataSet = new vis.DataSet([]);
    this.edgesDataSet = new vis.DataSet([]);

    const data = {
      nodes: this.nodesDataSet,
      edges: this.edgesDataSet
    };

    const options = {
      nodes: {
        shape: 'dot',
        size: 22,
        font: {
          color: '#f8fafc',
          size: 13,
          face: 'Inter',
          strokeWidth: 3,
          strokeColor: '#070b14'
        },
        borderWidth: 2,
        shadow: {
          enabled: true,
          color: 'rgba(0,0,0,0.6)',
          size: 8,
          x: 2,
          y: 4
        }
      },
      edges: {
        width: 1.5,
        color: {
          color: 'rgba(148, 163, 184, 0.3)',
          highlight: '#3b82f6',
          hover: '#60a5fa'
        },
        arrows: {
          to: { enabled: true, scaleFactor: 0.7 }
        },
        font: {
          color: '#94a3b8',
          size: 10,
          face: 'Inter',
          align: 'middle',
          strokeWidth: 2,
          strokeColor: '#070b14'
        },
        smooth: {
          type: 'continuous',
          roundness: 0.2
        }
      },
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -70,
          centralGravity: 0.015,
          springLength: 120,
          springConstant: 0.08,
          damping: 0.85
        },
        stabilization: {
          enabled: true,
          iterations: 150,
          updateInterval: 25
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 150,
        zoomView: true,
        dragView: true,
        navigationButtons: false
      }
    };

    this.network = new vis.Network(container, data, options);

    this.network.on('click', (params) => this.handleNodeClick(params));
    this.network.on('doubleClick', (params) => this.handleNodeDoubleClick(params));

    this.setupCanvasControls();
  },

  setupCanvasControls() {
    document.getElementById('btnFitGraph')?.addEventListener('click', () => this.fit());
    document.getElementById('btnZoomIn')?.addEventListener('click', () => this.zoom(1.2));
    document.getElementById('btnZoomOut')?.addEventListener('click', () => this.zoom(0.8));
    document.getElementById('btnStabilize')?.addEventListener('click', () => this.stabilize());
    document.getElementById('btnCloseInspector')?.addEventListener('click', () => this.hideInspector());

    const chkPhysics = document.getElementById('chkPhysics');
    if (chkPhysics) {
      chkPhysics.addEventListener('change', (e) => {
        this.setPhysics(e.target.checked);
      });
    }
  },

  loadGraph(graphData) {
    if (!graphData) return;
    this.rawGraphData = graphData;

    const formattedNodes = (graphData.nodes || []).map(n => {
      const labelType = n.label || 'Component';
      const colorScheme = this.colors[labelType] || this.colors.Component;
      const size = labelType === 'Product' ? 28 : labelType === 'Supplier' ? 24 : 20;

      return {
        id: n.id,
        label: n.name || n.id,
        title: `[${labelType}] ${n.name || n.id}`,
        shape: labelType === 'Product' ? 'diamond' : labelType === 'Region' ? 'hexagon' : 'dot',
        size: size,
        color: {
          background: colorScheme.background,
          border: colorScheme.border,
          highlight: {
            background: colorScheme.highlight,
            border: '#ffffff'
          }
        },
        raw: n
      };
    });

    const formattedEdges = (graphData.edges || []).map(e => ({
      id: e.id || `${e.from}->${e.to}`,
      from: e.from,
      to: e.to,
      label: e.label || '',
      title: e.label || '',
      raw: e
    }));

    this.nodesDataSet.clear();
    this.edgesDataSet.clear();

    this.nodesDataSet.add(formattedNodes);
    this.edgesDataSet.add(formattedEdges);

    this.fit();
  },

  highlightBlastRadius(disruptedTargetId, affectedNodeIds, pathEdgeIds = []) {
    const allNodes = this.nodesDataSet.get();
    const allEdges = this.edgesDataSet.get();

    const affectedSet = new Set(affectedNodeIds);
    affectedSet.add(disruptedTargetId);

    const updatedNodes = allNodes.map(node => {
      if (node.id === disruptedTargetId) {
        return {
          ...node,
          color: {
            background: '#ef4444',
            border: '#ffffff',
            highlight: { background: '#f87171', border: '#ffffff' }
          },
          size: 32,
          font: { color: '#fca5a5', size: 15, strokeWidth: 4 }
        };
      } else if (affectedSet.has(node.id)) {
        return {
          ...node,
          color: {
            background: '#f43f5e',
            border: '#fda4af',
            highlight: { background: '#fb7185', border: '#ffffff' }
          },
          size: node.size * 1.25,
          font: { color: '#fecdd3', size: 13, strokeWidth: 3 }
        };
      } else {
        return {
          ...node,
          color: {
            background: 'rgba(30, 41, 59, 0.4)',
            border: 'rgba(51, 65, 85, 0.3)',
            highlight: { background: '#334155', border: '#475569' }
          },
          font: { color: 'rgba(148, 163, 184, 0.3)', size: 10, strokeWidth: 1 }
        };
      }
    });

    const updatedEdges = allEdges.map(edge => {
      const isAffected = affectedSet.has(edge.from) && affectedSet.has(edge.to);
      return {
        ...edge,
        color: {
          color: isAffected ? '#ef4444' : 'rgba(148, 163, 184, 0.08)',
          highlight: isAffected ? '#f87171' : 'rgba(148, 163, 184, 0.2)'
        },
        width: isAffected ? 3 : 1
      };
    });

    this.nodesDataSet.update(updatedNodes);
    this.edgesDataSet.update(updatedEdges);
  },

  resetHighlight() {
    if (this.rawGraphData && this.rawGraphData.nodes) {
      this.loadGraph(this.rawGraphData);
    }
  },

  handleNodeClick(params) {
    if (params.nodes && params.nodes.length > 0) {
      const nodeId = params.nodes[0];
      const nodeItem = this.nodesDataSet.get(nodeId);
      if (nodeItem && nodeItem.raw) {
        this.showInspector(nodeItem.raw);
      }
    } else {
      this.hideInspector();
    }
  },

  handleNodeDoubleClick(params) {
    if (params.nodes && params.nodes.length > 0) {
      const nodeId = params.nodes[0];
      this.focusNode(nodeId);
    }
  },

  focusNode(nodeId) {
    if (!this.network) return;
    this.network.focus(nodeId, {
      scale: 1.3,
      animation: {
        duration: 800,
        easingFunction: 'easeInOutQuad'
      }
    });
  },

  showInspector(rawNode) {
    const panel = document.getElementById('nodeInspectorPanel');
    const badge = document.getElementById('inspectorNodeTypeBadge');
    const nameEl = document.getElementById('inspectorNodeName');
    const propsGrid = document.getElementById('inspectorProperties');
    const btnSimulate = document.getElementById('btnSimulateThisNode');
    const btnFindAlt = document.getElementById('btnFindAltForThisNode');

    if (!panel) return;

    badge.innerText = rawNode.label;
    badge.className = `badge badge-${rawNode.label.toLowerCase()}`;
    nameEl.innerText = rawNode.name || rawNode.id;

    propsGrid.innerHTML = '';
    const props = rawNode.properties || {};
    
    propsGrid.innerHTML += `
      <div class="prop-row">
        <span class="prop-key">Entity ID:</span>
        <span class="prop-val">${rawNode.id}</span>
      </div>
    `;

    for (const [k, v] of Object.entries(props)) {
      if (k !== 'id' && k !== 'name') {
        let displayVal = typeof v === 'number' && k.includes('revenue') ? `$${v}M` :
                         typeof v === 'number' && k.includes('cost') ? `$${v.toLocaleString()}` : v;
        propsGrid.innerHTML += `
          <div class="prop-row">
            <span class="prop-key">${k.replace(/_/g, ' ')}:</span>
            <span class="prop-val">${displayVal}</span>
          </div>
        `;
      }
    }

    if (rawNode.label === 'Supplier' || rawNode.label === 'Region') {
      btnSimulate.classList.remove('hidden');
      btnSimulate.onclick = () => {
        Simulation.triggerForEntity(rawNode.label.toLowerCase(), rawNode.id);
        this.hideInspector();
      };
    } else {
      btnSimulate.classList.add('hidden');
    }

    if (rawNode.label === 'Component') {
      btnFindAlt.classList.remove('hidden');
      btnFindAlt.onclick = () => {
        Vendors.findForComponent(rawNode.id);
        this.hideInspector();
      };
    } else {
      btnFindAlt.classList.add('hidden');
    }

    panel.classList.remove('hidden');
  },

  hideInspector() {
    const panel = document.getElementById('nodeInspectorPanel');
    if (panel) panel.classList.add('hidden');
  },

  fit() {
    if (this.network) {
      this.network.fit({
        animation: { duration: 600, easingFunction: 'easeInOutQuad' }
      });
    }
  },

  zoom(factor) {
    if (!this.network) return;
    const currentScale = this.network.getScale();
    this.network.moveTo({
      scale: currentScale * factor,
      animation: { duration: 300 }
    });
  },

  stabilize() {
    if (this.network) this.network.stabilize();
  },

  setPhysics(enabled) {
    this.isPhysicsEnabled = enabled;
    if (this.network) {
      this.network.setOptions({ physics: { enabled } });
    }
  }
};
