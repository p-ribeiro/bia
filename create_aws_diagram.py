#!/usr/bin/env python3
"""
AWS Architecture Diagram Generator - PPTX format
Creates a diagram following the official AWS Architecture Icons Deck For Dark Backgrounds guidelines.

Architecture:
- Custom VPC with 2 Availability Zones
- Each AZ has a Public Subnet and a Private Subnet
- ALB in public subnets for HA
- NAT Gateway in public subnets for outbound internet from private subnets
- ECS with EC2 launch type running 2 instances in private subnets
- ECR for container image registry
- Internet Gateway for inbound traffic

AWS Dark Background Guidelines Applied:
- Background: #232F3E (AWS Galaxy/Dark)
- VPC Group: Green border (#1A8542)
- Availability Zone Group: Blue border (#147EBA)
- Public Subnet: Green fill with transparency (#1A8542 at ~15%)
- Private Subnet: Blue fill with transparency (#147EBA at ~15%)
- Text: White (#FFFFFF)
- Connector lines: White (#FFFFFF)
- Icons labeled below
"""

import zipfile
import os

# ============================================================
# PPTX is an Open XML package (ZIP) with specific structure
# We'll create all required XML files manually
# ============================================================

# --- Constants for AWS Dark Background Theme ---
# All measurements in EMU (English Metric Units): 1 inch = 914400 EMU
SLIDE_WIDTH = 12192000   # 13.33 inches (widescreen)
SLIDE_HEIGHT = 6858000   # 7.5 inches

# AWS Brand Colors (Dark Background palette)
BG_COLOR = "232F3E"       # AWS Galaxy (dark background)
VPC_BORDER = "1A8542"     # Green for VPC
AZ_BORDER = "147EBA"      # Blue for AZ
PUBLIC_SUBNET_FILL = "1A8542"   # Green for public subnet
PRIVATE_SUBNET_FILL = "147EBA"  # Blue for private subnet
WHITE = "FFFFFF"
ORANGE = "FF9900"         # AWS Smile/Orange (for key services)
LIGHT_GRAY = "D5DBDB"

# Transparency for subnet fills (0=opaque, 100000=fully transparent)
SUBNET_TRANSPARENCY = "85000"  # 85% transparent = 15% visible


def emu(inches):
    """Convert inches to EMU."""
    return int(inches * 914400)


def create_content_types():
    """[Content_Types].xml"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
</Types>'''


def create_rels():
    """_rels/.rels"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''


def create_presentation():
    """ppt/presentation.xml"""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
    <p:sldId id="256" r:id="rId2"/>
  </p:sldIdLst>
  <p:sldSz cx="{SLIDE_WIDTH}" cy="{SLIDE_HEIGHT}"/>
  <p:notesSz cx="{SLIDE_HEIGHT}" cy="{SLIDE_WIDTH}"/>
</p:presentation>'''


def create_presentation_rels():
    """ppt/_rels/presentation.xml.rels"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
</Relationships>'''


def create_theme():
    """ppt/theme/theme1.xml - AWS Dark theme"""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="AWS Dark Theme">
  <a:themeElements>
    <a:clrScheme name="AWS Dark">
      <a:dk1><a:srgbClr val="{BG_COLOR}"/></a:dk1>
      <a:lt1><a:srgbClr val="{WHITE}"/></a:lt1>
      <a:dk2><a:srgbClr val="161E2D"/></a:dk2>
      <a:lt2><a:srgbClr val="{LIGHT_GRAY}"/></a:lt2>
      <a:accent1><a:srgbClr val="{ORANGE}"/></a:accent1>
      <a:accent2><a:srgbClr val="{VPC_BORDER}"/></a:accent2>
      <a:accent3><a:srgbClr val="{AZ_BORDER}"/></a:accent3>
      <a:accent4><a:srgbClr val="527FFF"/></a:accent4>
      <a:accent5><a:srgbClr val="8C4FFF"/></a:accent5>
      <a:accent6><a:srgbClr val="E7157B"/></a:accent6>
      <a:hlink><a:srgbClr val="{ORANGE}"/></a:hlink>
      <a:folHlink><a:srgbClr val="527FFF"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="AWS">
      <a:majorFont><a:latin typeface="Amazon Ember"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Amazon Ember"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:fillStyleLst>
      <a:lnStyleLst>
        <a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
      </a:lnStyleLst>
      <a:effectStyleLst>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
      </a:effectStyleLst>
      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>'''


def create_slide_master():
    """ppt/slideMasters/slideMaster1.xml"""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="{BG_COLOR}"/></a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>
      </p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="dk1" tx1="lt1" bg2="dk2" tx2="lt2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
  </p:sldLayoutIdLst>
</p:sldMaster>'''


