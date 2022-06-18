InternalAPI.add('accounts', { isSingle: true });
InternalAPI.resources.push(InternalAPI.accounts);

InternalAPI.accounts.add('upload_avatar', { url: 'avatar/upload' });
InternalAPI.accounts.addVerb('change_password', 'POST', { url: 'password/change' });
