document.addEventListener("DOMContentLoaded", () => {
  const campo = document.getElementById("consulta-search");
  const linhas = Array.from(document.querySelectorAll("#consulta-rows .consulta-row"));
  const vazio = document.getElementById("consulta-empty");

  if (!campo || linhas.length === 0) return;

  campo.addEventListener("input", () => {
    const termo = campo.value.trim().toLocaleLowerCase("pt-BR");
    let encontrados = 0;

    linhas.forEach(linha => {
      const texto = (linha.dataset.search || linha.textContent).toLocaleLowerCase("pt-BR");
      const corresponde = texto.includes(termo);
      linha.hidden = !corresponde;
      if (corresponde) encontrados += 1;
    });

    if (vazio) vazio.hidden = encontrados !== 0;
  });
});
