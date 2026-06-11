# Appendix B — Specimen pages

Same page, five parsers. We show the first ~30 lines of extracted text
per parser to let the reader see *qualitatively* what the cluster CER
numbers in §6.2 are measuring. Full extracts are in `results/specimen_pages/`.

## B.1 M005 — CDC MMWR Vol 73 No 41 — multi-column publication (page 1)

### pymupdf

```
Morbidity and Mortality Weekly Report
U.S. Centers for Disease Control and Prevention
Weekly / Vol. 73 / No. 41	
October 17, 2024
INSIDE
917	 Tobacco Product Use Among Middle and High 
School Students — National Youth Tobacco Survey, 
United States, 2024
925	 Coverage with Selected Vaccines and Exemption 
Rates Among Children in Kindergarten — United 
States, 2023–24 School Year
933	 Notes from the Field: Enhanced Surveillance for 
Raccoon Rabies Virus Variant and Vaccination of 
Wildlife for Management — Omaha, Nebraska, 
October 2023–July 2024 
936	 QuickStats
Continuing Education examination available at 
https://www.cdc.gov/mmwr/mmwr_continuingEducation.html
Update on Vaccine-Derived Poliovirus Outbreaks — 
Worldwide, January 2023–June 2024
Apophia Namageyo-Funa, PhD1; Sharon A. Greene, PhD1; Elizabeth Henderson2; Mohamed A. Traoré3; Shahzad Shaukat, PhD3; John Paul Bigouette, PhD1; 
Jaume Jorba, PhD2; Eric Wiesen, DrPH1; Omotayo Bolu, PhD1; Ousmane M. Diop, PhD3; Cara C. Burns, PhD2; Steven G.F. Wassilak, MD1
Abstract
Circulating vaccine-derived polioviruses (cVDPVs) can 
emerge and lead to outbreaks of paralytic polio as well as 
asymptomatic transmission in communities with a high percent­
age of undervaccinated children. Using data from the World 
Health Organization Polio Information System and Global 
Polio Laboratory Network, this report describes global polio 
outbreaks due to cVDPVs during January 2023–June 2024 
... [truncated, 1600 chars total]
```

### pypdf

```
Morbidity and Mortality Weekly Report
U.S. Centers for Disease Control and Prevention
Weekly / Vol. 73 / No. 41 Oct ober 17, 2024
INSIDE
917 Tobacco Product Use Among Middle and High 
School Students — National Youth Tobacco Survey, 
United States, 2024
925 Coverage with Selected Vaccines and Exemption 
Rates Among Children in Kindergarten — United 
States, 2023–24 School Year
933 Notes from the Field: Enhanced Surveillance for 
Raccoon Rabies Virus Variant and Vaccination of 
Wildlife for Management — Omaha, Nebraska, 
October 2023–July 2024 
936 QuickStats
Continuing Education examination available at  
https://www.cdc.gov/mmwr/mmwr_continuingEducation.html
Update on Vaccine-Derived Poliovirus Outbreaks —  
Worldwide, January 2023–June 2024
Apophia Namageyo-Funa, PhD1; Sharon A. Greene, PhD1; Elizabeth Henderson2; Mohamed A. T raoré3; Shahzad Shaukat, PhD3; John Paul Bigouette, PhD1; 
Jaume Jorba, PhD2; Eric Wiesen, DrPH1; Omotayo Bolu, PhD1; Ousmane M. Diop, PhD3; Cara C. Burns, PhD2; Steven G.F . Wassilak, MD1
Abstract
Circulating vaccine-derived polioviruses (cVDPVs) can 
emerge and lead to outbreaks of paralytic polio as well as 
asymptomatic transmission in communities with a high percent-
age of undervaccinated children. Using data from the World 
Health Organization Polio Information System and Global 
Polio Laboratory Network, this report describes global polio 
outbreaks due to cVDPVs during January 2023–June 2024 
and updates previous reports. During the reporting period, 
... [truncated, 1600 chars total]
```

### pdfplumber_tuned

