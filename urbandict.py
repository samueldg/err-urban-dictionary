import json
import urllib.request
import urllib.parse

from errbot import botcmd
from errbot import BotPlugin


class UrbanDictionary(BotPlugin):

    api_url = 'http://api.urbandictionary.com/v0'
    search_url_template = api_url + '/define?term={0}'
    random_term_url = api_url + '/random'

    @botcmd
    def ud(self, msg, args):
        """Looks up a term on urban dictionary"""

        if not args:
            # Get random definitions if no term is provided
            definitions = self.get_json(self.random_term_url)
        else:
            # Otherwise, get the definitions of the search term
            escaped_term = urllib.parse.quote(args)
            search_url = self.search_url_template.format(escaped_term)
            definitions = self.get_json(search_url)

            if definitions['result_type'] == 'no_results':
                return 'No such term: {0}!'.format(args)

        best_definition = definitions['list'][0]
        card_fields = self.format_definition_card(best_definition)
        self.send_card(in_reply_to=msg, **card_fields)

    @staticmethod
    def get_json(url):
        """Fetch a URL returning JSON, and return it as a dict."""
        with urllib.request.urlopen(url) as api_response:
            return json.load(api_response)

    @staticmethod
    def format_definition_card(definition):
        """Formats a definition JSON from Urban Dictionary into a dictionary
        containing the keyword arguments for `BotPlugin.send_card()`.
        """
        return {
            'title': definition['word'],
            'body': '\n\n'.join([definition['definition'], definition['example']]),
            'link': definition['permalink'],
            'fields': (
                ('thumbs_up', definition.get('thumbs_up', 0)),
                ('thumbs_down', definition.get('thumbs_down', 0)),
            )
        }
