import logging
import re
import pkg_resources
import urlparse

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer, Boolean
from xblock.fragment import Fragment
from xblock.validation import ValidationMessage
from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblockutils.resources import ResourceLoader

log = logging.getLogger(__name__)


class ColabXBlock(XBlock, StudioEditableXBlockMixin):
    """Adds link to google colab with optional HTML instructions"""

    display_name = String(
        display_name="Display Name", default="Colab XBlock",
        scope=Scope.settings,
        help="Name of this XBlock"
    )

    button_text = String(
        help="Button Text",
        scope=Scope.content,
        display_name="Button Text",
        default="Open Notebook"
    )

    instructions = String(
        help="Optional Instructions",
        scope=Scope.content,
        display_name="Instructions",
        default="",
        multiline_editor='html',
    )

    notebook_url = String(
        help="Fully qualified Link to github notebook or colab.research.google.com/drive/ ... link",
        display_name="Notebook URL",
        scope=Scope.content,
        default="https://colab.research.google.com/notebooks/welcome.ipynb"
    )

    editable_fields = ('display_name', 'button_text', 'notebook_url', 'instructions')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def validate_field_data(self, validation, data):
        """Ensure Notebook URL starts with https:// or http://"""
        url = data.notebook_url
        if not url.startswith('https://') and not url.startswith('http://'):
            validation.add(
                ValidationMessage(
                    ValidationMessage.ERROR, 
                    u"Notebook URL must start with 'http://' or 'https://'"))


    def student_view(self, context=None):
        loader = ResourceLoader('colab_xblock')
        notebook_url = self._get_colab_url(self.notebook_url)
        context = dict(
            url=notebook_url,
            button_text=self.button_text,
            instructions=self.instructions,
        )
                        
        template = loader.render_django_template(
            'static/html/student_view.html', context=context)

        # add html and css
        frag = Fragment(template)
        frag.add_css(self.resource_string('static/css/style.css'))
        return frag

    def _get_colab_url(self, url):
        """If github.com in url, return colab'd version of that url"""
        github_base = 'https://colab.research.google.com/github/{}'
        path = urlparse.urlsplit(url)
        if path.netloc == 'github.com':
            url = github_base.format(path.path)
        return url

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MyXBlock",
             """<myxblock/>
             """),
            ("Multiple MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]

