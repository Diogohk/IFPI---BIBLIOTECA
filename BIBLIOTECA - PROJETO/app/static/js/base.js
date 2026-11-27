document.addEventListener("DOMContentLoaded", () => {
  const themeButton = document.querySelector("#theme-toggle");
  const themeLabel = themeButton?.querySelector(".theme-toggle-label");
  const themeState = themeButton?.querySelector(".theme-toggle-state");

  function aplicarTema(tema) {
    const escuro = tema === "dark";
    document.documentElement.dataset.theme = escuro ? "dark" : "light";
    if (themeButton) {
      themeButton.setAttribute("aria-pressed", String(escuro));
      if (themeLabel) themeLabel.textContent = escuro ? "Modo claro" : "Modo escuro";
      if (themeState) themeState.textContent = escuro ? "Ativado" : "Desativado";
    }
  }

  let temaSalvo = "light";
  try { temaSalvo = localStorage.getItem("biblioteca-ifpi-theme") || "light"; } catch (error) {}
  aplicarTema(temaSalvo);

  themeButton?.addEventListener("click", () => {
    const proximo = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    aplicarTema(proximo);
    try { localStorage.setItem("biblioteca-ifpi-theme", proximo); } catch (error) {}
  });
  const dialog = document.querySelector("#feedback-dialog");
  const closeButton = document.querySelector("#feedback-close");

  if (dialog && typeof dialog.showModal === "function") {
    dialog.showModal();
    closeButton?.focus();
    closeButton?.addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  }

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });

  document.querySelectorAll("form[data-confirm-reset]").forEach((form) => {
    form.addEventListener("reset", (event) => {
      if (!window.confirm(form.dataset.confirmReset)) event.preventDefault();
    });
  });
});
