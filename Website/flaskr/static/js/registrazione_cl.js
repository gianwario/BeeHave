  $(document).ready(function() {
    $('#contact_form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            first_name: {
                validators: {
                        stringLength: {
                        min: 2,
                    },
                        notEmpty: {
                        message: 'Perfavore inserisci il tuo Nome'
                    }
                }
            },
             last_name: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Perfavore inserisci il tuo cognome'
                    }
                }
            },
			 user_password: {
                validators: {
                     stringLength: {
                        min: 8,
                    },
                    notEmpty: {
                        message: 'Perfavore inserisci la tua Password'
                    }
                }
            },
			confirm_password: {
                validators: {
                     stringLength: {
                        min: 8,
                    },
                    notEmpty: {
                        message: 'Perfavore conferma la tua Password.'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'Perfavore inserisci il tuo indirizzo Email.'
                    },
                    emailAddress: {
                        message: 'Perfavore inserisci un indirizzo Email valido.'
                    }
                }
            },
            contact_no: {
                validators: {
                  stringLength: {
                        min: 12,
                        max: 12,
                    notEmpty: {
                        message: 'Perfavore inserisci il tuo numero di telefono.'
                     }
                }
            },
                }
            }
        })
        .on('success.form.bv', function(e) {
            $('#success_message').slideDown({ opacity: "show" }, "slow")
                $('#contact_form').data('bootstrapValidator').resetForm();


            e.preventDefault();

            var $form = $(e.target);

            var bv = $form.data('bootstrapValidator');

            $.post($form.attr('action'), $form.serialize(), function(result) {
                console.log(result);
            }, 'json');
        });
});

