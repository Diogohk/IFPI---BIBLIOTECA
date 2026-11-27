document.addEventListener("DOMContentLoaded", () => {
  const search = document.getElementById("catalog-search");
  const grid = document.getElementById("catalog-grid");
  const count = document.getElementById("catalog-count");
  const empty = document.getElementById("catalog-empty");
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".catalog-card"));

  function normalizeIsbn(value) {
    return (value || "").replace(/[\s-]/g, "").toUpperCase();
  }

  function hasMatchingIsbn(volume, expectedIsbn) {
    const identifiers = (volume.volumeInfo && volume.volumeInfo.industryIdentifiers) || [];
    return identifiers.some(identifier =>
      normalizeIsbn(identifier.identifier) === expectedIsbn
    );
  }

  function getCoverUrls(volume) {
    const links = (volume.volumeInfo && volume.volumeInfo.imageLinks) || {};
    return [links.thumbnail, links.smallThumbnail]
      .filter(Boolean)
      .map(url => url.replace(/^http:/i, "https:"));
  }

  cards.forEach(async card => {
    const isbn = normalizeIsbn(card.dataset.isbn);
    const image = card.querySelector(".catalog-cover");
    const placeholder = card.querySelector(".catalog-cover-placeholder");
    if (!isbn || !image || !placeholder) return;

    try {
      const query = "isbn:" + isbn;
      const response = await fetch("/api/google-books?q=" + encodeURIComponent(query));
      if (!response.ok) return;

      const data = await response.json();
      const volume = (data.items || []).find(item => hasMatchingIsbn(item, isbn));
      if (!volume) return;

      const coverUrls = getCoverUrls(volume);
      if (!coverUrls.length) return;

      // Só troca o espaço reservado depois que uma capa válida carregar.
      let index = 0;
      const tryNextCover = () => {
        if (index >= coverUrls.length) {
          image.hidden = true;
          placeholder.hidden = false;
          return;
        }
        image.src = coverUrls[index++];
      };

      image.onload = () => {
        image.hidden = false;
        placeholder.hidden = true;
      };
      image.onerror = tryNextCover;
      tryNextCover();
    } catch (error) {
      // A ausência de capa não impede a consulta ao acervo.
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
