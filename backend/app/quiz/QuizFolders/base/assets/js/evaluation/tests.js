(function() {
  var self = {};

  $(document).ready(function() {
    initialize();
    enableTestCreation();
    enableTestPreview();
  });

  function initialize() {
    self.$widgetHistorial  = $('#widget-tests-historial');
    self.$widgetCreateTest = $('#widget-create-test');
    self.$modalPreviewTest = $('#modal-preview-test');
  }

  function enableTestCreation() {
    self.$widgetCreateTest.find('.submit-test').on('click', _ => {
      domain = self.$widgetCreateTest.find('.select-domain').val();
      length = self.$widgetCreateTest.find('.select-length').val();

      if (domain && length) {
        $selectedOption = self.$widgetCreateTest.find('.select-domain').find(':selected');
        scholarity      = $selectedOption.data('scholarity');
        studyCycle      = $selectedOption.data('study-cycle');

        sendTestCreationRequest(studyCycle, scholarity, domain, length);
      } else {
        var $error = $('<div>', { class: 'error-message', text: '*Selecione um valor para todos os campos.' });

        self.$widgetCreateTest.append($error);
        self.$widgetCreateTest.find('select').on('change', removeTestCreationError);
      }
    });
  }

  function enableTestPreview() {
    self.$widgetHistorial.find('.preview-test').on('click', event => {
      var $target     = $(event.target).closest('.preview-test');
      var testID      = $target.data('test-id');
      var $testFields = $target.parent().siblings();
      var $modalBody  = self.$modalPreviewTest.find('.modal-body');

      $modalBody.empty();
      $testFields.each( (index, element) => {
        var title = self.$widgetHistorial.find('th').eq(index).text();
        var value = $(element).text();

        $modalBody.append(
          $('<div>').append($('<span>', { class: 'test-field-title', text: title }))
            .append($('<span>', { text: value }))
        );
      });

      InternalAPI.evaluation.preview_test(testID)
        .done(response => {
          console.log(response);
        });
    });
  }

  function sendTestCreationRequest(studyCycle, scholarity, domain, length) {
    var params = {
      study_cycle: studyCycle,
      scholarity : scholarity,
      domain     : domain,
      length     : length
    };

    InternalAPI.evaluation.create_test(params)
      .done(_ => location.reload());
  }

  function removeTestCreationError() {
    self.$widgetCreateTest.find('.error-message').remove();
    self.$widgetCreateTest.find('select').off('change', removeTestCreationError);
  }
})();
