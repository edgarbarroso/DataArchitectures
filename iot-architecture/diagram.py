from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.gcp.api import APIGateway
from diagrams.gcp.iot import IotCore
from diagrams.gcp.network import CDN
from diagrams.gcp.storage import Storage
from diagrams.gcp.compute import Run, Functions
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.database import SQL, Memorystore
from diagrams.gcp.analytics import PubSub, Dataflow, Bigquery
from diagrams.onprem.analytics import Tableau, PowerBI
from diagrams.firebase.develop import Authentication
from diagrams.generic.device import Mobile, Tablet
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana, Logstash, Beats
from diagrams.programming.flowchart import Action

# Colores
black = "#555555"
orange = "#D85E14"
dark_blue = "#023059"
light_blue = "#2A8782"

with Diagram(name="Arquitectura IoT (agricultura y ganadería)", show=False, filename="iot-architecture"):  
  web = Custom("Web", "./assets/internet.png")

  with Cluster("Local"):    
    maquinaria = Custom("Maquinaria", "./assets/tractor.png")
    ganaderia = Custom("Ganadería", "./assets/ganado.png")    
    hub = Custom("Dispositivo IoT", "./assets/hub.png")
    sensor1 = Custom("sensor", "./assets/sensor.png")
    sensor2 = Custom("sensor", "./assets/sensor.png")
    sensor3 = Custom("sensor", "./assets/sensor.png")
    sensor4 = Custom("sensor", "./assets/sensor.png")

    with Cluster("Agricultura"):
      maiz= Custom("", "./assets/maiz.png")
      trigo = Custom("", "./assets/trigo.png")      

  with Cluster("Visualización"):    
    smartphone = Mobile("Smartphone")
    tablet = Tablet("Tablet")
    computer = Custom("Computadora", "./assets/computer.png")
    tableau = Tableau("Tableau")
    powerbi = PowerBI("Power BI")
    gds = Custom("Google Data Studio", "./assets/google-data-studio.png")

  with Cluster("Servicios Externos"):
    with Cluster("Archivos"):
      drive = Custom("Google Drive", "./assets/google-drive.png")
      csv = Custom("CSV", "./assets/file.png")

    with Cluster("Formularios"):
      kobotoolbox = Custom("Kobotoolbox", "./assets/kobotoolbox.png")

  with Cluster("Google Cloud Platform"):    
    scheduler = Scheduler("Scheduler\n(Programador de Tareas)")
    firebase_auth = Authentication("Firebase Authentication")
    cdn = CDN("Cloud CDN\n(Distribución de contenido)")

    with Cluster("Ingesta de datos"):
      iot_core = IotCore("IoT Core\n(Administrar dispositivos IoT )")
      pubsub = PubSub("PubSub\n(Cola de mensajes)")

    with Cluster("Procesamiento"):
      agregacion = Dataflow("Dataflow\n(Agregación)")
      decodificacion = Dataflow("Dataflow\n(Decodificación)")

    with Cluster("Almacenamiento de datos"):
      bigquery = Bigquery("BigQuery\n(Almacen de datos)")
      base_datos = SQL("SQL\n(Historico, BD Core)")
      cache = Memorystore("Memorystore\n(Cache)")

    with Cluster("Backend"):
      contenedor = Run("Cloud Run\n(Aplicación)")
      bucket = Storage("Storage\n(Multimedia, Archivos)")

    with Cluster("Integración externa"):
      function1 = Functions("Cloud Function\n(Servicio 1)")
      functions = Functions("Cloud Function\n(Servicio N)")
      api_gateway = APIGateway("API Gateway")

    with Cluster("Registros y monitoreo"):
      elasticsearch = Elasticsearch("Elasticsearch\n(Registro de eventos/errores)")      
      logstash = Logstash("Logstash\n(Procesamiento de logs)")
      beats = Beats("Beats\n(Ingesta)")
      kibana = Kibana("Kibana\n(Monitorización y Debugging)")

  # Conexiones Local
  maiz >> Edge(color=black, style="dotted") >> sensor1
  trigo >> Edge(color=black, style="dotted") >> sensor2
  maquinaria >> Edge(color=black, style="dotted") >> sensor3
  ganaderia >> Edge(color=black, style="dotted") >> sensor4
  [sensor1, sensor2, sensor3, sensor4] >> Edge(color=black, style="dotted") >> hub
  hub >> Edge(color=black) >> iot_core

  # Conexiones GCP - Ingesta de datos
  iot_core >> Edge(color=black, style="dotted") >> pubsub
  pubsub >> Edge(color=black, style="dotted") >> decodificacion

  # Conexiones GCP - Procesamiento
  decodificacion >> Edge(color=black, style="dotted") >> bigquery
  agregacion << Edge(color=black, style="dotted") >> bigquery
  agregacion >> Edge(color=black, style="dotted") >> base_datos

  # Conexiones GCP - Almacenamiento de datos
  base_datos << Edge(color=black, style="dotted") >> cache
  bigquery << Edge(color=black, style="dotted") >> cache
  cache << Edge(color=black, style="dotted") >> contenedor

  # Conexiones GCP - Backend
  contenedor << Edge(color=black, style="dotted") >> bucket
  firebase_auth << Edge(color=black, style="dotted") >> contenedor
  cdn << Edge(color=black, style="dotted") >> firebase_auth

  # Conexiones GCP - Integración externa
  function1 >> Edge(color=black, style="dotted") >> api_gateway
  functions << Edge(color=black, style="dotted") >> api_gateway
  function1 << Edge(color=black, style="dotted") << cache
  functions << Edge(color=black, style="dotted") >> cache

  # Conexiones GCP - Visualización
  [ smartphone, tablet, computer ] << Edge(color=orange) >> web
  web << Edge(color=orange) >> cdn
  gds << Edge(color=dark_blue) >> bigquery
  [ tableau, powerbi ] << Edge(color=dark_blue) >> cache

  # Conexiones GCP - Registros y monitoreo
  beats >> Edge(color=black, style="dotted") >> logstash
  logstash >> Edge(color=black, style="dotted") >> elasticsearch
  elasticsearch >> Edge(color=black, style="dotted") >> kibana
  beats << Edge(color=light_blue, style="dashed") << contenedor
  beats << Edge(color=light_blue, style="dashed") << [ function1, functions ]

  # Conexiones GCP - Servicios Externos
  csv >> Edge(color=dark_blue) >> bucket
  kobotoolbox >> Edge(color=dark_blue) >> api_gateway

  # GCP - Otros
  scheduler - Edge(color=black, style="dotted") - agregacion