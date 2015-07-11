# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.Expression import createExprContext
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.memoize.request import memoize_diy_request
from plone.protect.authenticator import createToken
from urllib import quote_plus
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.i18n import translate
from zope.publisher.browser import BrowserView


@memoize_diy_request(arg=0)
def _allowedTypes(request, context):
    return context.allowedContentTypes()


class FolderFactoriesView(BrowserView):
    """The folder_factories view - show addable types
    """

    def __call__(self):
        if 'form.button.Add' in self.request.form:
            return self.redirect_to_add_form()
        else:
            return self.index()

    def redirect_to_add_form(self):
        type_id = self.request.form.get('id')
        folder_path = self.request.form.get('folder')
        if folder_path is None:
            folder = self.add_context()
        else:
            portal = self.portal_state.portal()
            if folder_path == '/':
                folder = portal
            else:
                folder = portal.restrictedTraverse(folder_path.lstrip('/'))

        for type_info in self.addable_types(addContext=folder):
            if type_info['id'] == type_id:
                self.request.response.redirect(type_info['action'])
                return ''
        # XXX This should NOT happen. validation, etc should hapeen and users
        # should not see this
        raise Exception("Not allowed to add type to this container")

    @property
    @memoize
    def portal_state(self):
        return getMultiAdapter((self.context, self.request),
                               name='plone_portal_state')

    @property
    @memoize
    def context_state(self):
        return getMultiAdapter((self.context, self.request),
                               name='plone_context_state')
    @property
    def current_folder(self):
        if self.context_state.is_portal_root():
            return '/'
        portal = self.portal_state.portal()
        site_path = '/'.join(portal.getPhysicalPath())
        context_path = '/'.join(self.context_state.folder().getPhysicalPath())
        path = context_path[len(site_path):]
        return path

    def can_constrain_types(self):
        aspect = ISelectableConstrainTypes(self.add_context(), None)
        return aspect.canSetConstrainTypes() if aspect else False

    @memoize
    def add_context(self):
        context = self.context
        context = aq_inner(context)
        try:
            published = self.request.PUBLISHED
        except AttributeError:
            published = context
        if self.context_state.is_structural_folder():
            if self.context_state.is_default_page():
                is_folder_contents_view = \
                    IFolderContentsView.providedBy(published)
                if is_folder_contents_view or self == published:
                    # on the folder_contents view and factories view,
                    # show the actual context object's addable types
                    return context
                else:
                    return aq_parent(context)
            else:
                return context
        else:
            return aq_parent(context)

    # NOTE: This is also used by plone.app.contentmenu.menu.FactoriesMenu.
    # The return value is somewhat dictated by the menu infrastructure, so
    # be careful if you change it
    def addable_types(self, include=None, addContext=None):
        """Return menu item entries in a TAL-friendly form.

        Pass a list of type ids to 'include' to explicitly allow a list of
        types.
        """

        context = aq_inner(self.context)
        request = self.request

        results = []

        idnormalizer = queryUtility(IIDNormalizer)

        if addContext is None:
            addContext = self.add_context()
        baseUrl = addContext.absolute_url()
        token = createToken()

        allowedTypes = _allowedTypes(request, addContext)

        types_tool = getToolByName(context, 'portal_types')

        # Note: we don't check 'allowed' or 'available' here, because these are
        # slow. We assume the 'allowedTypes' list has already performed the
        # necessary calculations
        actions = types_tool.listActionInfos(
            object=addContext,
            check_permissions=False,
            check_condition=False,
            category='folder/add',
        )
        addActionsById = dict([(a['id'], a) for a in actions])

        expr_context = createExprContext(
            aq_parent(addContext), self.portal_state.portal(), addContext)
        for t in allowedTypes:
            typeId = t.getId()
            if include is None or typeId in include:
                cssId = idnormalizer.normalize(typeId)
                cssClass = 'contenttype-%s' % cssId

                url = None
                addAction = addActionsById.get(typeId, None)
                if addAction is not None:
                    url = addAction['url']

                if not url:
                    url = '%s/createObject?type_name=%s&_authenticator=%s' % (
                        baseUrl, quote_plus(typeId), token)

                icon = t.getIconExprObject()
                if icon:
                    icon = icon(expr_context)

                results.append({
                    'id': typeId,
                    'title': t.Title(),
                    'description': t.Description(),
                    'action': url,
                    'selected': False,
                    'icon': icon,
                    'extra': {
                        'id': cssId,
                        'separator': None,
                        'class': cssClass},
                    'submenu': None,
                })

        # Sort the addable content types based on their translated title
        results = [(translate(ctype['title'], context=request), ctype)
                   for ctype in results]
        results.sort()
        results = [ctype[-1] for ctype in results]

        return results
