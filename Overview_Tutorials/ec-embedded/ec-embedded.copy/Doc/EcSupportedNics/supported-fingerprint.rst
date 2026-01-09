Supported fingerprint
*********************

.. datatemplate:xml::
    :source: _build/doxygen/xml/combined.xml
    
    {% set supported_nics_json = load("_build/SupportedNics.json") %}
    {% for arch in supported_nics_json["arch"] %}
    {%   set compound = data.find("./compounddef[@kind='page']/[compoundname='EC_FINGERPRINT_" + arch.upper() +"']") %}
    {%   if compound is not none: %}
    .. _fingerprint-{{arch}}:
    .. rubric:: {{arch}}
    {%     for para in compound.findall("detaileddescription/para/variablelist/listitem/para") %}
    {%       set para_text = "".join(para.itertext()).strip() %}
    {%       if para_text: %}
    - {{para_text}}
    {%       endif %}
    {%     endfor %}
    {%   endif %}
    {% endfor %}
