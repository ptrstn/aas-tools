from aastools import crud, services
from aastools.upload import upload_aas_folder


def test_get_shells(semitrailer, workpiece_carrier_a1):
    services.delete_all_submodels()
    services.delete_all_shells()
    upload_aas_folder("aas")
    shells = crud.get_shells()
    assert len(shells) == 2


def test_get_shell(
    semitrailer,
    workpiece_carrier_a1,
):
    shell = crud.get_shell(semitrailer.id)
    assert shell["id"] == semitrailer.id
    assert shell["idShort"] == semitrailer.id_short

    shell = crud.get_shell(workpiece_carrier_a1.id)
    assert shell["id"] == workpiece_carrier_a1.id
    assert shell["idShort"] == workpiece_carrier_a1.id_short


def test_get_submodel(
    semitrailer,
    workpiece_carrier_a1,
):
    submodel = crud.get_submodel(semitrailer.product_identification.id)
    assert submodel["idShort"] == semitrailer.product_identification.id_short

    submodel = crud.get_submodel(semitrailer.production_plan.id)
    assert submodel["idShort"] == semitrailer.production_plan.id_short

    submodel = crud.get_submodel(workpiece_carrier_a1.good_information.id)
    assert submodel["idShort"] == workpiece_carrier_a1.good_information.id_short

    submodel = crud.get_submodel(workpiece_carrier_a1.asset_location.id)
    assert submodel["idShort"] == workpiece_carrier_a1.asset_location.id_short


def test_get_submodel_elements(
    semitrailer,
    workpiece_carrier_a1,
):
    elements = crud.get_submodel_elements(semitrailer.product_identification.id)
    assert elements[0]["idShort"] == "Identifier"
    assert elements[1]["idShort"] == "ProductName"
    assert elements[1]["value"] == "Semitrailer"

    elements = crud.get_submodel_elements(workpiece_carrier_a1.good_information.id)
    assert elements[0]["idShort"] == "CurrentProduct"
    assert elements[0]["value"] == semitrailer.id
    assert elements[1]["idShort"] == "ListTransportableProducts"
    assert elements[2]["idShort"] == "ProductName"
    assert elements[2]["value"] == "Semitrailer"

    elements = crud.get_submodel_elements(workpiece_carrier_a1.asset_location.id)
    assert elements[0]["idShort"] == "CurrentFences"
    assert elements[0]["value"][0]["value"][0]["idShort"] == "FenceName"
    assert elements[0]["value"][0]["value"][0]["value"] == "TSN-Module"


def test_set_submodel_element(
    workpiece_carrier_a1,
):
    old_product_name = "Semitrailer"
    new_product_name = "A New Product Name"

    crud.set_submodel_element_value(
        submodel_id=workpiece_carrier_a1.good_information.id,
        id_short_path="ProductName",
        value=new_product_name,
    )

    elements = crud.get_submodel_elements(workpiece_carrier_a1.good_information.id)
    assert elements[2]["value"] == new_product_name

    # Reset
    crud.set_submodel_element_value(
        submodel_id=workpiece_carrier_a1.good_information.id,
        id_short_path="ProductName",
        value=old_product_name,
    )
    elements = crud.get_submodel_elements(workpiece_carrier_a1.good_information.id)
    assert elements[2]["value"] == old_product_name


#
#
def test_set_current_fence_name(
    workpiece_carrier_a1,
):
    old_fence_name = "TSN-Module"
    new_fence_name = "New-Fence-001"

    crud.set_submodel_element_value(
        submodel_id=workpiece_carrier_a1.asset_location.id,
        id_short_path="CurrentFences[0].FenceName",
        value=new_fence_name,
    )

    elements = crud.get_submodel_elements(workpiece_carrier_a1.asset_location.id)
    assert elements[0]["idShort"] == "CurrentFences"
    assert elements[0]["value"][0]["value"][0]["idShort"] == "FenceName"
    assert elements[0]["value"][0]["value"][0]["value"] == new_fence_name

    crud.set_submodel_element_value(
        submodel_id=workpiece_carrier_a1.asset_location.id,
        id_short_path="CurrentFences[0].FenceName",
        value=old_fence_name,
    )

    elements = crud.get_submodel_elements(workpiece_carrier_a1.asset_location.id)
    assert elements[0]["value"][0]["value"][0]["value"] == old_fence_name