def create_slide_master_rels():
    """ppt/slideMasters/_rels/slideMaster1.xml.rels"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>'''


def create_slide_layout():
    """ppt/slideLayouts/slideLayout1.xml"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>
      </p:grpSpPr>
    </p:spTree>
  </p:cSld>
</p:sldLayout>'''


def create_slide_layout_rels():
    """ppt/slideLayouts/_rels/slideLayout1.xml.rels"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>'''


def create_slide_rels():
    """ppt/slides/_rels/slide1.xml.rels"""
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>'''


def make_rounded_rect(sp_id, name, x, y, cx, cy, border_color, fill_color=None, transparency=None, border_width=19050, dash=None):
    """Create a rounded rectangle shape (used for groups/containers)."""
    fill_xml = ""
    if fill_color:
        alpha = f'<a:alpha val="{100000 - int(transparency)}"/>' if transparency else ""
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill_color}">{alpha}</a:srgbClr></a:solidFill>'
    else:
        fill_xml = '<a:noFill/>'

    dash_xml = f'<a:prstDash val="{dash}"/>' if dash else ""

    return f'''<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sp_id}" name="{name}"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 3000"/></a:avLst></a:prstGeom>
    {fill_xml}
    <a:ln w="{border_width}">
      <a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill>
      {dash_xml}
    </a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="t" anchorCtr="0" lIns="91440" tIns="45720" rIns="91440" bIns="45720"/>
    <a:lstStyle/>
    <a:p><a:endParaRPr lang="en-US"/></a:p>
  </p:txBody>
</p:sp>'''


def make_label(sp_id, name, x, y, cx, cy, text, font_size=1000, bold=False, color=WHITE, anchor="ctr"):
    """Create a text label."""
    bold_attr = ' b="1"' if bold else ""
    return f'''<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sp_id}" name="{name}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/>
    <a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" anchor="{anchor}" anchorCtr="0"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"/>
      <a:r>
        <a:rPr lang="en-US" sz="{font_size}"{bold_attr} dirty="0">
          <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
          <a:latin typeface="Amazon Ember"/>
        </a:rPr>
        <a:t>{text}</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>'''


def make_service_icon(sp_id, name, x, y, size, icon_text, label_text, icon_color=ORANGE):
    """Create a service icon representation (colored square with text label below)."""
    label_y = y + size + emu(0.05)
    # Icon box
    icon_xml = f'''<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sp_id}" name="{name}_icon"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{size}" cy="{size}"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 8000"/></a:avLst></a:prstGeom>
    <a:solidFill><a:srgbClr val="{icon_color}"><a:alpha val="25000"/></a:srgbClr></a:solidFill>
    <a:ln w="19050"><a:solidFill><a:srgbClr val="{icon_color}"/></a:solidFill></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr" anchorCtr="1"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"/>
      <a:r>
        <a:rPr lang="en-US" sz="900" b="1" dirty="0">
          <a:solidFill><a:srgbClr val="{icon_color}"/></a:solidFill>
          <a:latin typeface="Amazon Ember"/>
        </a:rPr>
        <a:t>{icon_text}</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>'''
    # Label below icon
    label_xml = make_label(sp_id + 1, f"{name}_label", x - emu(0.2), label_y,
                           size + emu(0.4), emu(0.3), label_text, font_size=800, color=WHITE)
    return icon_xml + "\n" + label_xml


def make_connector(sp_id, name, x1, y1, x2, y2, color=WHITE, width=12700, dash=None):
    """Create a straight connector line."""
    dash_xml = f'<a:prstDash val="{dash}"/>' if dash else ""
    # Determine if we need flip
    flipH = ' flipH="1"' if x2 < x1 else ""
    flipV = ' flipV="1"' if y2 < y1 else ""
    cx = abs(x2 - x1)
    cy = abs(y2 - y1)
    off_x = min(x1, x2)
    off_y = min(y1, y2)

    return f'''<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="{sp_id}" name="{name}"/>
    <p:cNvCxnSpPr/>
    <p:nvPr/>
  </p:nvCxnSpPr>
  <p:spPr>
    <a:xfrm{flipH}{flipV}><a:off x="{off_x}" y="{off_y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>
    <a:ln w="{width}">
      <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
      {dash_xml}
      <a:tailEnd type="triangle" w="med" len="med"/>
    </a:ln>
  </p:spPr>
