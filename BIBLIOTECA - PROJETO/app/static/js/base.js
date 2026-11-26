document.addEventListener("DOMContentLoaded", () => {
  const dialog = document.querySelector("#feedback-dialog");
  const closeButton = document.querySelector("#feedback-close");
  if (dialog && typeof dialog.showModal === "function") {
    dialog.showModal();
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
