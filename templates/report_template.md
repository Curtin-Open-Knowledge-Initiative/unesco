{% import "report_macros.md" as helper with context %}
{% include "report_css.html" %}

<!-- Title Page -->
<pdf:nexttemplate name="titlepage">
<pdf:nextpage>

<p class="subtitle">UNESCO REPORT</p>
<p class="titlemeta"><br>DATE: {{ helper.created_at()|upper }}</p>


<!-- switch page templates -->
<pdf:nexttemplate name="report">

<pdf:nextpage>

# Summary and Abstract

This report contains example graphs and data to support the UNESCO Open Science Declaration communication plans. The 
focus is on showing regional open access levels rising, citation advantages for open access, the relationship 
between collaboration and open access and open access relating to the sustainable development goals.

# Open Access by Region

Open access (including all accessible outputs) is reported by UNESCO electoral region. Latin America and the Caribbean, 
and Africa show the highest levels of open access over the whole reporting period, demonstrating a long-standing 
commitment to access.

![](oa_regions.png)

Interestingly global levels of OA are relatively low compared to some of the strong performers. This is in part due 
to collaborations, which are systematically high in OA levels. If we examine OA levels based on the number of UNESCO 
Electoral regions that contributed to the outputs (i.e. number of collaborating regions) then we see the more 
collaborative outputs are, the higher the levels of open access are, right across the time period. Highly 
international work (collaborations across five or six regions) are very strongly open, for the whole reporting period.

![](collab_regions.png)

<pdf:nextpage>
# Open Access Citation Advantage

There is an association between open access and higher citations. We see this across most regions and the whole time 
period under analysis. There are some interesting cases where non-OA have higher average citations, with some 
periods for Latin America and the Caribbean and for Asia and the Pacific. These show differences in the way that 
prestige and visibility have interacted with open access under the different policy regimes in different regions.

![](citations_region_2010-14-18.png)

<pdf:nextpage>
# Sustainable Development Goals

It might be expected that research pursuing the Sustainable Development Goals is higher in OA levels than other 
research, but there is little evidence of this. Health and Education research have higher levels of open access 
consistent with disciplinary differences. Overall levels of OA for the SDGs are only marginally higher than the 
levels of OA globally.

![](any_sdg.png)

Looking across the SDGs there are a variety of patterns. It is perhaps good to see that research that explicitly 
references the SDGs shows a reasonably high level of open access.

![](sdgs_oa.png)
