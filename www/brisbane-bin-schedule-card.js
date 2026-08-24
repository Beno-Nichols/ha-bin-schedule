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
    const image = bins?.attributes?.bin_image || next?.attributes?.bin_image;
    const collectionDay = next?.attributes?.collection_day || "Collection day unavailable";
    const date = next?.state || "Unavailable";
    this.shadowRoot.innerHTML = `<style>
      :host { display:block; font-family: var(--primary-font-family); color: var(--primary-text-color); }
      article { overflow:hidden; border-radius:12px; background:var(--ha-card-background,var(--card-background-color)); box-shadow:var(--ha-card-box-shadow); }
      header { padding:20px; background:linear-gradient(115deg,#005b96,#007f73); color:#fff; }
      h2,p { margin:0; } h2 { font-size:1.15rem; } header p { margin-top:8px; opacity:.9; }
      section { padding:0; } img { display:block; width:100%; height:auto; max-height:260px; object-fit:cover; } .empty { padding:24px; }
    </style><article><header><h2>${date}</h2><p>Collection day: ${collectionDay}</p></header><section>${image ? `<img src="${image}" alt="Bins for collection">` : "<p class=\"empty\">No bin image available.</p>"}</section></article>`;
  }

  getCardSize() { return 3; }
}
customElements.define("brisbane-bin-schedule-card", BrisbaneBinScheduleCard);
window.customCards = window.customCards || [];
window.customCards.push({ type: "brisbane-bin-schedule-card", name: "Brisbane Bin Schedule", description: "Upcoming Brisbane bin collections" });