</p:cxnSp>'''


def create_slide():
    """ppt/slides/slide1.xml - The main architecture diagram slide."""
    
    # Layout coordinates (all in EMU)
    # Slide is 13.33" x 7.5"
    
    # Title area
    title_x = emu(0.3)
    title_y = emu(0.1)
    
    # AWS Cloud boundary
    cloud_x = emu(0.4)
    cloud_y = emu(0.8)
    cloud_w = emu(12.5)
    cloud_h = emu(6.4)
    
    # VPC boundary (inside cloud)
    vpc_x = emu(1.8)
    vpc_y = emu(1.5)
    vpc_w = emu(10.5)
    vpc_h = emu(5.5)
    
    # AZ 1 (left half of VPC)
    az1_x = vpc_x + emu(0.2)
    az1_y = vpc_y + emu(0.5)
    az1_w = emu(4.9)
    az1_h = emu(4.8)
    
    # AZ 2 (right half of VPC)
    az2_x = az1_x + az1_w + emu(0.2)
    az2_y = az1_y
    az2_w = az1_w
    az2_h = az1_h
    
    # Public subnets (top portion of each AZ)
    pub1_x = az1_x + emu(0.15)
    pub1_y = az1_y + emu(0.45)
    pub_w = emu(4.6)
    pub_h = emu(1.8)
    
    pub2_x = az2_x + emu(0.15)
    pub2_y = pub1_y
    
    # Private subnets (bottom portion of each AZ)
    priv1_x = pub1_x
    priv1_y = pub1_y + pub_h + emu(0.2)
    priv_w = pub_w
    priv_h = emu(2.1)
    
    priv2_x = pub2_x
    priv2_y = priv1_y
    
    # Service icon size
    icon_size = emu(0.5)
    
    # Internet Gateway position (top of VPC, centered)
    igw_x = vpc_x + vpc_w // 2 - icon_size // 2
    igw_y = vpc_y + emu(0.05)
    
    # ALB positions (in public subnets)
    alb1_x = pub1_x + pub_w // 2 - icon_size // 2
    alb1_y = pub1_y + emu(0.3)
    
    alb2_x = pub2_x + pub_w // 2 - icon_size // 2
    alb2_y = pub2_y + emu(0.3)
    
    # NAT Gateway positions (in public subnets, right side)
    nat1_x = pub1_x + pub_w - icon_size - emu(0.3)
    nat1_y = pub1_y + emu(0.9)
    
    nat2_x = pub2_x + pub_w - icon_size - emu(0.3)
    nat2_y = pub2_y + emu(0.9)
    
    # ECS/EC2 instances (in private subnets)
    ecs1_x = priv1_x + priv_w // 2 - icon_size // 2
    ecs1_y = priv1_y + emu(0.6)
    
    ecs2_x = priv2_x + priv_w // 2 - icon_size // 2
    ecs2_y = priv2_y + emu(0.6)
    
    # ECR (outside VPC, left side)
    ecr_x = cloud_x + emu(0.3)
    ecr_y = cloud_h // 2 + cloud_y - icon_size // 2
    
    # Users/Internet (top left, outside cloud)
    users_x = emu(0.5)
    users_y = emu(0.2)
    
    # Build shapes
    sp_id = 10  # Starting shape ID
    shapes = []
    
    # --- Title ---
    shapes.append(make_label(sp_id, "title", title_x, title_y, emu(8), emu(0.5),
                            "AWS ECS Architecture - High Availability with ALB &amp; NAT Gateway",
                            font_size=1600, bold=True, color=WHITE, anchor="t"))
    sp_id += 2
    
    # --- AWS Cloud boundary ---
    shapes.append(make_rounded_rect(sp_id, "AWS Cloud", cloud_x, cloud_y, cloud_w, cloud_h,
                                    border_color=ORANGE, border_width=25400, dash="dash"))
    sp_id += 1
    shapes.append(make_label(sp_id, "cloud_label", cloud_x + emu(0.2), cloud_y + emu(0.05),
                            emu(2), emu(0.35), "AWS Cloud", font_size=1100, bold=True, color=ORANGE, anchor="t"))
    sp_id += 2
    
    # --- VPC boundary ---
    shapes.append(make_rounded_rect(sp_id, "VPC", vpc_x, vpc_y, vpc_w, vpc_h,
                                    border_color=VPC_BORDER, border_width=25400))
    sp_id += 1
    shapes.append(make_label(sp_id, "vpc_label", vpc_x + emu(0.15), vpc_y + emu(0.05),
                            emu(3.5), emu(0.35), "VPC (10.0.0.0/16)", font_size=1000, bold=True, color=VPC_BORDER, anchor="t"))
    sp_id += 2
    
    # --- Availability Zone 1 ---
    shapes.append(make_rounded_rect(sp_id, "AZ1", az1_x, az1_y, az1_w, az1_h,
                                    border_color=AZ_BORDER, border_width=19050, dash="dash"))
    sp_id += 1
    shapes.append(make_label(sp_id, "az1_label", az1_x + emu(0.1), az1_y + emu(0.05),
                            emu(2.5), emu(0.3), "Availability Zone 1", font_size=900, bold=True, color=AZ_BORDER, anchor="t"))
    sp_id += 2
    
    # --- Availability Zone 2 ---
    shapes.append(make_rounded_rect(sp_id, "AZ2", az2_x, az2_y, az2_w, az2_h,
                                    border_color=AZ_BORDER, border_width=19050, dash="dash"))
    sp_id += 1
    shapes.append(make_label(sp_id, "az2_label", az2_x + emu(0.1), az2_y + emu(0.05),
                            emu(2.5), emu(0.3), "Availability Zone 2", font_size=900, bold=True, color=AZ_BORDER, anchor="t"))
    sp_id += 2
    
    # --- Public Subnet 1 ---
    shapes.append(make_rounded_rect(sp_id, "PublicSubnet1", pub1_x, pub1_y, pub_w, pub_h,
                                    border_color=VPC_BORDER, fill_color=PUBLIC_SUBNET_FILL,
                                    transparency=SUBNET_TRANSPARENCY, border_width=12700))
    sp_id += 1
    shapes.append(make_label(sp_id, "pub1_label", pub1_x + emu(0.1), pub1_y + emu(0.05),
                            emu(2.5), emu(0.25), "Public Subnet", font_size=800, bold=True, color=VPC_BORDER, anchor="t"))
    sp_id += 2
    
    # --- Public Subnet 2 ---
    shapes.append(make_rounded_rect(sp_id, "PublicSubnet2", pub2_x, pub2_y, pub_w, pub_h,
                                    border_color=VPC_BORDER, fill_color=PUBLIC_SUBNET_FILL,
                                    transparency=SUBNET_TRANSPARENCY, border_width=12700))
    sp_id += 1
    shapes.append(make_label(sp_id, "pub2_label", pub2_x + emu(0.1), pub2_y + emu(0.05),
                            emu(2.5), emu(0.25), "Public Subnet", font_size=800, bold=True, color=VPC_BORDER, anchor="t"))
    sp_id += 2
    
    # --- Private Subnet 1 ---
    shapes.append(make_rounded_rect(sp_id, "PrivateSubnet1", priv1_x, priv1_y, priv_w, priv_h,
                                    border_color=PRIVATE_SUBNET_FILL, fill_color=PRIVATE_SUBNET_FILL,
                                    transparency=SUBNET_TRANSPARENCY, border_width=12700))
    sp_id += 1
    shapes.append(make_label(sp_id, "priv1_label", priv1_x + emu(0.1), priv1_y + emu(0.05),
                            emu(2.5), emu(0.25), "Private Subnet", font_size=800, bold=True, color=PRIVATE_SUBNET_FILL, anchor="t"))
    sp_id += 2
    
    # --- Private Subnet 2 ---
    shapes.append(make_rounded_rect(sp_id, "PrivateSubnet2", priv2_x, priv2_y, priv_w, priv_h,
                                    border_color=PRIVATE_SUBNET_FILL, fill_color=PRIVATE_SUBNET_FILL,
                                    transparency=SUBNET_TRANSPARENCY, border_width=12700))
    sp_id += 1
    shapes.append(make_label(sp_id, "priv2_label", priv2_x + emu(0.1), priv2_y + emu(0.05),
                            emu(2.5), emu(0.25), "Private Subnet", font_size=800, bold=True, color=PRIVATE_SUBNET_FILL, anchor="t"))
    sp_id += 2
    
    # --- Internet Gateway ---
    shapes.append(make_service_icon(sp_id, "IGW", igw_x, igw_y, icon_size, "IGW", "Internet Gateway", icon_color="8C4FFF"))
    sp_id += 2
    
    # --- ALB (centered between the two public subnets, representing cross-AZ) ---
    alb_x = vpc_x + vpc_w // 2 - icon_size // 2
    alb_y = pub1_y + emu(0.6)
    shapes.append(make_service_icon(sp_id, "ALB", alb_x, alb_y, icon_size, "ALB", "Application Load Balancer", icon_color=ORANGE))
    sp_id += 2
    
    # --- NAT Gateway 1 ---
    shapes.append(make_service_icon(sp_id, "NAT1", nat1_x, nat1_y, icon_size, "NAT", "NAT Gateway", icon_color=VPC_BORDER))
    sp_id += 2
    
    # --- NAT Gateway 2 ---
    shapes.append(make_service_icon(sp_id, "NAT2", nat2_x, nat2_y, icon_size, "NAT", "NAT Gateway", icon_color=VPC_BORDER))
    sp_id += 2
    
    # --- ECS Task 1 (EC2 instance in private subnet 1) ---
    shapes.append(make_service_icon(sp_id, "ECS1", ecs1_x, ecs1_y, icon_size, "ECS", "ECS Task (EC2)", icon_color=ORANGE))
    sp_id += 2
    
    # --- ECS Task 2 (EC2 instance in private subnet 2) ---
    shapes.append(make_service_icon(sp_id, "ECS2", ecs2_x, ecs2_y, icon_size, "ECS", "ECS Task (EC2)", icon_color=ORANGE))
    sp_id += 2
    
    # --- ECR ---
    shapes.append(make_service_icon(sp_id, "ECR", ecr_x, ecr_y, icon_size, "ECR", "Elastic Container Registry", icon_color=ORANGE))
    sp_id += 2
    
    # --- Connectors ---
    
    # Internet -> IGW
    shapes.append(make_connector(sp_id, "conn_inet_igw",
                                igw_x + icon_size // 2, cloud_y,
                                igw_x + icon_size // 2, igw_y,
                                color=WHITE, width=19050))
    sp_id += 1
    
    # IGW -> ALB
    shapes.append(make_connector(sp_id, "conn_igw_alb",
                                igw_x + icon_size // 2, igw_y + icon_size,
                                alb_x + icon_size // 2, alb_y,
                                color=WHITE, width=15875))
    sp_id += 1
    
    # ALB -> ECS1
    shapes.append(make_connector(sp_id, "conn_alb_ecs1",
                                alb_x + icon_size // 2, alb_y + icon_size,
                                ecs1_x + icon_size // 2, ecs1_y,
                                color=ORANGE, width=15875))
    sp_id += 1
    
    # ALB -> ECS2
    shapes.append(make_connector(sp_id, "conn_alb_ecs2",
                                alb_x + icon_size // 2, alb_y + icon_size,
                                ecs2_x + icon_size // 2, ecs2_y,
                                color=ORANGE, width=15875))
    sp_id += 1
    
    # ECS1 -> NAT1 (outbound internet via NAT)
    shapes.append(make_connector(sp_id, "conn_ecs1_nat1",
                                ecs1_x + icon_size // 2, ecs1_y,
                                nat1_x + icon_size // 2, nat1_y + icon_size,
                                color=VPC_BORDER, width=12700, dash="dash"))
    sp_id += 1
    
    # ECS2 -> NAT2 (outbound internet via NAT)
    shapes.append(make_connector(sp_id, "conn_ecs2_nat2",
                                ecs2_x + icon_size // 2, ecs2_y,
                                nat2_x + icon_size // 2, nat2_y + icon_size,
                                color=VPC_BORDER, width=12700, dash="dash"))
    sp_id += 1
    
    # ECR -> ECS1 (image pull)
    shapes.append(make_connector(sp_id, "conn_ecr_ecs1",
                                ecr_x + icon_size, ecr_y + icon_size // 2,
                                ecs1_x, ecs1_y + icon_size // 2,
                                color=LIGHT_GRAY, width=9525, dash="dash"))
    sp_id += 1
    
    # ECR -> ECS2 (image pull)
    shapes.append(make_connector(sp_id, "conn_ecr_ecs2",
                                ecr_x + icon_size, ecr_y + icon_size // 2,
                                ecs2_x, ecs2_y + icon_size // 2,
                                color=LIGHT_GRAY, width=9525, dash="dash"))
    sp_id += 1
    
    # --- Users icon (top-center, outside cloud) ---
    shapes.append(make_service_icon(sp_id, "Users", igw_x, cloud_y - emu(0.7), icon_size, "&#x1F310;", "Users / Internet", icon_color="527FFF"))
    sp_id += 2
    
    # --- Legend ---
    legend_x = cloud_x + cloud_w - emu(2.8)
    legend_y = cloud_y + emu(0.1)
    shapes.append(make_label(sp_id, "legend_title", legend_x, legend_y, emu(2.5), emu(0.25),
                            "Legend:", font_size=800, bold=True, color=WHITE, anchor="t"))
    sp_id += 2
    shapes.append(make_label(sp_id, "legend1", legend_x, legend_y + emu(0.25), emu(2.5), emu(0.2),
                            "&#x25A0; Public Subnet (Green)", font_size=700, color=VPC_BORDER, anchor="t"))
    sp_id += 2
    shapes.append(make_label(sp_id, "legend2", legend_x, legend_y + emu(0.45), emu(2.5), emu(0.2),
                            "&#x25A0; Private Subnet (Blue)", font_size=700, color=PRIVATE_SUBNET_FILL, anchor="t"))
    sp_id += 2
    shapes.append(make_label(sp_id, "legend3", legend_x, legend_y + emu(0.65), emu(2.5), emu(0.2),
                            "--- Outbound traffic (NAT)", font_size=700, color=VPC_BORDER, anchor="t"))
    sp_id += 2
    shapes.append(make_label(sp_id, "legend4", legend_x, legend_y + emu(0.85), emu(2.5), emu(0.2),
                            "&#x2192; Inbound traffic (ALB)", font_size=700, color=ORANGE, anchor="t"))
    sp_id += 2
    
    # Combine all shapes
    all_shapes = "\n".join(shapes)
    
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="{BG_COLOR}"/></a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {all_shapes}
    </p:spTree>
  </p:cSld>
</p:sld>'''


