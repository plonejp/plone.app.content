import unittest2 as unittest
from plone.app.content.browser.interfaces import IATCTFileFactory
from plone.app.content.browser.interfaces import IDXFileFactory
from plone.app.content.browser.factories import ATCTFileFactory
from plone.app.content.browser.factories import DXFileFactory
from Products.CMFCore.interfaces._content import IFolderish
from Products.ATContentTypes.interfaces import IATFile
from Products.PloneTestCase import PloneTestCase as ptc

ptc.setupPloneSite()


class FileUploadCreationTest(ptc.PloneTestCase):

    def test_atctfile_factory(self):
        factory = IATCTFileFactory(self.portal)
        new_object = factory('at_file', 'File', None)
        self.failUnless(IATFile.providedBy(new_object))

    def test_dxfile_factory(self):
        """ force dexterity to be installed """
        pass
        #factory = IDXFileFactory(self.portal)
        #new_object = factory('dx_file', 'File', None)
        #self.failUnless(IATFile.providedBy(new_object))

def test_suite():
    return unittest.makeSuite(FileUploadCreationTest)
