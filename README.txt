Gaeutilities is a collection of utility classes intended to aid development
on Google's Appengine. The classes include:

More information and the demo can be found at http://gaeutilities.appspot.com
which is hosted on Appengine.

Cache: A simple caching library that stores data in both memcache and the
  datastore, attempting to work directly with memcache when possible. Cache is
  accessible as a dictionary.

Session: A robust sessions library with a focus on security. It features
  memcache and datastore interaction with rotating tokens to provide
  high levels of security and perfomance for when session data must be kept
  server side, and also supports a cookie only mode for when security is
  not a concern, and performance is of the upmost importance.

Flash: Functionality to provide next request messages, that integrates with
  Session, or can be used stand alone. Useful for those "Thank you for logging
  in" type messages.

Event: A simple subscribe/publish event model, useful for creating hooks
  within your applications.

ROTModel: (soon to be deprecated) A wrapper for db.Model that will automatically
  retry reads/writes when a timeout is encounterd. This functionality was
  introduced natively into Appengine a while ago, and this module will be
  deprecated shortly.