from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter


class DefaultViewSelectionView(BrowserView):

    def __call__(self):

        self.context_state = getMultiAdapter((self.context, self.request),
                                name='plone_context_state')

        templateId = self.request.form.get('templateId', False)
        if templateId:
            plone_utils = getToolByName(self.context, 'plone_utils')
            # Make sure this is a valid template
            if self.isValidTemplate(templateId):
                # Update the template
                self.context.setLayout(templateId)
                plone_utils.addPortalMessage(u'View changed.')
            else:
                plone_utils.addPortalMessage(u'Invalid view.', type="error")
                return self.index()
        if templateId or self.request.form.get('form.button.Cancel', False):
            # Redirect to view
            self.request.response.redirect('%s/view' % self.context_state.object_url())

        return self.index()

    def isValidTemplate(self, templateId):
        return templateId in [a[0] for a in self.vocab]

    @property
    def vocab(self):
        return self.context.getAvailableLayouts()

    @property
    def selectedLayout(self):
        if not self.context_state.is_default_page():
            return self.context.getLayout()
        else:
            return ""

    @property
    def action_url(self):
        return "%s/select_default_view" % self.context_state.object_url()
