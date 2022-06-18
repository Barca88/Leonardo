(function() {
  var self = {};

  $(document).ready(function() {
    initialize();
    get_domains_map();
    enableChangingSubdomainsSelect();
  });

  function initialize() {
    self.$domainSelect = $('#domainChoice');
  }

  function get_domains_map() {
    InternalAPI.questions.domains_map().done(map => self.domainsMap = JSON.parse(map));
  }

  function setSubdomainOptions(subdomainsList) {
    $('#subdomainChoice').html($('<option>', { value: '', text: '-- Escolha um subdomínio --' }));

    for(var i = 0; i < subdomainsList.length; i++) {
      var $option = $('<option>', { value: subdomainsList[i]['description'], text: subdomainsList[i]['description'] });

      $('#subdomainChoice').append($option);
    }
  }

  function enableChangingSubdomainsSelect() {
    self.$domainSelect.change(event => {
      domain = $(event.target).val();

      if (domain) {
        $selectedOption = $(event.target).find(':selected');
        scholarity      = $selectedOption.data('scholarity');
        studyCycle      = $selectedOption.data('study-cycle');
        setSubdomainOptions(self.domainsMap[domain]['subdomains']);
      }
      else {
        $('#subdomainChoice').html($('<option>', { value: '', text: '-- Escolha um subdomínio --' }));
      }
    })
  }
})();
