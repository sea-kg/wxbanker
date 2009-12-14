#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    https://launchpad.net/wxbanker
#    dbupgradetests.py: Copyright 2007-2009 Mike Rooney <mrooney@ubuntu.com>
#
#    This file is part of wxBanker.
#
#    wxBanker is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    wxBanker is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with wxBanker.  If not, see <http://www.gnu.org/licenses/>.

from wxbanker.tests import testbase
from wxbanker.controller import Controller
import unittest, shutil, os

class DBUpgradeTest(unittest.TestCase):
    def doBaseTest(self, ver):
        origpath = testbase.fixturefile("bank-%s.db"%ver)
        dbpath = os.path.join(os.path.split(origpath)[0], "temp.db")
        shutil.copyfile(origpath, dbpath)
        
        c = Controller(path=dbpath)
        model = c.Model
        accounts = model.Accounts
        self.assertEqual([a.Name for a in accounts], ["My Checking", "Another"])
        self.assertEqual(accounts[0].Balance, 25)
        self.assertEqual(accounts[1].Balance, -123.45)
        
        # Make sure it is persisted!
        model2 = model.Store.GetModel(useCached=False)
        accounts = model2.Accounts
        self.assertEqual([a.Name for a in accounts], ["My Checking", "Another"])
        self.assertEqual(accounts[0].Balance, 25)
        self.assertEqual(accounts[1].Balance, -123.45)
        
        return c
        
    def testUpgradeFrom04(self):
        c = self.doBaseTest("0.4")
        
    def testUpgradeFrom05(self):
        c = self.doBaseTest("0.5")
        
    def tearDown(self):
        tmpPath = os.path.join(testbase.fixturefile('.'), "temp.db")
        if os.path.exists(tmpPath):
            os.remove(tmpPath)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
