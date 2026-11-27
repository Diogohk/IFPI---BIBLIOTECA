document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("google-books-query");
  const searchButton = document.getElementById("google-books-search");
  const results = document.getElementById("google-books-results");
  const status = document.getElementById("google-books-status");
  if (!input || !searchButton || !results || !status) return;

  const fields = {
    title: document.getElementById("titulo"),
    author: document.getElementById("autor"),
    isbn: document.getElementById("isbn"),
    publisher: document.getElementById("editora"),
    year: document.getElementById("ano_publicacao")
  };

  function getIsbn(volume) {
    const ids = volume.industryIdentifiers || [];
    const preferred = ids.find(item => item.type === "ISBN_13") || ids.find(item => item.type === "ISBN_10");
    return preferred ? preferred.identifier : "";
  }

  function selectBook(volume) {
    const info = volume.volumeInfo || {};
    fields.title.value = info.title || "";
    fields.author.value = (info.authors || []).join(", ");
    fields.isbn.value = getIsbn(volume);
    fields.publisher.value = info.publisher || "";
    const year = (info.publishedDate || "").match(/^\d{4}/);
    fields.year.value = year ? year[0] : "";
    fields.title.dispatchEvent(new Event("input", { bubbles: true }));
    fields.isbn.dispatchEvent(new Event("input", { bubbles: true }));
    status.textContent = "Dados preenchidos. Confira as informações e valide o ISBN antes de salvar.";
    results.innerHTML = "";
    fields.title.focus();
  }

  async function searchBooks() {
    const term = input.value.trim();
    if (!term) {
      status.textContent = "Digite um ISBN ou título para pesquisar.";
      return;
    }
    const normalized = term.replace(/[\s-]/g, "");
    const query = /^\d{10,13}$/.test(normalized)
      ? "isbn:" + normalized
      : "intitle:" + term;

    searchButton.disabled = true;
    status.textContent = "Pesquisando no Google Books...";
    results.innerHTML = "";

    try {
      const response = await fetch("/api/google-books?q=" + encodeURIComponent(query));
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "A API respondeu com erro.");
      const items = data.items || [];
      if (!items.length) {
        status.textContent = "Nenhum resultado encontrado. Você ainda pode preencher os campos manualmente.";
        return;
      }
      status.textContent = items.length + " resultado(s). Selecione a obra correta:";
      items.forEach(volume => {
        const info = volume.volumeInfo || {};
        const item = document.createElement("article");
        item.className = "google-book-result";
        const cover = document.createElement("img");
        const imageUrl = info.imageLinks && info.imageLinks.thumbnail;
        if (imageUrl) cover.src = imageUrl.replace(/^http:/, "https:");
        else cover.hidden = true;
        cover.alt = "";
        const details = document.createElement("div");
        const title = document.createElement("strong");
        title.textContent = info.title || "Título não informado";
        const meta = document.createElement("small");
        meta.textContent = (info.authors || ["Autor não informado"]).join(", ") + " · " + (info.publisher || "Editora não informada");
        details.append(title, meta);
        const choose = document.createElement("button");
        choose.type = "button";
        choose.className = "button button-secondary";
        choose.textContent = "Selecionar";
        choose.addEventListener("click", () => selectBook(volume));
        item.append(cover, details, choose);
        results.appendChild(item);
      });
    } catch (error) {
      status.textContent = error.message || "Não foi possível acessar o Google Books agora. Tente novamente ou preencha manualmente.";
    } finally {
      searchButton.disabled = false;
    }
  }

  searchButton.addEventListener("click", searchBooks);
  input.addEventListener("keydown", event => {
    if (event.key === "Enter") {
      event.preventDefault();
      searchBooks();
    }
  });
});
