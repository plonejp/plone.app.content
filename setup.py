from setuptools import setup, find_packages

version = '2.3.0.dev0'

setup(name='plone.app.content',
      version=version,
      description="Content Views for Plone",
      long_description='\n\n'.join([
          open("README.rst").read(),
          open("CHANGES.rst").read(),
      ]),
      classifiers=[
          "Framework :: Plone",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
      ],
      keywords='plone content views viewlet',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.content',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'plone.app.testing',
              'plone.app.contenttypes',
              'Products.PloneTestCase',
          ]
      ),
      install_requires=[
          'setuptools',
          'plone.memoize',
          'plone.batching',
          'plone.i18n',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.component',
          'zope.container',
          'zope.event',
          'zope.lifecycleevent',
          'zope.publisher',
          'zope.schema',
          'zope.viewlet',
          'Acquisition',
          'Products.CMFPlone',
          'Products.CMFCore>=2.2.0dev',
          'Products.CMFDefault',
          'Products.CMFDynamicViewFTI',  # required for cmf.ModifyViewTemplate
          'Zope2',
      ],
      )
