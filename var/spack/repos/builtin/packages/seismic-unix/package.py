# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SeismicUnix(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://wiki.seismic-unix.org"
    url      = "https://nextcloud.seismic-unix.org/s/LZpzc8jMzbWG9BZ/download?path=%2F&files=cwp_su_all_44R20.tgz"

    maintainers = ['RemiLacroix-IDRIS']

    version('44R20', sha256='8ab2bb88b9eb71ddcd93c708bcfdc0c42dedcae95ca611709586cef83dcebaaf')

    variant('x11', default=True,
            description='Build x11 applications')
    variant('motif', default=False,
            description='Build M*tif applications')
    variant('fortran', default=False,
            description='Build Fortran codes')
    variant('gl', default=False,
            description='Build Mesa/OpenGL codes')
    variant('utils', default=False,
            description='Build utils')
    variant('sfio', default=False,
            description='Build the SFIO version of SEGDREAD')

    depends_on('libx11', when='+x11')
    depends_on('motif', when='+motif')
    depends_on('gl', when='+gl')

    def edit(self, spec, prefix):
        makefile_common = FileFilter('Makefile.config')

        makefile_common.filter(r'XDRFLAG\s*=.*', 'XDRFLAG =')  # Don't force endianness

        if '+x11' in spec:
            makefile_common.filter(r'IX11\s*=.*',
                                   'IX11 = {0}'.format())
            makefile_common.filter(r'LX11\s*=.*',
                                   'LX11 = {0}'.format())

        if '+motif' in self.spec:
            makefile_common.filter(r'IMOTIF\s*=.*',
                                   'IMOTIF = {0}'.format())
            makefile_common.filter(r'LMOTIF\s*=.*',
                                   'LMOTIF = {0}'.format())

        makefile_common.filter(r'CC\s*=.*', 'CC = {0}'.format(spack_cc))
        makefile_common.filter(r'FC\s*=.*', 'FC = {0}'.format(spack_fc))

        touch('LICENSE_44R18_ACCEPTED')
        touch('MAILHOME_44R18')

    @property
    def build_targets(self):
        targets = ['CWPROOT={0}'.format(ancestor(self.build_directory)), 'install']

        if '+x11' in self.spec:
            targets.append('xtinstall')
        if '+motif' in self.spec:
            targets.append('xminstall')
        if '+fortran' in self.spec:
            targets.append('finstall')
        if '+gl' in self.spec:
            targets.append('mglinstall')
        if '+utils' in self.spec:
            targets.append('utils')
        if '+sfio' in self.spec:
            targets.append('sfinstall')
    
        return targets

    def install(self, spec, prefix):
        # Seismic Unix the parent directory
        install_tree('../bin', prefix.bin)
        install_tree('../lib', prefix.lib)
        install_tree('../include', prefix.include)
