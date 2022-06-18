(function() {
  var self = {};

  $(document).ready(function() {
    initialize();
    enableStartStudying();
  });

  function initialize() {
    self.$widgetStudyLauncher  = $('#widget-study-launcher');
    self.$widgetStudyContainer = $('#widget-study-container');
  }

  function enableStartStudying() {
    self.$widgetStudyLauncher.find('.start-studying').on('click', _ => {
      $domain = self.$widgetStudyLauncher.find('.select-domain');
      domain  = $domain.val();

      if (domain) {
        $selectedOption = $domain.find(':selected');
        scholarity      = $selectedOption.data('scholarity');
        studyCycle      = $selectedOption.data('study-cycle');

        InternalAPI.evaluation.new({
          study_cycle: studyCycle,
          scholarity : scholarity,
          description: domain
        }).done(question => {
          self.$widgetStudyLauncher.addClass('hidden');
          self.$widgetStudyContainer.removeClass('hidden').html(question);
          enableClickingAnswerText();
          enableNextQuestionButton();
        });
      }
    });
  }

  function enableClickingAnswerText() {
    self.$widgetStudyContainer.find('.answer span').on('click', event => {
      $(event.target).siblings('input').trigger('click');
    })
  }

  function enableNextQuestionButton() {
    var $button = self.$widgetStudyContainer.find('.next-question');
    var $body   = self.$widgetStudyContainer.find('.question-body');

    $body.find('.answer').find('input').on('click', _ => {
      $button.removeClass('disabled');
      enableThrowingNextQuestion($button);
    })
  }

  function enableThrowingNextQuestion($button) {
    var $body          = self.$widgetStudyContainer.find('.question-body');
    var questionNumber = self.$widgetStudyContainer.find('.x_title').find('b').text();

    $button.off("click").on('click', _ => {
      var $answer     = $body.find(`input[name="answer_${questionNumber}"]:checked`);
      var answerIndex = $answer.val();
      var answerText  = $answer.next().text();

      InternalAPI.evaluation.next({
        answer: answerText
      }).done(question => {
        self.$widgetStudyContainer.html(question);
        enableClickingAnswerText();
        enableNextQuestionButton();
      });
    })
  }
})();
