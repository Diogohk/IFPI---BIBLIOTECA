document.addEventListener("DOMContentLoaded", () => {
  const search = document.getElementById("catalog-search");
  const grid = document.getElementById("catalog-grid");
  const count = document.getElementById("catalog-count");
  const empty = document.getElementById("catalog-empty");
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".catalog-card"));

  // O catálogo usa exclusivamente a capa salva no cadastro, sem consultar ISBN/API.
  cards.forEach(card => {
    const image = card.querySelector(".catalog-cover");
    const placeholder = card.querySelector(".catalog-cover-placeholder");
    if (!image || !placeholder) return;

    image.addEventListener("load", () => {
      image.hidden = false;
      placeholder.hidden = true;
    });
    image.addEventListener("error", () => {
      image.hidden = true;
      placeholder.hidden = false;
    });
    if (image.complete && image.naturalWidth > 0) {
      image.hidden = false;
      placeholder.hidden = true;
    }
  });

  function filterCatalog() {
    if (!search || !count || !empty) return;
    const term = (search.value || "").trim().toLocaleLowerCase("pt-BR");
    let visible = 0;
    cards.forEach(card => {
      const matches = card.textContent.toLocaleLowerCase("pt-BR").includes(term);
      card.hidden = !matches;
      if (matches) visible += 1;
    });
    count.textContent = visible + " de " + cards.length + " obra(s)";
    empty.hidden = visible !== 0;
  }

  if (search) search.addEventListener("input", filterCatalog);
});
