#IMPORTANT!!
updater_verion = None
cargo_read_attempts = 0
journal_file_path = None
new_journal_file = None
shopping_list_exists = True
journal_folder = ""
ship_docked = False
docked_at_construction = False
input_started = False
updated_cargo = {}
get_updated_cargo = {}
initialized = False
ship_cargo_space = 0
item_name_list = []
item_count_list = []
delivered_amount = []
ready_to_print = True
current_amount_delivered = {}
last_delivered_amount = {}
switched = False
item_name = []
lines = []
input_thread = None
total = 0
app_mode = None
just_started = True
event = {}
formatted_timestamp = None
REPO = "https://api.github.com/repos/Piniat/ED-Construction-helper/releases/latest"
REPO_ALL = "https://api.github.com/repos/Piniat/ED-Construction-helper/releases"
current_version = None
update_attempts = 0
last_release = None
last_updater_release = None
user_os = None
item_count = 0
percent_complete = None
contributed_display_amount = []
contributed_display_name = []
all_comodities = [
    "Agronomic Treatment",
    "Explosives",
    "Hydrogen Fuel",
    "Hydrogen Peroxide",
    "Liquid Oxygen",
    "Mineral Oil",
    "Nerve Agents",
    "Pesticides",
    "Rockforth Fertiliser",
    "Surface Stabilisers",
    "Synthetic Reagents",
    "Tritium",
    "Water",
    "Clothing",
    "Consumer Technology",
    "Domestic Appliances",
    "Evacuation Shelter",
    "Survival Equipment",
    "Algae",
    "Animal Meat",
    "Coffee",
    "Fish",
    "Food Cartridges",
    "Fruit and Vegetables",
    "Grain",
    "Synthetic Meat",
    "Tea",
    "Ceramic Composites",
    "CMM Composite",
    "Insulating Membrane",
    "Meta-Alloys",
    "Micro-Weave Cooling Hoses",
    "Neofabric Insulation",
    "Polymers",
    "Semiconductors",
    "Superconductors",
    "Beer",
    "Bootleg Liquor",
    "Liquor",
    "Narcotics",
    "Onionhead Gamma Strain",
    "Tobacco",
    "Wine",
    "Articulation Motors",
    "Atmospheric Processors",
    "Building Fabricators",
    "Crop Harvesters",
    "Emergency Power Cells",
    "Energy Grid Assembly",
    "Exhaust Manifold",
    "Geological Equipment",
    "Heatsink Interlink",
    "HN Shock Mount",
    "Magnetic Emitter Coil",
    "Marine Equipment",
    "Microbial Furnaces",
    "Mineral Extractors",
    "Modular Terminals",
    "Power Converter",
    "Power Generators",
    "Power Transfer Bus",
    "Radiation Baffle",
    "Reinforced Mounting Plate",
    "Skimmer Components",
    "Thermal Cooling Units",
    "Water Purifiers",
    "Advanced Medicines",
    "Agri-Medicines",
    "Basic Medicines",
    "Combat Stabilisers",
    "Performance Enhancers",
    "Progenitor Cells",
    "Aluminium",
    "Beryllium",
    "Bismuth",
    "Cobalt",
    "Copper",
    "Gallium",
    "Gold",
    "Hafnium 178",
    "Indium",
    "Lanthanum",
    "Lithium",
    "Osmium",
    "Palladium",
    "Platinum",
    "Platinum Alloy",
    "Praseodymium",
    "Samarium",
    "Silver",
    "Tantalum",
    "Thallium",
    "Thorium",
    "Titanium",
    "Uranium",
    "Alexandrite",
    "Bauxite",
    "Benitoite",
    "Bertrandite",
    "Bromellite",
    "Coltan",
    "Cryolite",
    "Gallite",
    "Goslarite",
    "Grandidierite",
    "Indite",
    "Jadeite",
    "Lepidolite",
    "Lithium Hydroxide",
    "Low Temperature Diamonds",
    "Methane Clathrate",
    "Methanol Monohydrate Crystals",
    "Moissanite",
    "Monazite",
    "Musgravite",
    "Painite",
    "Pyrophyllite",
    "Rhodplumsite",
    "Rutile",
    "Serendibite",
    "Taaffeite",
    "Uraninite",
    "Void Opals",
    "AI Relics",
    "Ancient Artefact",
    "Ancient Key",
    "Anomaly Particles",
    "Antimatter Containment Unit",
    "Antique Jewellery",
    "Antiquities",
    "Assault Plans",
    "Black Box",
    "Commercial Samples",
    "Damaged Escape Pod",
    "Data Core",
    "Diplomatic Bag",
    "Earth Relics",
    "Encrypted Correspondence",
    "Encrypted Data Storage",
    "Experimental Chemicals",
    "Fossil Remnants",
    "Gene Bank",
    "Geological Samples",
    "Guardian Casket",
    "Guardian Orb",
    "Guardian Relic",
    "Guardian Tablet",
    "Guardian Totem",
    "Guardian Urn",
    "Hostage",
    "Large Survey Data Cache",
    "Military Intelligence",
    "Military Plans",
    "Mollusc Brain Tissue",
    "Mollusc Fluid",
    "Mollusc Membrane",
    "Mollusc Mycelium",
    "Mollusc Soft Tissue",
    "Mollusc Spores",
    "Mysterious Idol",
    "Occupied Escape Pod",
    "Personal Effects",
    "Pod Core Tissue",
    "Pod Dead Tissue",
    "Pod Mesoglea",
    "Pod Outer Tissue",
    "Pod Shell Tissue",
    "Pod Surface Tissue",
    "Pod Tissue",
    "Political Prisoner",
    "Precious Gems",
    "Prohibited Research Materials",
    "Prototype Tech",
    "Rare Artwork",
    "Rebel Transmissions",
    "SAP 8 Core Container",
    "Scientific Research",
    "Scientific Samples",
    "Small Survey Data Cache",
    "Space Pioneer Relics",
    "Tactical Data",
    "Technical Blueprints",
    "Thargoid Basilisk Tissue Sample",
    "Thargoid Biological Matter",
    "Thargoid Bio-Storage Capsule",
    "Thargoid Cyclops Tissue Sample",
    "Thargoid Glaive Tissue Sample",
    "Thargoid Heart",
    "Thargoid Hydra Tissue Sample",
    "Thargoid Link",
    "Thargoid Orthrus Tissue Sample",
    "Thargoid Probe",
    "Thargoid Resin",
    "Thargoid Sensor",
    "Thargoid Medusa Tissue Sample",
    "Thargoid Scout Tissue Sample",
    "Thargoid Technology Samples",
    "Time Capsule",
    "Titan Deep Tissue Sample",
    "Titan Maw Deep Tissue Sample",
    "Titan Maw Partial Tissue Sample",
    "Titan Maw Tissue Sample",
    "Titan Partial Tissue Sample",
    "Titan Tissue Sample",
    "Trade Data",
    "Trinkets of Hidden Fortune",
    "Unclassified Relic",
    "Unoccupied Escape Pod",
    "Unstable Data Core",
    "Wreckage Components",
    "Imperial Slaves",
    "Slaves",
    "Advanced Catalysers",
    "Animal Monitors",
    "Aquaponic Systems",
    "Auto Fabricators",
    "Bioreducing Lichen",
    "Computer Components",
    "H.E. Suits",
    "Hardware Diagnostic Sensor",
    "Ion Distributor",
    "Land Enrichment Systems",
    "Medical Diagnostic Equipment",
    "Micro Controllers",
    "Muon Imager",
    "Nanobreakers",
    "Resonating Separators",
    "Robotics",
    "Structural Regulators",
    "Telemetry Suite",
    "Conductive Fabrics",
    "Leather",
    "Military Grade Fabrics",
    "Natural Fabrics",
    "Synthetic Fabrics",
    "Biowaste",
    "Chemical Waste",
    "Scrap",
    "Toxic Waste",
    "Battle Weapons",
    "Landmines",
    "Non-Lethal Weapons",
    "Personal Weapons",
    "Reactive Armour",
    "Terrain Enrichment Systems",
    "Steel"
]