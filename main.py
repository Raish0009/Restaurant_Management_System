import os 
import sys
sys.path.append(os.getcwd())

from Src.Authentication.Manage import Manage

Management=Manage()
Management.management()
