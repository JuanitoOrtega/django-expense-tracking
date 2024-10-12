"use strict";
const formAuthentication = document.querySelector("#formAuthentication");
document.addEventListener("DOMContentLoaded", function (e) {
  var t;
  formAuthentication &&
    FormValidation.formValidation(formAuthentication, {
      fields: {
        username: {
          validators: {
            notEmpty: { message: "Por favor ingrese un usuario" },
            stringLength: {
              min: 4,
              message: "El usuario debe tener al menos 4 caracteres",
            },
            regexp: {
              regexp: /^[a-zA-Z0-9]+$/,
              message: 'El usuario solo puede contener caracteres alfanuméricos',
            },
          },
        },
        email: {
          validators: {
            notEmpty: { message: "Por favor ingresa un correo electrónico" },
            emailAddress: {
              message: "Por favor ingrese un correo electrónico válido",
            },
          },
        },
        "email-username": {
          validators: {
            notEmpty: { message: "Por favor ingrese un usuario / correo electrónico" },
            stringLength: {
              min: 4,
              message: "El usuario debe tener al menos 4 caracteres",
            },
          },
        },
        password: {
          validators: {
            notEmpty: { message: "Por favor ingresa una contraseña" },
            stringLength: {
              min: 6,
              message: "La contraseña debe tener al menos 6 caracteres",
            },
          },
        },
        "confirm-password": {
          validators: {
            notEmpty: { message: "Por favor confirme la contraseña" },
            identical: {
              compare: function () {
                return formAuthentication.querySelector('[name="password"]')
                  .value;
              },
              message: "La contraseña y su confirmación no son iguales.",
            },
            stringLength: {
              min: 6,
              message: "La contraseña debe tener al menos 6 caracteres",
            },
          },
        },
        terms: {
          validators: {
            notEmpty: { message: "Por favor acepte los Términos & Condiciones" },
          },
        },
      },
      plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap5: new FormValidation.plugins.Bootstrap5({
          eleValidClass: "",
          rowSelector: ".mb-3",
        }),
        submitButton: new FormValidation.plugins.SubmitButton(),
        defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
        autoFocus: new FormValidation.plugins.AutoFocus(),
      },
      init: (e) => {
        e.on("plugins.message.placed", function (e) {
          e.element.parentElement.classList.contains("input-group") &&
            e.element.parentElement.insertAdjacentElement(
              "afterend",
              e.messageElement
            );
        });
      },
    }),
    (t = document.querySelectorAll(".numeral-mask")).length &&
      t.forEach((e) => {
        new Cleave(e, { numeral: !0 });
      });
});
