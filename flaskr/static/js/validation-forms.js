
// Si los formularios validan ok, se devuelve TRUE, es decir, se continúa el flujo normal del formulario
jQuery.validator.setDefaults({
    submitHandler: function() {
        jQuery('input[type="submit"]').attr('disabled', 'disabled');
        return true;
    }
});

jQuery().ready(function() {
    // Se validan los formularios al hacer keyup y submit

    jQuery("#form_contacto").validate({
        rules: {
            nombre: "required",
            email: {
                required: true,
                email: true
            },
            mensaje: {
                required: true,
                minlength: 5
            },
            documento: "required",
        },
        messages: {
            nombre: "El nombre es obligatorio",
            email: "Por favor introduce un email válido",
            mensaje: {
                required: "Por favor redacta tu mensaje",
                minlength: "Tu mensaje es demasiado corto"
            },
            documento: "El documento es obligatorio",
        }
    });
});
