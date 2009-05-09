##
## Biskit, a toolkit for the manipulation of macromolecular structures
## Copyright (C) 2004-2009 Raik Gruenberg & Johan Leckner
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You find a copy of the GNU General Public License in the file
## license.txt along with this program; if not, write to the Free
## Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
##
##
## $Revision$
## last $Author$
## last $Date$

"""
PDBModel with attached Xplor topology (PSF).
"""

## PCRModel:
## collect and manage information about a ligand or receptor conformation
## generated by (PCR)MD

import tools as t
from PDBModel import PDBModel
from LocalPath import LocalPath


class PCRModel( PDBModel ):
    """
    PDBModel with attached Xplor topology (PSF).
    Creates more problems than it solves...
    """

    def __init__(self, fPsf=None, source=None, pdbCode=None, **params):
        """
        @param fPsf: file name of psf
        @type  fPsf: str
        @param source: file name of pdb OR PDBModel instance
        @type  source: str | PDBModel
        @param pdbCode: if None, first 4 letters of filename will be used
        @type  pdbCode: str
        """
        PDBModel.__init__( self, source=source, pdbCode=pdbCode, **params )

        if fPsf and not isinstance( fPsf, LocalPath):
            fPsf = LocalPath( fPsf )

        ## in case given fPDB is already a PCRModel, keep psfFileName
        self.psfFileName = fPsf or getattr( source, 'psfFileName', None)

        ## version as of creation of this object
        self.initVersion = self.version()


    def version( self ):
        return PDBModel.version(self) + '; PCRModel $Revision$'


    def getPsfFile(self):
        """
        @return: file name
        @rtype: str
        """
        return self.psfFileName


    def take(self, i, rindex=None, cindex=None ):
        r = PDBModel.take( self, i, rindex=rindex, cindex=cindex )
        r.psfFileName = self.psfFileName
        r.initVersion = self.initVersion
        return r


    def concat(self, *models ):
        r = PDBModel.concat( self, *models )
        r.psfFileName = self.psfFileName
        r.initVersion = self.initVersion
        return r


#############
##  TESTING        
#############
import Biskit.test as BT

class Test(BT.BiskitTest):
    """Test class """

    def test_PCRModel( self ):
        """PCRModel test"""
        ## Loading PDB...
        self.m_com = PCRModel( t.testRoot() + "/com/1BGS.psf",
                          t.testRoot() + "/com/1BGS.pdb" )

        self.m_rec = PCRModel( t.testRoot() + "/rec/1A2P.psf",
                          t.testRoot() + "/rec/1A2P.pdb" )

        ## remove waters
        self.m_com = self.m_com.compress( self.m_com.maskProtein() )
        self.m_rec = self.m_rec.compress( self.m_rec.maskProtein() )

        ## fit the complex structure to the free receptor
        m_com_fit = self.m_com.magicFit( self.m_rec )

        ## calculate the rmsd between the original complex and the
        ## one fitted to the free receptor
        rms = m_com_fit.rms(self.m_com, fit=0)
        
        if self.local:
            print 'Rmsd between the two complex structures: %.2f Angstrom'%rms

        self.assertAlmostEqual(rms, 58.7844130314, 4)

    
if __name__ == '__main__':

    BT.localTest()






