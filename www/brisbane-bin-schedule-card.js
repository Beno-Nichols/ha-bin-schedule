class BrisbaneBinScheduleCard extends HTMLElement {
  setConfig(config) {
    if (!config.next_entity || !config.bins_entity) throw new Error("next_entity and bins_entity are required");
    this.config = config;
    this.attachShadow({ mode: "open" });
  }

  set hass(hass) {
    this._hass = hass;
    const next = hass.states[this.config.next_entity];
    const bins = hass.states[this.config.bins_entity];
    const upcoming = next?.attributes?.upcoming || [];
    this.shadowRoot.innerHTML = `<style>
      :host { display:block; font-family: var(--primary-font-family); color: var(--primary-text-color); }
      article { overflow:hidden; border-radius:12px; background:var(--ha-card-background,var(--card-background-color)); box-shadow:var(--ha-card-box-shadow); }
      header { padding:20px; background:linear-gradient(115deg,#005b96,#007f73); color:#fff; }
      h2,p { margin:0; } h2 { font-size:1.15rem; } header p { margin-top:8px; opacity:.9; }
      section { padding:14px 20px 18px; } .bin { display:flex; align-items:center; gap:12px; padding:8px 0; border-bottom:1px solid var(--divider-color); }
      .bin:last-child { border:0; } img { width:52px; height:36px; object-fit:cover; border-radius:6px; } small { color:var(--secondary-text-color); display:block; margin-top:3px; }
    </style><article><header><h2>${this.config.title || "Bin collection"}</h2><p>${next?.state || "Unavailable"} | ${bins?.state || "No bins listed"}</p></header><section>${upcoming.slice(0, 4).map(item => `<div class="bin"><img src="${item.bin.toLowerCase().includes("recycl") ? "https://www.brisbane.qld.gov.au/content/dam/brisbanecitycouncil/common/images/General-and-Recycling-bins-V3.jpg" : "https://www.brisbane.qld.gov.au/content/dam/brisbanecitycouncil/common/images/General-and-Green-Waste-bins-V3.jpg"}"><div><strong>${item.bin}</strong><small>${item.date}</small></div></div>`).join("") || "<p>No upcoming collections.</p>"}</section></article>`;
  }

  getCardSize() { return 3; }
}
customElements.define("brisbane-bin-schedule-card", BrisbaneBinScheduleCard);
window.customCards = window.customCards || [];
window.customCards.push({ type: "brisbane-bin-schedule-card", name: "Brisbane Bin Schedule", description: "Upcoming Brisbane bin collections" });