```
Morbidity and Mortality Weekly Report
U.S. Centers for Disease Control and Prevention
Weekly / Vol. 73 / No. 41 October 17, 2024
INSIDE
917 Tobacco Product Use Among Middle and High
School Students — National Youth Tobacco Survey,
United States, 2024
925 Coverage with Selected Vaccines and Exemption
Rates Among Children in Kindergarten — United
States, 2023–24 School Year
933 Notes from the Field: Enhanced Surveillance for
Raccoon Rabies Virus Variant and Vaccination of
Wildlife for Management — Omaha, Nebraska,
October 2023–July 2024
936 QuickStats
Continuing Education examination available at
https://www.cdc.gov/mmwr/mmwr_continuingEducation.html
Update on Vaccine-Derived Poliovirus Outbreaks —
Worldwide, January 2023–June 2024
Apophia Namageyo-Funa, PhD1; Sharon A. Greene, PhD1; Elizabeth Henderson2; Mohamed A. Traoré3; Shahzad Shaukat, PhD3; John Paul Bigouette, PhD1;
Jaume Jorba, PhD2; Eric Wiesen, DrPH1; Omotayo Bolu, PhD1; Ousmane M. Diop, PhD3; Cara C. Burns, PhD2; Steven G.F. Wassilak, MD1
Abstract
Circulating vaccine-derived polioviruses (cVDPVs) can
emerge and lead to outbreaks of paralytic polio as well as
asymptomatic transmission in communities with a high percent-
age of undervaccinated children. Using data from the World
Health Organization Polio Information System and Global
Polio Laboratory Network, this report describes global polio
outbreaks due to cVDPVs during January 2023–June 2024
and updates previous reports. During the reporting period,
... [truncated, 1600 chars total]
```

### pdfminer

```
U.S. Centers for Disease Control and Prevention

Weekly / Vol. 73 / No. 41 

Morbidity and Mortality Weekly Report
October 17, 2024

Update on Vaccine-Derived Poliovirus Outbreaks —  
Worldwide, January 2023–June 2024

Apophia Namageyo-Funa, PhD1; Sharon A. Greene, PhD1; Elizabeth Henderson2; Mohamed A. Traoré3; Shahzad Shaukat, PhD3; John Paul Bigouette, PhD1; 
Jaume Jorba, PhD2; Eric Wiesen, DrPH1; Omotayo Bolu, PhD1; Ousmane M. Diop, PhD3; Cara C. Burns, PhD2; Steven G.F. Wassilak, MD1

Abstract
Circulating  vaccine-derived  polioviruses  (cVDPVs)  can 
emerge  and  lead  to  outbreaks  of  paralytic  polio  as  well  as 
asymptomatic transmission in communities with a high percent-
age of undervaccinated children. Using data from the World 
Health  Organization  Polio  Information  System  and  Global 
Polio  Laboratory  Network,  this  report  describes  global  polio 
outbreaks  due  to  cVDPVs  during  January  2023–June  2024 
and  updates  previous  reports.  During  the  reporting  period, 
74 cVDPV outbreaks were detected in 39 countries or areas 
(countries), predominantly in Africa. Among these 74 cVDPV 
outbreaks, 47 (64%) were new outbreaks, detected in 30 (77%) 
of the 39 countries. Three countries reported cVDPV type 1 
(cVDPV1) outbreaks and 38 countries reported cVDPV type 
2 (cVDPV2) outbreaks; two of these countries reported cocir-
culating  cVDPV1  and  cVDPV2.  In  the  38  countries  with 
cVDPV2  transmission,  70  distinct  outbreaks  were  reported. 
... [truncated, 1600 chars total]
```

### pdfplumber

```
U.S. Centers for Disease Control and Prevention
Morbidity and Mortality Weekly Report
Weekly / Vol. 73 / No. 41 October 17, 2024
Update on Vaccine-Derived Poliovirus Outbreaks —
Worldwide, January 2023–June 2024
Apophia Namageyo-Funa, PhD1; Sharon A. Greene, PhD1; Elizabeth Henderson2; Mohamed A. Traoré3; Shahzad Shaukat, PhD3; John Paul Bigouette, PhD1;
Jaume Jorba, PhD2; Eric Wiesen, DrPH1; Omotayo Bolu, PhD1; Ousmane M. Diop, PhD3; Cara C. Burns, PhD2; Steven G.F. Wassilak, MD1
Abstract vaccine-derived poliovirus (cVDPVs)* outbreaks occur when
Circulating vaccine-derived polioviruses (cVDPVs) can OPV-related strains undergo prolonged circulation in com-
emerge and lead to outbreaks of paralytic polio as well as munities with very low immunity against polioviruses, and the
asymptomatic transmission in communities with a high percent- genetically reverted virus has regained neurovirulence (vaccine-
age of undervaccinated children. Using data from the World derived poliovirus [VDPV] emergence) (2,3). After declaration
Health Organization Polio Information System and Global of wild poliovirus type 2 eradication in 2015, and in an effort
Polio Laboratory Network, this report describes global polio to lower the risk for cVDPV type 2 (cVDPV2) outbreaks,
outbreaks due to cVDPVs during January 2023–June 2024 immunization programs in countries using OPV switched
and updates previous reports. During the reporting period, from using trivalent OPV (tOPV) (containing types 1, 2, and
74 cVDPV outbreaks were detected in 39 countries or areas 3 Sabin strains) in routine and supplementary
```

---

## B.2 L001 — SCOTUS Slip Opinion 23-477 — single-column prose (page 1)

### pymupdf

```
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
... [truncated, 1600 chars total]
```

### pypdf

