document.addEventListener("DOMContentLoaded", () => {
  const search = document.getElementById("catalog-search");
  const grid = document.getElementById("catalog-grid");
  const count = document.getElementById("catalog-count");
  const empty = document.getElementById("catalog-empty");
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".catalog-card"));
  cards.forEach(async card => {
    const isbn = (card.dataset.isbn || "").replace(/[\\s-]/g, "");
    if (!isbn) return;
    try {
      const response = await fetch("https://www.googleapis.com/books/v1/volumes?q=" + encodeURIComponent("isbn:" + isbn) + "&maxResults=1");
      if (!response.ok) return;
      const data = await response.json();
      const info = data.items && data.items[0] && data.items[0].volumeInfo;
      const url = info && info.imageLinks && (info.imageLinks.thumbnail || info.imageLinks.smallThumbnail);
      if (!url) return;
      const image = card.querySelector(".catalog-cover");
      const placeholder = card.querySelector(".catalog-cover-placeholder");
      image.src = url.replace(/^http:/, "https:");
      image.hidden = false;
      placeholder.hidden = true;
    } catch (error) {
      // A ausência de capa não impede a consulta ao acervo.
    }
  });

  function filterCatalog() {
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
