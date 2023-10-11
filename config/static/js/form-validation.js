"use strict";!function(){window.Helpers.initCustomOptionCheck();var e=[].slice.call(document.querySelectorAll(".flatpickr-validation")),e=(e&&e.forEach(e=>{e.flatpickr({allowInput:!0,monthSelectorType:"static"})}),document.querySelectorAll(".needs-validation"));Array.prototype.slice.call(e).forEach(function(a){a.addEventListener("submit",function(e){a.checkValidity()?alert("Submitted!!!"):(e.preventDefault(),e.stopPropagation()),a.classList.add("was-validated")},!1)})}(),document.addEventListener("DOMContentLoaded",function(e){{const a=document.getElementById("formValidationExamples"),t=jQuery(a.querySelector('[name="formValidationSelect2"]')),o=jQuery(a.querySelector('[name="formValidationTech"]')),n=a.querySelector('[name="formValidationLang"]'),i=jQuery(a.querySelector('[name="formValidationHobbies"]')),l=FormValidation.formValidation(a,{fields:{formValidationName:{validators:{notEmpty:{message:"Please enter your name"},stringLength:{min:6,max:30,message:"The name must be more than 6 and less than 30 characters long"},regexp:{regexp:/^[a-zA-Z0-9 ]+$/,message:"The name can only consist of alphabetical, number and space"}}},formValidationEmail:{validators:{notEmpty:{message:"Por favor ingresa un correo electrónico"},emailAddress:{message:"The value is not a valid email address"}}},formValidationPass:{validators:{notEmpty:{message:"Por favor ingresa una contraseña"}}},formValidationConfirmPass:{validators:{notEmpty:{message:"Please confirm password"},identical:{compare:function(){return a.querySelector('[name="formValidationPass"]').value},message:"The password and its confirm are not the same"}}},formValidationFile:{validators:{notEmpty:{message:"Please select the file"}}},formValidationDob:{validators:{notEmpty:{message:"Please select your DOB"},date:{format:"YYYY/MM/DD",message:"The value is not a valid date"}}},formValidationSelect2:{validators:{notEmpty:{message:"Please select your country"}}},formValidationLang:{validators:{notEmpty:{message:"Please add your language"}}},formValidationTech:{validators:{notEmpty:{message:"Please select technology"}}},formValidationHobbies:{validators:{notEmpty:{message:"Please select your hobbies"}}},formValidationBio:{validators:{notEmpty:{message:"Please enter your bio"},stringLength:{min:100,max:500,message:"The bio must be more than 100 and less than 500 characters long"}}},formValidationGender:{validators:{notEmpty:{message:"Please select your gender"}}},formValidationPlan:{validators:{notEmpty:{message:"Please select your preferred plan"}}},formValidationSwitch:{validators:{notEmpty:{message:"Please select your preference"}}},formValidationCheckbox:{validators:{notEmpty:{message:"Please confirm our T&C"}}}},plugins:{trigger:new FormValidation.plugins.Trigger,bootstrap5:new FormValidation.plugins.Bootstrap5({eleValidClass:"",rowSelector:function(e,a){switch(e){case"formValidationName":case"formValidationEmail":case"formValidationPass":case"formValidationConfirmPass":case"formValidationFile":case"formValidationDob":case"formValidationSelect2":case"formValidationLang":case"formValidationTech":case"formValidationHobbies":case"formValidationBio":case"formValidationGender":return".col-md-6";case"formValidationPlan":return".col-xl-3";case"formValidationSwitch":case"formValidationCheckbox":return".col-12";default:return".row"}}}),submitButton:new FormValidation.plugins.SubmitButton,defaultSubmit:new FormValidation.plugins.DefaultSubmit,autoFocus:new FormValidation.plugins.AutoFocus},init:e=>{e.on("plugins.message.placed",function(e){e.element.parentElement.classList.contains("input-group")&&e.element.parentElement.insertAdjacentElement("afterend",e.messageElement),e.element.parentElement.parentElement.classList.contains("custom-option")&&e.element.closest(".row").insertAdjacentElement("afterend",e.messageElement)})}});flatpickr(a.querySelector('[name="formValidationDob"]'),{enableTime:!1,dateFormat:"Y/m/d",onChange:function(){l.revalidateField("formValidationDob")}}),t.length&&(t.wrap('<div class="position-relative"></div>'),t.select2({placeholder:"Select country",dropdownParent:t.parent()}).on("change.select2",function(){l.revalidateField("formValidationSelect2")})),new Tagify(n),n.addEventListener("change",function(){l.revalidateField("formValidationLang")}),o.on("changed.bs.select",function(e,a,t,o){l.revalidateField("formValidationTech")}),i.on("changed.bs.select",function(e,a,t,o){l.revalidateField("formValidationHobbies")})}});