(() => {
  "use strict";

  const form = document.querySelector("#form-livro");
  if (!form) return;

  const isbnField = form.elements.isbn;

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

  function atualizarValidadeISBN() {
    const valor = isbnField.value.trim();
    isbnField.setCustomValidity(
      valor && !validarISBN(valor) ? "O ISBN informado não é válido." : ""
    );
  }

  isbnField.addEventListener("input", atualizarValidadeISBN);
  atualizarValidadeISBN();
})();
