
(() => {
  "use strict";

  const form = document.querySelector("#form-livro");

  if (!form) return;

  const feedback = document.querySelector("#form-feedback");

  function validarISBN(isbn) {
    isbn = isbn.replace(/[\s-]/g, "").toUpperCase();

    // Validação ISBN-10
    if (/^\d{9}[\dX]$/.test(isbn)) {
      const soma = [...isbn].reduce((total, char, index) => {
        const numero = char === "X" ? 10 : Number(char);
        return total + numero * (10 - index);
      }, 0);

      if (soma % 11 === 0) return true;
    }

    // Validação ISBN-13
    if (/^\d{13}$/.test(isbn)) {
      const soma = [...isbn].reduce((total, char, index) => {
        return total + Number(char) * (index % 2 === 0 ? 1 : 3);
      }, 0);

      if (soma % 10 === 0) return true;
    }

    return false;
  }

  function mostrarErro(campo, mensagem) {
    const elemento = document.querySelector(`#erro-${campo}`);
    const input = form.elements[campo];

    if (elemento) elemento.textContent = mensagem;

    if (input) {
      input.setAttribute(
        "aria-invalid",
        mensagem ? "true" : "false"
      );
    }
  }

  form.addEventListener("submit", (event) => {
    let valido = true;

    feedback.textContent = "";

    const titulo = form.elements.titulo.value.trim();
    const autor = form.elements.autor.value.trim();
    const isbn = form.elements.isbn.value.trim();
    const ano = form.elements.ano_publicacao.value;

    if (!titulo) {
      mostrarErro("titulo", "Informe o título do livro.");
      valido = false;
    } else {
      mostrarErro("titulo", "");
    }

    if (!autor) {
      mostrarErro("autor", "Informe o autor.");
      valido = false;
    } else {
      mostrarErro("autor", "");
    }

    if (!isbn) {
      mostrarErro("isbn", "Informe o ISBN.");
      valido = false;
    } else if (!validarISBN(isbn)) {
      mostrarErro("isbn", "ISBN inválido.");
      valido = false;
    } else {
      mostrarErro("isbn", "");
    }

    if (ano && (!Number.isInteger(Number(ano)) ||
        Number(ano) < 1 || Number(ano) > 2100)) {
      mostrarErro("ano_publicacao", "Informe um ano válido.");
      valido = false;
    } else {
      mostrarErro("ano_publicacao", "");
    }

    if (!valido) {
      event.preventDefault();
      feedback.textContent =
        "Confira os campos destacados antes de continuar.";
    }
  });

  form.addEventListener("reset", () => {
    setTimeout(() => {
      document.querySelectorAll(".field-error").forEach((campo) => {
        campo.textContent = "";
      });

      form.querySelectorAll("[aria-invalid]").forEach((campo) => {
        campo.removeAttribute("aria-invalid");
      });

      feedback.textContent = "";
    }, 0);
  });
})();
