const senha = document.getElementById("senha");
const toggleSenha = document.getElementById("toggleSenha");
const loginForm = document.getElementById("loginForm");
const usuario = document.getElementById("usuario");

// Alterna a visualização da senha.
toggleSenha.addEventListener("click", () => {
    const mostrarSenha = senha.type === "password";

    senha.type = mostrarSenha ? "text" : "password";
    toggleSenha.textContent = mostrarSenha ? "Ocultar" : "Mostrar";
    toggleSenha.setAttribute("aria-label", mostrarSenha ? "Ocultar senha" : "Mostrar senha");
    toggleSenha.setAttribute("aria-pressed", String(mostrarSenha));
});

// Faz uma conferência simples antes de enviar o formulário.
// A autenticação real deverá ser feita no Flask, no servidor.
loginForm.addEventListener("submit", (event) => {
    usuario.value = usuario.value.trim();

    if (usuario.value === "" || senha.value.trim() === "") {
        event.preventDefault();
        alert("Preencha todos os campos para continuar.");
    }
});
