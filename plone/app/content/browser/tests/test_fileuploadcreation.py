import unittest2 as unittest
from plone.app.content.browser.interfaces import IATCTFileFactory
from plone.app.content.browser.interfaces import IDXFileFactory
from Products.ATContentTypes.interfaces import IATFile
from plone.dexterity.interfaces import IDexterityFTI

from Products.PloneTestCase import PloneTestCase as ptc

ptc.installPackage('plone.app.dexterity')
ptc.setupPloneSite(extension_profiles=('plone.app.dexterity:default',))

class DXFileUploadCreationTest(ptc.PloneTestCase):

    def test_dxfile_factory(self):
        import StringIO
        data = StringIO.StringIO()
        data.write("Hello, world")
        data.filename = 'file.txt'

        factory = IDXFileFactory(self.portal)
        new_object = factory('dx_file', 'File', data)
        self.failUnless(IDexterityFTI.providedBy(new_object))
        data.close()


class ATCTFileUploadCreationTest(ptc.PloneTestCase):

    def test_atctfile_factory(self):
        factory = IATCTFileFactory(self.portal)
        new_object = factory('at_file', 'File', None)
        self.failUnless(IATFile.providedBy(new_object))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
