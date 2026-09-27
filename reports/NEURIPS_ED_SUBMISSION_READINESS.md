# NeurIPS 2026 E&D submission readiness

**Status: BLOCKED_EXTERNAL**

This checker separates repository/scientific completeness from requirements that need external venue assets or hosting.

- PASS: **anonymous paper source** - paper/PAPER.md contains no public author name
- PASS: **15 checklist answers** - paper/APPENDIX_CHECKLIST.md contains items 1-15
- PASS: **official-template-ready source** - paper/main_neurips_2026.tex generated
- BLOCKED: **official NeurIPS 2026 style present** - Download official 2026 template and place paper/neurips_2026.sty before final submission
- PASS: **Croissant core: @context** - @context present
- PASS: **Croissant core: @type** - @type present
- PASS: **Croissant core: name** - name present
- PASS: **Croissant core: url** - url present
- PASS: **Croissant core: license** - license present
- PASS: **Croissant core: conformsTo** - conformsTo present
- PASS: **Croissant core: distribution** - distribution present
- PASS: **Croissant core: recordSet** - recordSet present
- PASS: **Croissant RAI: rai:dataLimitations** - rai:dataLimitations present
- PASS: **Croissant RAI: rai:dataBiases** - rai:dataBiases present
- PASS: **Croissant RAI: rai:personalSensitiveInformation** - rai:personalSensitiveInformation present
- PASS: **Croissant RAI: rai:dataUseCases** - rai:dataUseCases present
- PASS: **Croissant RAI: rai:dataSocialImpact** - rai:dataSocialImpact present
- PASS: **Croissant RAI: rai:hasSyntheticData** - rai:hasSyntheticData present
- PASS: **Croissant RAI: prov:wasGeneratedBy** - prov:wasGeneratedBy present
- BLOCKED: **anonymous reviewer-accessible dataset URL** - current url='REPLACE_WITH_ANONYMOUS_REVIEW_URL_BEFORE_SUBMISSION'; must be externally accessible at submission
- PASS: **anonymous submission bundle** - submission zip exists
- PASS: **bundle excludes author-facing metadata** - suspicious files=[]
- PASS: **readable draft PDF** - generic-style research draft exists; not venue-format final
- PASS: **PDF under 50MB** - NeurIPS maximum file size is 50MB
- PASS: **generic draft content <=9 pages** - content pages before references=8
- PASS: **anonymous PDF content scan** - leaks=[]
- PASS: **anonymous bundle content scan** - leaks=[]

## External blockers

- official NeurIPS 2026 style present: Download official 2026 template and place paper/neurips_2026.sty before final submission
- anonymous reviewer-accessible dataset URL: current url='REPLACE_WITH_ANONYMOUS_REVIEW_URL_BEFORE_SUBMISSION'; must be externally accessible at submission
