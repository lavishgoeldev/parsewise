"""Direct-download URLs for clearly public-domain US government PDFs.

Used for Step 1.B parser eval on real-world docs. Each entry points to a
direct PDF URL (not a landing page), which lets us automate the download
while still preserving Wayback archival + sha256 verification.

License: every entry here is a US federal government work, which is in the
public domain by 17 USC §105. Verified human-confirmed: 2026-06-09 (initial 6)
and 2026-06-10 (expanded set for parser-paper n>=30).

The categories below are chosen for *layout diversity* rather than strictly
"personal documents":
  - tax           : IRS forms (short, field-heavy) + IRS publications (long, multi-column)
  - immigration   : USCIS forms (long, mixed form + instruction prose)
  - medical       : CDC MMWR (multi-column scientific publications with tables/figures)
  - housing       : HUD model leases + supporting forms (lease-style structured text)
  - legal         : SCOTUS slip opinions (prose-dense, long, single-column)
  - administrative: SSA / GSA / federal forms with varied layouts
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RealPDF:
    id: str
    category: str
    title: str
    url: str
    publisher: str


REAL_PDFS: list[RealPDF] = [
    # ---------------------------------------------------------------- TAX (8)
    RealPDF(
        id="T001",
        category="tax",
        title="IRS Form 1040 (U.S. Individual Income Tax Return)",
        url="https://www.irs.gov/pub/irs-pdf/f1040.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    RealPDF(
        id="T002",
        category="tax",
        title="IRS Schedule C (Profit or Loss from Business)",
        url="https://www.irs.gov/pub/irs-pdf/f1040sc.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    RealPDF(
        id="T003",
        category="tax",
        title="IRS Publication 17 (Your Federal Income Tax)",
        url="https://www.irs.gov/pub/irs-pdf/p17.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    RealPDF(
        id="T004",
        category="tax",
        title="IRS Schedule A (Itemized Deductions)",
        url="https://www.irs.gov/pub/irs-pdf/f1040sa.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    RealPDF(
        id="T005",
        category="tax",
        title="IRS Form W-9 (Request for Taxpayer Identification Number)",
        url="https://www.irs.gov/pub/irs-pdf/fw9.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    RealPDF(
        id="T006",
        category="tax",
        title="IRS Form W-4 (Employee's Withholding Certificate)",
        url="https://www.irs.gov/pub/irs-pdf/fw4.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    RealPDF(
        id="T007",
        category="tax",
        title="IRS Publication 463 (Travel, Gift, and Car Expenses)",
        url="https://www.irs.gov/pub/irs-pdf/p463.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    RealPDF(
        id="T008",
        category="tax",
        title="IRS Form 1040 Instructions",
        url="https://www.irs.gov/pub/irs-pdf/i1040gi.pdf",
        publisher="U.S. Internal Revenue Service",
    ),
    # --------------------------------------------------------- IMMIGRATION (8)
    RealPDF(
        id="IM001",
        category="immigration",
        title="USCIS Form I-130 (Petition for Alien Relative)",
        url="https://www.uscis.gov/sites/default/files/document/forms/i-130.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    RealPDF(
        id="IM002",
        category="immigration",
        title="USCIS Form N-400 (Application for Naturalization)",
        url="https://www.uscis.gov/sites/default/files/document/forms/n-400.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    RealPDF(
        id="IM003",
        category="immigration",
        title="USCIS Form I-485 (Application to Register Permanent Residence)",
        url="https://www.uscis.gov/sites/default/files/document/forms/i-485.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    RealPDF(
        id="IM004",
        category="immigration",
        title="USCIS Form I-765 (Application for Employment Authorization)",
        url="https://www.uscis.gov/sites/default/files/document/forms/i-765.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    RealPDF(
        id="IM005",
        category="immigration",
        title="USCIS Form I-864 (Affidavit of Support)",
        url="https://www.uscis.gov/sites/default/files/document/forms/i-864.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    RealPDF(
        id="IM006",
        category="immigration",
        title="USCIS Form I-90 (Application to Replace Permanent Resident Card)",
        url="https://www.uscis.gov/sites/default/files/document/forms/i-90.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    RealPDF(
        id="IM007",
        category="immigration",
        title="USCIS Form G-28 (Notice of Entry of Appearance)",
        url="https://www.uscis.gov/sites/default/files/document/forms/g-28.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    RealPDF(
        id="IM008",
        category="immigration",
        title="USCIS Form I-485 Instructions",
        url="https://www.uscis.gov/sites/default/files/document/forms/i-485instr.pdf",
        publisher="U.S. Citizenship and Immigration Services",
    ),
    # -------------------------------------------------------------- MEDICAL (6)
    RealPDF(
        id="M001",
        category="medical",
        title="CDC MMWR Vol 73 No 1 (Jan 11, 2024)",
        url="https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7301-H.pdf",
        publisher="U.S. Centers for Disease Control and Prevention",
    ),
    RealPDF(
        id="M002",
        category="medical",
        title="CDC MMWR Vol 73 No 9 (Mar 7, 2024)",
        url="https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7309-H.pdf",
        publisher="U.S. Centers for Disease Control and Prevention",
    ),
    RealPDF(
        id="M003",
        category="medical",
        title="CDC MMWR Vol 73 No 15 (Apr 18, 2024)",
        url="https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7315-H.pdf",
        publisher="U.S. Centers for Disease Control and Prevention",
    ),
    RealPDF(
        id="M004",
        category="medical",
        title="CDC MMWR Vol 73 No 16 (Apr 25, 2024)",
        url="https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7316-H.pdf",
        publisher="U.S. Centers for Disease Control and Prevention",
    ),
    RealPDF(
        id="M005",
        category="medical",
        title="CDC MMWR Vol 73 No 41 (Oct 17, 2024)",
        url="https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7341-H.pdf",
        publisher="U.S. Centers for Disease Control and Prevention",
    ),
    RealPDF(
        id="M006",
        category="medical",
        title="CDC MMWR Vol 73 No 50 (Dec 19, 2024)",
        url="https://www.cdc.gov/mmwr/volumes/73/wr/pdfs/mm7350-H.pdf",
        publisher="U.S. Centers for Disease Control and Prevention",
    ),
    # -------------------------------------------------------------- HOUSING (4)
    RealPDF(
        id="H001",
        category="housing",
        title="HUD Model Lease for Subsidized Programs (HUD-90105a)",
        url="https://www.hud.gov/sites/dfiles/OCHCO/documents/90105a.pdf",
        publisher="U.S. Department of Housing and Urban Development",
    ),
    RealPDF(
        id="H002",
        category="housing",
        title="HUD Model Lease — Section 202 (HUD-90105b)",
        url="https://www.hud.gov/sites/dfiles/OCHCO/documents/90105b.pdf",
        publisher="U.S. Department of Housing and Urban Development",
    ),
    RealPDF(
        id="H003",
        category="housing",
        title="HUD Form 52646",
        url="https://www.hud.gov/sites/dfiles/OCHCO/documents/52646.pdf",
        publisher="U.S. Department of Housing and Urban Development",
    ),
    RealPDF(
        id="H004",
        category="housing",
        title="HUD Form 52641-A (HAP Contract)",
        url="https://www.hud.gov/sites/dfiles/OCHCO/documents/52641A.pdf",
        publisher="U.S. Department of Housing and Urban Development",
    ),
    # ---------------------------------------------------------------- LEGAL (4)
    # SCOTUS slip opinions are public-domain US-govt works; long prose, single-column.
    RealPDF(
        id="L001",
        category="legal",
        title="SCOTUS Slip Opinion 23-477 (United States v. Skrmetti)",
        url="https://www.supremecourt.gov/opinions/24pdf/23-477_2cp3.pdf",
        publisher="Supreme Court of the United States",
    ),
    RealPDF(
        id="L002",
        category="legal",
        title="SCOTUS Slip Opinion 22-7466",
        url="https://www.supremecourt.gov/opinions/24pdf/22-7466_5h25.pdf",
        publisher="Supreme Court of the United States",
    ),
    RealPDF(
        id="L003",
        category="legal",
        title="SCOTUS Slip Opinion 23-719",
        url="https://www.supremecourt.gov/opinions/23pdf/23-719_19m2.pdf",
        publisher="Supreme Court of the United States",
    ),
    RealPDF(
        id="L004",
        category="legal",
        title="SCOTUS Slip Opinion 23-939",
        url="https://www.supremecourt.gov/opinions/23pdf/23-939_e2pg.pdf",
        publisher="Supreme Court of the United States",
    ),
]
