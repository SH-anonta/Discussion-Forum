How functional tests (FT) are organized for this app (forum)

Each FT resembles a user story, the tests try to do something using selenium and test if the operations succeed/fail as expected
FTs are separated into different files (file names should be convenient enough)

#Important:

1. The BaseTestCase class:
    located in the base_testcase.py file, this class should be the base if all FT for this app
    All common testing methods go here ie. goToHomePage,

    * attributes of this class:
        self.browser: selenium web driver
        self.<PageName>_page: page object class instance for <PageName> template

    * methods:
        self.goTo<PageName>(): does a get request using url to a <PageName>
        self.assert<PageName>Loaded(): asserts whether the browser is currently at <pageName

    * Methods not to  overwrite in this class:
    setUp, TearDown


    * Methods to overwrite in this class
    loadData: this gets called by setUp after all basic data have been loaded

2. page_objects file:
    contains page object classes,
    Each class knows how to interact with a certain template
    class names are (almost) same as the template names

    These classes take a selenium web browser with the constructor
    and use the driver to do operations on the page

    page object classes are initialized in the BaseTestCase classes setUp method
    these objects are assigned to the test case attributes
    ie. the self.homepage attribute is an object that knows how to interact with the homepage template