// Dashboard runtime: polls live-data, dispatches to widgets, exposes event bus.
// Widgets self-register via Dashboard.register('<name>', {init, render}).
//
// Each widget receives in init({el, config, bus, state}) and render(data, ctx).
// `data` is a map of alias → JSON. `ctx` exposes helpers (flash, scrollTo, etc).

window.Dashboard = (() => {
  const widgets = new Map(); // name → factory
  const mounted = [];         // [{name, el, config, state, instance}]
  const bus = new EventTarget();
  let liveData = {};          // alias → relative path
  let dataSnapshot = {};      // alias → parsed JSON
  let pollHandle = null;

  function register(name, factory) {
    widgets.set(name, factory);
  }

  function dispatch(type, detail) {
    bus.dispatchEvent(new CustomEvent(type, { detail }));
  }

  function on(type, handler) {
    bus.addEventListener(type, handler);
  }

  // Helpers for widgets
  const ctx = {
    flash(el) {
      if (!el) return;
      el.classList.remove('flash');
      void el.offsetWidth;
      el.classList.add('flash');
    },
    scrollToWidget(id, opts = {}) {
      const target = document.querySelector(`[data-widget-id="${id}"]`);
      if (target) {
        target.scrollIntoView({behavior:'smooth', block: opts.block || 'start'});
        setTimeout(() => ctx.flash(target), 300);
      }
    },
    fmtDate(ms) {
      if (!ms) return 'never';
      return new Date(ms).toISOString().split('T')[0];
    },
    fmtDateTime(ms) {
      if (!ms) return 'never';
      return new Date(ms).toISOString().replace('T',' ').slice(0,16);
    },
    daysSince(ms) {
      if (!ms) return Infinity;
      return Math.floor((Date.now() - ms) / 86400000);
    },
    getByPath(obj, path) {
      if (!path) return obj;
      // Support: foo.bar.baz, foo.bar.length, foo[0].bar, foo.bar[2]
      // Tokenize by . and [n] (where n is integer)
      const tokens = [];
      path.split('.').forEach(seg => {
        const m = seg.match(/^([^\[]*)((?:\[\d+\])*)$/);
        if (!m) return;
        if (m[1]) tokens.push(m[1]);
        const idxRe = /\[(\d+)\]/g;
        let im;
        while ((im = idxRe.exec(m[2])) !== null) tokens.push(parseInt(im[1], 10));
      });
      return tokens.reduce((o, k) => {
        if (o == null) return undefined;
        if (k === 'length' && Array.isArray(o)) return o.length;
        return o[k];
      }, obj);
    },
  };

  async function fetchAll() {
    const out = {};
    for (const [alias, path] of Object.entries(liveData)) {
      try {
        const r = await fetch(path, { cache: 'no-store' });
        out[alias] = await r.json();
      } catch (e) {
        console.warn('fetch fail', path, e);
        out[alias] = null;
      }
    }
    dataSnapshot = out;
    return out;
  }

  async function tick() {
    await fetchAll();
    for (const m of mounted) {
      try {
        m.instance.render(dataSnapshot, ctx);
      } catch (e) {
        console.error(`[widget ${m.name}] render error`, e);
      }
    }
    // Update header timestamp
    const t = new Date();
    const stamp = document.getElementById('db-updated');
    if (stamp) {
      stamp.textContent = `updated ${String(t.getHours()).padStart(2,'0')}:${String(t.getMinutes()).padStart(2,'0')}:${String(t.getSeconds()).padStart(2,'0')}`;
    }
  }

  async function init(spec) {
    liveData = spec.live_data || {};
    // Wire each section
    for (const section of spec.sections) {
      // raw_html sections are static; no widget lifecycle needed.
      if (section.raw_html !== undefined) continue;
      const factory = widgets.get(section.widget);
      if (!factory) {
        console.error('Unknown widget:', section.widget);
        continue;
      }
      const el = document.querySelector(`[data-widget-id="${section.id || section.widget}"]`);
      if (!el) {
        console.error('Mount point missing for', section.widget, section.id);
        continue;
      }
      const state = {};
      const instance = factory({ el, config: section, bus: { dispatch, on }, state, ctx });
      mounted.push({ name: section.widget, el, config: section, state, instance });
    }
    // Refresh button
    const btn = document.getElementById('db-refresh');
    if (btn) btn.addEventListener('click', async () => {
      btn.classList.add('spinning');
      await tick();
      setTimeout(() => btn.classList.remove('spinning'), 400);
    });
    // First tick + poll loop
    await tick();
    pollHandle = setInterval(tick, 5000);
  }

  return { register, init, dispatch, on, ctx };
})();
