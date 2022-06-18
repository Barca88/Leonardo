InternalAPI.add('evaluation');
InternalAPI.resources.push(InternalAPI.evaluation);

InternalAPI.evaluation.addVerb('create_test', 'POST');
InternalAPI.evaluation.addVerb('preview_test', 'GET');
InternalAPI.evaluation.addVerb('get_domains', 'GET');
InternalAPI.evaluation.addVerb('new', 'GET', { 'ajax': { 'dataType': 'html' } });
InternalAPI.evaluation.addVerb('next', 'POST');