```
  
 
 
 
 
    
       
 
  
 
  
 
  
 
 
 
 
 
 
 
    
  
  
 
 
   
 
 
  
 
... [truncated, 1600 chars total]
```

### pdfplumber_tuned

```
1 (Slip Opinion) OCTOBER TERM, 2024
Syllabus
NOTE: Where it is feasible, a syllabus (headnote) will be released, as is
being done in connection with this case, at the time the opinion is issued.
The syllabus constitutes no part of the opinion of the Court but has been
prepared by the Reporter of Decisions for the convenience of the reader.
See United States v. Detroit Timber & Lumber Co., 200 U. S. 321, 337.
SUPREME COURT OF THE UNITED STATES
Syllabus
UNITED STATES v. SKRMETTI, ATTORNEY GENERAL
AND REPORTER FOR TENNESSEE, ET AL.
CERTIORARI TO THE UNITED STATES COURT OF APPEALS FOR
THE SIXTH CIRCUIT
No. 23–477. Argued December 4, 2024—Decided June 18, 2025
In 2023, Tennessee joined the growing number of States restricting sex
transition treatments for minors by enacting the Prohibition on Medi-
cal Procedures Performed on Minors Related to Sexual Identity, Sen-
ate Bill 1 (SB1). SB1 prohibits healthcare providers from prescribing,
administering, or dispensing puberty blockers or hormones to any mi-
nor for the purpose of (1) enabling the minor to identify with, or live
as, a purported identity inconsistent with the minor’s biological sex, or
(2) treating purported discomfort or distress from a discordance be-
tween the minor’s biological sex and asserted identity. At the same
time, SB1 permits a healthcare provider to administer puberty block-
ers or hormones to treat a minor’s congenital defect, precocious pu-
berty, disease, or physical injury.
Three transgender minors, their parents, and a doctor challenged
SB1 under the Equal Protection Clause of the Fourteenth Amendment
```

### pdfminer

```
(Slip Opinion) 

OCTOBER  TERM,  2024 

1 

Syllabus 

NOTE:  Where  it  is  feasible,  a  syllabus  (headnote)  will  be  released,  as  is 
being  done  in  connection  with  this  case,  at  the  time  the  opinion  is  issued. 
The  syllabus  constitutes  no  part  of  the  opinion  of  the  Court  but  has  been 
prepared  by  the  Reporter  of  Decisions  for  the  convenience  of  the  reader. 
See United States v. Detroit Timber & Lumber Co., 200 U. S. 321, 337. 

SUPREME COURT OF THE UNITED STATES 

Syllabus 

UNITED STATES v. SKRMETTI, ATTORNEY GENERAL 
AND REPORTER FOR TENNESSEE, ET AL. 

CERTIORARI TO THE UNITED STATES COURT OF APPEALS FOR 
THE SIXTH CIRCUIT 

No. 23–477.  Argued December 4, 2024—Decided June 18, 2025 

In 2023, Tennessee joined the growing number of States restricting sex 
transition treatments for minors by enacting the Prohibition on Medi-
cal Procedures Performed on Minors Related to Sexual Identity, Sen-
ate Bill 1 (SB1).  SB1 prohibits healthcare providers from prescribing, 
... [truncated, 1600 chars total]
```

### pdfplumber

```
(Slip Opinion) OCTOBER TERM, 2024 1
Syllabus
NOTE: Where it is feasible, a syllabus (headnote) will be released, as is
being done in connection with this case, at the time the opinion is issued.
The syllabus constitutes no part of the opinion of the Court but has been
prepared by the Reporter of Decisions for the convenience of the reader.
See United States v. Detroit Timber & Lumber Co., 200 U. S. 321, 337.
SUPREME COURT OF THE UNITED STATES
Syllabus
UNITED STATES v. SKRMETTI, ATTORNEY GENERAL
AND REPORTER FOR TENNESSEE, ET AL.
CERTIORARI TO THE UNITED STATES COURT OF APPEALS FOR
THE SIXTH CIRCUIT
No. 23–477. Argued December 4, 2024—Decided June 18, 2025
In 2023, Tennessee joined the growing number of States restricting sex
transition treatments for minors by enacting the Prohibition on Medi-
cal Procedures Performed on Minors Related to Sexual Identity, Sen-
ate Bill 1 (SB1). SB1 prohibits healthcare providers from prescribing,
administering, or dispensing puberty blockers or hormones to any mi-
nor for the purpose of (1) enabling the minor to identify with, or live
as, a purported identity inconsistent with the minor’s biological sex, or
(2) treating purported discomfort or distress from a discordance be-
tween the minor’s biological sex and asserted identity. At the same
time, SB1 permits a healthcare provider to administer puberty block-
ers or hormones to treat a minor’s congenital defect, precocious pu-
berty, disease, or physical injury.
Three transgender minors, their parents, and a doctor challenged
SB1 under the Equal Protection Clause of the Fourteenth Amendment
```

---
