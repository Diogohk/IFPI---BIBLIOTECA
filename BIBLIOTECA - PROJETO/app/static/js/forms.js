
document.addEventListener(“DOMContentLoaded”, function () {
    const formularios = document.querySelectorAll(“form”);

    formularios.forEach(function (formulario) {
        formulario.addEventListener(“submit”, function (evento) {
            const campos = formulario.querySelectorAll(
                “input[required], select[required], textarea[required]”
            );

            let formularioValido = true;

            campos.forEach(function (campo) {
                if (!campo.value.trim()) {
                    formularioValido = false;
                    campo.style.border = “2px solid red”;
                } else {
                    campo.style.border = “”;
                }
            });

            if (!formularioValido) {
                evento.preventDefault();
                alert(“Preencha todos os campos obrigatórios!”);
            }
        });
    });
});
