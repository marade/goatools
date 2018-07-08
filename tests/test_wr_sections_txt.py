#!/usr/bin/env python
"""Test reading GO IDs from a file."""

import os
import sys
from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag
from goatools.grouper.grprdflts import GrouperDflts
from goatools.grouper.hdrgos import HdrgosSections
from goatools.grouper.grprobj import Grouper
from goatools.grouper.read_goids import read_sections
from goatools.grouper.wr_sections import WrSectionsTxt
# from goatools.grouper.wr_sections import WrSectionsPy
# from goatools.cli.wr_sections import
from goatools.test_data.gjoneska_goea_consistent_increase import goea_results

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def test_wr_sections_all():
    """Test that all sections files generated by wr_sections have the same content."""
    f_sec_rd = "./data/gjoneska_pfenning/sections_in.txt"
    f_sec_wr = "./tmp_sections_out.txt"
    f_sec_py = "goatools/test_data/sections/tmp_test.py"
    f_sec_mod = "goatools.test_data.sections.tmp_test"
    # Read user GO IDs. Do preliminaries.
    usrgos = [getattr(nt, 'GO') for nt in goea_results]
    godag = get_godag("go-basic.obo", prt=None, loading_bar=False, optional_attrs=['relationship'])
    gosubdag = GoSubDag(usrgos, godag, relationships=True, tcntobj=None)
    grprdflt = GrouperDflts(gosubdag)
    # Create text and Python sections files
    # Read text and Python sections files
    sec_rd = _read_sections(f_sec_rd)
    # sec_wr = _read_sections(f_sec_wr)
    # sec_py = _read_sections(f_sec_py)
    # sec_mod = _read_sections(f_sec_mod)
    # _chk_sections(sec_wr, sec_py)
    # _chk_sections(sec_wr, sec_mod)

def test_wr_sections_txt():
    """Group depth-02 GO terms under their most specific depth-01 GO parent(s)."""
    # Get GOs to be grouped
    usrgos = [getattr(nt, 'GO') for nt in goea_results]
    # Read OBO files once to save time
    grprdflt = GrouperDflts()

    # ------------------------------------------------------------------
    # Print usrgos in txt (Do not use sections containing hdrgos)
    # ------------------------------------------------------------------
    # Show GO grouping hdrgos and usrgos to show how usrgos are grouped
    _wr_sections_txt("a0_hdr1.txt", usrgos, sections=None, grprdflt=grprdflt)

    # ------------------------------------------------------------------
    # Print usrgos in txt using sections containing hdrgos
    # ------------------------------------------------------------------
    sec1 = _read_sections("./data/gjoneska_pfenning/sections_in.txt")
    _wr_sections_txt("a_ec0_hdr1.txt", usrgos, sec1, grprdflt=grprdflt)

    # ------------------------------------------------------------------
    sec2a = _read_sections("goatools/test_data/sections/gjoneska_pfenning.py")
    _wr_sections_txt("b_sec0_hdr1.txt", usrgos, sec2a, grprdflt=grprdflt)

    sec2b = _read_sections("goatools.test_data.sections.gjoneska_pfenning")
    _wr_sections_txt("c_sec0_hdr1.txt", usrgos, sec2b, grprdflt=grprdflt)
    _chk_sections(sec2a, sec2b)


def _chk_sections(sec_a, sec_b):
    """Do the two sections variables contain the same data?"""
    assert len(sec_a) == len(sec_b), "LENGTH MISMATCH: {A} != {B}".format(
        A=len(sec_a), B=len(sec_b))
    for (name_a, gos_a), (name_b, gos_b) in zip(sec_a, sec_b):
        assert name_a == name_b, "NAME MISMATCH: {A} != {B}".format(A=name_a, B=name_b)
        assert gos_a == gos_b, "GO IDs MISMATCH: {A} != {B}".format(A=gos_a, B=gos_b)

def _read_sections(sec):
    """Get sections variable from file."""
    if '/' in sec:
        sec = os.path.join(REPO, sec)
    var = read_sections(sec)
    assert var, "EMPTY SECTIONS FILE({})".format(sec)
    return var

def _wr_sections_txt(fout_txt, usrgos, sections, grprdflt):
    """Given a list of usrgos and sections, write text file."""
    try:
        hdrobj = HdrgosSections(grprdflt.gosubdag, grprdflt.hdrgos_dflt, sections=sections)
        grprobj = Grouper(fout_txt, usrgos, hdrobj, grprdflt.gosubdag, go2nt=None)
        full_txt = os.path.join(REPO, fout_txt)
        WrSectionsTxt(grprobj).wr_txt_section_hdrgos(full_txt, sortby=None, prt_section=True)
        assert os.path.exists(full_txt)
    except RuntimeError as inst:
        sys.stdout.write("\n  **FATAL: {MSG}\n\n".format(MSG=str(inst)))


if __name__ == '__main__':
    test_wr_sections_all()
    # test_wr_sections_txt()