def build_pptx(output_path):
    """Assemble the PPTX file."""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', create_content_types())
        zf.writestr('_rels/.rels', create_rels())
        zf.writestr('ppt/presentation.xml', create_presentation())
        zf.writestr('ppt/_rels/presentation.xml.rels', create_presentation_rels())
        zf.writestr('ppt/theme/theme1.xml', create_theme())
        zf.writestr('ppt/slideMasters/slideMaster1.xml', create_slide_master())
        zf.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels', create_slide_master_rels())
        zf.writestr('ppt/slideLayouts/slideLayout1.xml', create_slide_layout())
        zf.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels', create_slide_layout_rels())
        zf.writestr('ppt/slides/slide1.xml', create_slide())
        zf.writestr('ppt/slides/_rels/slide1.xml.rels', create_slide_rels())
    
    print(f"✅ PPTX file created: {output_path}")
    print(f"   File size: {os.path.getsize(output_path):,} bytes")


if __name__ == "__main__":
    output = "/projects/sandbox/AWS_ECS_Architecture_Dark_BG.pptx"
    build_pptx(output)
    print("\n📋 Diagram Details:")
    print("   - Dark background (#232F3E - AWS Galaxy)")
    print("   - VPC with green border (#1A8542)")
    print("   - 2 Availability Zones with blue dashed borders (#147EBA)")
    print("   - Public subnets (green tint) with ALB nodes and NAT Gateways")
    print("   - Private subnets (blue tint) with ECS Tasks on EC2")
    print("   - ECR outside VPC for container image registry")
    print("   - Internet Gateway at VPC edge")
    print("   - Connector lines showing traffic flow")
    print("   - Legend included")
    print("\n📐 AWS Architecture Icons Guidelines Applied:")
    print("   ✓ Dark background theme")
    print("   ✓ Official group border colors (VPC=green, AZ=blue)")
    print("   ✓ Subnet fills with transparency")
    print("   ✓ Service icons with labels below")
    print("   ✓ Direct connector lines")
    print("   ✓ Adequate whitespace")
    print("   ✓ Rounded rectangle containers")
    print("   ✓ AWS brand color palette (Orange, Green, Blue, Purple)")
