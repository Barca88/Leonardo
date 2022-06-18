var InternalAPI = new $.RestClient('/api/v0/', {
  cache: 5,
  cachableMethods: ["GET"]
});

InternalAPI.resources = [];
