# import os, sys, ogr
from qgis.core import QgsCoordinateReferenceSystem, QgsProcessingRegistry
from qgis.core import QgsApplication, QgsVectorLayer, QgsProject, QgsVectorFileWriter, QgsVectorLayerExporter
import processing
from processing.modeler.ModelerDialog import ModelerDialog
from processing import runAndLoadResults
from processing.core.Processing import Processing

path_to_qgis_app = "C:\Program Files\QGIS 3.28.1\apps\qgis"

path_to_competitor = "/sao_vicente_americana_sp/sao_vicente_americana_sp/concorrentes/Concorrentes São Vicente Americana SP.kml "

path_to_store = "/sao_vicente_americana_sp/sao_vicente_americana_sp/concorrentes/LOJA 01.kml"

shp_gpkg_folder = "C:/Users/yukif/Bnex/shp_gpkg_files"

# path_to_csv = "C:/Users/yukif/Bnex/sao_vicente_americana_sp/sao_vicente_americana_sp/concorrentes/Lista de concorrentes São Vicente Americana SP.csv?delimiter={}".format(
#     ";")
path_to_csv = "sao_vicente_americana_sp/sao_vicente_americana_sp/concorrentes/Lista de concorrentes São Vicente Americana SP.csv"
# uri = "file://{}/testdata/delimited_xy.csv?delimiter={}&xField={}&yField={}".format(os.getcwd(), ";", "x", "y")

path_to_model = "C:/Users/yukif/Bnex/sao_vicente_americana_sp/sao_vicente_americana_sp/models/GP_BNEXv6.model3"

QgsApplication.setPrefixPath(path_to_qgis_app, True)
# QgsApplication.setPrefixPath("C:\Program Files\QGIS 3.28.1\apps\qgis", False)
qgs = QgsApplication([], False)


# Load providers
def start_qgis():
    qgs.initQgis()
    print("Qgis Iniciado")


# Exit providers
def exit_qgis():
    qgs.exitQgis()
    print("Qgis Finalizado")


def convert_kml_to_shp(layer_path, layer_name, shp_file_folder):
    vlayer_ = QgsVectorLayer(layer_path, f"kml_{layer_name}", "ogr")
    writer = QgsVectorFileWriter.writeAsVectorFormat(vlayer_, f"{shp_file_folder}/{layer_name}", "ESRI Shapefile")

    converted_layer_path = f"{shp_file_folder}/{layer_name}.gpkg"
    return converted_layer_path


def create_vector_layer(path_to_vlayer, layer_name, provider_name="ogr"):
    vlayer = QgsVectorLayer(path_to_vlayer, layer_name, provider_name)

    if not vlayer.isValid():
        print(f"Layer {layer_name} failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)


def open_model(model_path, concorrencia_path, ponto_path, tabela_concorrencia_path):
    try:
        Processing.initialize()
        # Processing.updateAlgsList()

        dlg = ModelerDialog()

        dlg.loadModel(model_path)

        # print(f"Found the model: {QgsProcessingRegistry.algorithmById(dlg.model)}")
        print(f"modelo: {dlg.model()}")

        processing.runAndLoadResults(
            dlg.model(),
            {
                'concorrencia': concorrencia_path,
                'native:buffer_4:buff_aprox4km': 'TEMPORARY_OUTPUT',
                'native:extractbyexpression_1:mp': 'TEMPORARY_OUTPUT',
                'native:extractbyexpression_2:gp': 'TEMPORARY_OUTPUT',
                'native:extractbyexpression_3:mm_pp': 'TEMPORARY_OUTPUT',
                'native:extractbyexpression_5:at': 'TEMPORARY_OUTPUT',
                'native:joinattributestable_1:CONCORRENTES': 'TEMPORARY_OUTPUT',
                'native:joinattributestable_2:dist_unido': 'TEMPORARY_OUTPUT',
                'ponto': ponto_path,
                'qgis:fieldcalculator_1:buff_3km': 'TEMPORARY_OUTPUT',
                'qgis:fieldcalculator_2:buff_1km': 'TEMPORARY_OUTPUT',
                'qgis:fieldcalculator_3:buff_2km': 'TEMPORARY_OUTPUT',
                'qgis:refactorfields_2:uniao_isos': 'TEMPORARY_OUTPUT',
                'tabelaconcorrencia': tabela_concorrencia_path
            }
        )

        # dlg.loadModel('C:/Users/Me/Desktop/test.model3')
        # runAndLoadResults(
        #     dlg.model, {'layer': 'C:/Users/Me/Desktop/Point_example.shp', 'native:buffer_1:result': 'memory:'}
        # )
    except BaseException as err:
        print(f"Error during open_model: {err}")
        exit_qgis()


if __name__ == '__main__':
    start_qgis()

    competitor_gpkg_path = convert_kml_to_shp(path_to_competitor, "concorrencia", shp_gpkg_folder)
    store_gpkg_path = convert_kml_to_shp(path_to_store, "local_do_estudo", shp_gpkg_folder)

    create_vector_layer(competitor_gpkg_path, "Camada da concorrencia")
    create_vector_layer(path_to_csv, "Camada de Texto da concorrencia")
    create_vector_layer(store_gpkg_path, "Camada do local do estudo")

    list_layers = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
    print(list_layers)

    open_model(path_to_model, competitor_gpkg_path, path_to_csv, store_gpkg_path)

    exit_qgis()

