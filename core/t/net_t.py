#!/usr/bin/python
# encoding: utf-8
""" The net test class """

from core.net import Net
from core.net import NetPoint
from core.net import ConnectedComponent
from core.shape import Point
import unittest


class NetTests(unittest.TestCase):
    """ The tests of the core module net feature """

    def setUp(self):
        """ Setup the test case. """
        self.net = Net('001')

    def tearDown(self):
        """ Teardown the test case. """
        del self.net

    def test_create_new_net(self):
        """ Test the creation of a new empty net. """
        assert self.net.net_id == '001'

    def test_bounds_simple(self):
        '''Make sure bounds() uses all the included NetPoints'''
        for (x, y) in ((1,3), (3,2), (4,3), (3,5)):
            pt = NetPoint(str((x,y)), x, y)
            self.net.add_point(pt)
            # NetPoints don't actually need to be connected to affect bounds()

        tl, br = self.net.bounds()
        self.assertEqual(tl.x, 1)
        self.assertEqual(tl.y, 2)
        self.assertEqual(br.x, 4)
        self.assertEqual(br.y, 5)

class NetPointTests(unittest.TestCase):
    """ The tests of the core module net point feature """

    def setUp(self):
        """ Setup the test case. """
        pass

    def tearDown(self):
        """ Teardown the test case. """
        pass

    def test_create_new_net_point(self):
        """ Test the creation of a new empty net point. """
        point = NetPoint('001', 0, 1)
        assert point.point_id == '001'


class ConnectedComponentTests(unittest.TestCase):
    """ The tests of the core module connected component feature """

    def setUp(self):
        """ Setup the test case. """
        pass

    def tearDown(self):
        """ Teardown the test case. """
        pass

    def test_create_new_component(self):
        """ Test the creation of a new empty connected component. """
        comp = ConnectedComponent('001', '002')
        assert comp.instance_id == '001'