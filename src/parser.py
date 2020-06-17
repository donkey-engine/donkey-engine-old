from webargs.aiohttpparser import AIOHTTPParser


class Parser(AIOHTTPParser):
    DEFAULT_VALIDATION_STATUS = 400

    async def _on_validation_error(self, error, req, schema, location,
                                   error_status_code, error_headers):
        '''
        Redefenition to remove location from reponse.
        https://github.com/marshmallow-code/webargs/issues/460
        '''
        error_handler = self.error_callback or self.handle_error
        await error_handler(error, req, schema,
                            error_status_code=error_status_code,
                            error_headers=error_headers)


parser = Parser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
