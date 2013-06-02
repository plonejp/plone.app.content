import unittest2 as unittest
from plone.app.content.testing import PLONE_APP_CONTENT_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login
#import transaction
#from plone.app.content.namechooser import ATTEMPTS
#from zope.container.interfaces import INameChooser


class FileUploadCreationTest(unittest.TestCase):
    layer = PLONE_APP_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_dx_file_created(self):
        self.fail()

    def test_at_file_created(self):
        self.fail()

def test_suite():
    return unittest.makeSuite(FileUploadCreationTest)
