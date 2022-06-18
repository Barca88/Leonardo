(function() {
  var self = {};

  $(document).ready(function() {
    initialize();
    enableShowingStudents();
  });

  function initialize() {
    self.$studentsPage = $('#students-page');
  }

  function enableShowingStudents() {
    self.$studentsPage.find('.show-students-list').on('click', _ => {
      $domain = self.$studentsPage.find('.select-domain');
      domain  = $domain.val();

      if (domain) {
        $selectedOption = $domain.find(':selected');
        scholarity      = $selectedOption.data('scholarity');
        studyCycle      = $selectedOption.data('study-cycle');

        InternalAPI.students.list({
          study_cycle: studyCycle,
          scholarity : scholarity,
          description: domain
        }).done(students => {
          self.$studentsPage.find('.x_content').html(students)
        });
      }
    });
  }
})();
