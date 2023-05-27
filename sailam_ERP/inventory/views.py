from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from .models import inventory
# Create your views here.

def loadGiaData(request):
    if request.method=="POST":
        url_end_point = "https://api.reportresults.gia.edu/"
        report_number = request.POST.get("gianumber")

        query = {
        "query": '''
            query($reportNumber: String!) {
            getReport(report_number: $reportNumber) {
                
                report_number
                report_date
                report_date_iso
                report_type
                report_type_code
                industry_disclosures {
                        ...IndustryDisclosureFields
                    }
                supplemental_report_results {
                        ...SupplementalReportResultFields
                    }
                results {
                __typename
                ...DiamondGradingResultFields
                ...PearlIdentResultFields
                ...NarrativeResultFields
                ...LabGrownResultFields
                ...IdentificationResultFields
                ...MeleeResultFields
                }
                links {
                ...LinkFields
                }
                assets {
                    ...AssetFields
                }
            }
            }

            fragment DiamondGradingResultFields on DiamondGradingReportResults {
            shape_and_cutting_style
            measurements
            carat_weight
            color_grade
            color_origin
            color_distribution
            clarity_grade
            cut_grade
            polish
            symmetry
            fluorescence
            clarity_characteristics
            inscriptions
            country_of_origin
            diamond_type
            report_comments
            proportions {
                ...DiamondProportionFields
            }
            data {
                ...DiamondGradingDataFields
            }
            }

            fragment PearlIdentResultFields on PearlIdentReportResults {
            report_title
            item_description
            weight
            measurements
            shape
            bodycolor
            overtone
            identification
            environment
            mollusk
            quantity
            surface
            luster
            matching
            drilling
            treatment
            report_comments
            }

            fragment NarrativeResultFields on NarrativeReportResults {
            report_title
            description
            conclusion
            report_comments
            inscriptions
            pearl_identification
            }

            fragment LabGrownResultFields on LabGrownDiamondGradingReportResults {
            identification
            shape_and_cutting_style
            measurements
            carat_weight
            color_grade
            color_origin
            color_distribution
            clarity_grade
            cut_grade
            polish
            symmetry
            fluorescence
            inscriptions
            report_comments
            }

            fragment IdentificationResultFields on IdentificationReportResults {
            weight
            measurements
            shape
            cutting_style
            cutting_style_crown
            cutting_style_pavilion
            transparency
            color
            item_description
            species
            geographic_origin
            variety
            phenomenon
            treatment
            report_comments
            }

            fragment MeleeResultFields on MeleeServiceResults {
            packages {
                service_results_number
                issue_date
                melee_shape
                diameter
                total_carat_weight
                color_range
                number_of_items
                material_test_results
                comments
            }
            }

            fragment LinkFields on Links {
            pdf
            proportions_diagram
            plotting_diagram
            image
            rough_image
            rough_video
            polished_image
            polished_video
            dtl_pdf_filename
            dttl_pdf_filename
            dtlp_pdf_filename
            dtlp_image_filename
            ideal_report_pdf
            aset_image
            digital_card
            }

            fragment AssetFields on ReportAsset {
            asset_type_code
            asset_type_description
            link
            }

            fragment DiamondProportionFields on DiamondProportions {
            depth_pct
            table_pct
            crown_angle
            crown_height
            pavilion_angle
            pavilion_depth
            star_length
            lower_half
            girdle
            culet
            }

            fragment DiamondGradingDataFields on DiamondData {
            shape {
                shape_category
                shape_code
                shape_group
                shape_group_code
            }
            measurements {
                __typename
                ... on RoundMeasurements {
                min_diam
                max_diam
                depth
                }
                ... on FancyMeasurements {
                length
                width
                depth
                }
            }
            weight {
                weight
                weight_unit
            }
            color {
                color_grade_code
                color_modifier
            }
            clarity
            cut
            polish
            symmetry
            fluorescence {
                fluorescence_intensity
                fluorescence_color
            }
            girdle {
                girdle_condition
                girdle_condition_code
                girdle_pct
                girdle_size
                girdle_size_code
            }
            culet {
                culet_code
            }  
            }
            fragment IndustryDisclosureFields on IndustryDisclosures {
                disclosed_source {
                name
                code
            }
            }
            fragment SupplementalReportResultFields on SupplementalReportResults {	
                ... on IdealReportResults {
                            shape_and_cutting_style,
                            measurements,
                            carat_weight,
                            light_performance_grade,
                            brightness,
                            fire,
                            contrast
                        }
            }
        ''',
        "variables": {
            "reportNumber": report_number
        }
    }

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "64112d47-a247-4259-a9d0-a402e186f4a8"
    }

        response = requests.post(url_end_point, data=json.dumps(query), headers=headers)
        data = response.json()
    return HttpResponse(json.dumps(data),content_type="application/json")
    
def insertDiamond(request):
    if request.method=="POST":
       user=request.user
       stkno=request.POST.get("stkno")
       size=request.POST.get("size")
       shape=request.POST.get("shape")
       color=request.POST.get("color")
       clarity=request.POST.get("clarity")
       polish=request.POST.get("polish")
       symmetry=request.POST.get("symmetry");
       cut=request.POST.get("cut")
       fluorescence=request.POST.get("fluorescence")
       mesurement=request.POST.get("mesurement")
       depth=request.POST.get("depth")
       table=request.POST.get("table")
       giano=request.POST.get("giano")
       remark=request.POST.get("remark")
       photo=request.POST.get("photo")
       video=request.POST.get("video")
       price=request.POST.get("price")
       stkid=request.POST.get("stkid")
       crt=request.POST.get("crt")
       purity=request.POST.get("purity")
       desc=request.POST.get("desc")
       exist=inventory.objects.filter(GIA_NO=giano).values()
       if not exist:
        stock=inventory.objects.create(STK_NO=stkno,SIZE=size,SHAPE=shape,COLOR=color,CLARITY=clarity,POL=polish,SYM=symmetry,CUT=cut,FLO_COL=fluorescence,MESUREMNT=mesurement,DEPTH=depth,TABLE=table,GIA_NO=giano,REMARK=remark,PHOTO=photo,VIDEO=video,PRICE=price,STK_ID=stkid,CRT=crt,PURITY=purity,DESCRIPTION=desc,CretedBy=user,)
        if stock:
          return render(request,'inventory/inventory.html',{"message":"Data Inserted Successfully!"})
       else:
          print(exist)
          return render(request,'inventory/inventory.html',{"errormessage":"Data Is Already Present"})
    else:
     return render(request,'inventory/inventory.html')
    
def viewStock(request):
    stocks=inventory.objects.all()
    context={
       "stocks":stocks
    }
    return render(request,'inventory/viewinventory.html',context)