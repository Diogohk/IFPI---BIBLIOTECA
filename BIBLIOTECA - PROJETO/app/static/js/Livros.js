(() => {
  "use strict";

  const form = document.querySelector("#form-livro");
  if (!form) return;

  function validarISBN(valor) {
    const isbn = valor.replace(/[ -]/g, "").toUpperCase();
    if (/^[0-9]{9}[0-9X]$/.test(isbn)) {
      const soma = [...isbn].reduce((total, char, index) =>
        total + (char === "X" ? 10 : Number(char)) * (10 - index), 0);
      if (soma % 11 === 0) return true;
    }
    if (/^[0-9]{13}$/.test(isbn)) {
      const soma = [...isbn].reduce((total, char, index) =>
        total + Number(char) * (index % 2 === 0 ? 1 : 3), 0);
      if (soma % 10 === 0) return true;
    }
    return false;
  }

  form.addEventListener("submit", (event) => {
    const erros = [];
    const titulo = form.elements.titulo.value.trim();
    const autor = form.elements.autor.value.trim();
    const isbn = form.elements.isbn.value.trim();
    const ano = form.elements.ano_publicacao.value;

    if (!titulo) erros.push("Informe o título do livro.");
    if (!autor) erros.push("Informe o autor.");
    if (!isbn) erros.push("Informe o ISBN.");
    else if (!validarISBN(isbn)) erros.push("O ISBN informado é inválido.");
    if (ano && (!Number.isInteger(Number(ano)) || Number(ano) < 1 || Number(ano) > 2100)) {
      erros.push("Informe um ano de publicação válido (entre 1 e 2100).");
    }

    if (erros.length) {
      event.preventDefault();
      window.alert("Não foi possível validar o formulário:\n\n• " + erros.join("\n• "));
    }
  });
})();
