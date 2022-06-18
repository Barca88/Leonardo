InternalAPI.add('statistics');
InternalAPI.resources.push(InternalAPI.statistics);

InternalAPI.statistics.addVerb('answers_domain', 'GET');
InternalAPI.statistics.addVerb('subdomains_domain', 'GET')
InternalAPI.statistics.addVerb('distinct_subdomain', 'GET')
InternalAPI.statistics.addVerb('answers_level', 'GET')
InternalAPI.statistics.addVerb('score_level', 'GET')
InternalAPI.statistics.addVerb('answers_degree', 'GET')
InternalAPI.statistics.addVerb('top_users', 'GET')
InternalAPI.statistics.addVerb('general_answers', 'GET')
