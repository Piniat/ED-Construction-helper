import os
import time
import glob
import configparser
import json
from modules import state, journal_logging, delivery_tracking, exit_app, select_app_mode, shopping_list, clean_screen

def get_latest_journal():
    latest_file = glob.glob(os.path.join(state.journal_folder, 'Journal.*.log'))
    if not latest_file:
        print("No journal files found.")
    newest_file = max(latest_file, key=os.path.getctime)
    return newest_file

def start():
    clean_screen.clear_screen()
    print('ED Construction helper v0.7.0-beta \n Type "help" for a list of commands')
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    state.journal_folder
    state.journal_folder = config['JOURNAL_PATH']['path']
    journal_file_path = get_latest_journal()
    if journal_file_path == "None":
        print("No journal files found. Exiting...")
        time.sleep(1)
        exit_app.close_app()
    if not journal_file_path:
        print("No journal files found.")
        time.sleep(1)
        exit_app.close_app()
    select_app_mode.app_mode_selection()
    state.ship_cargo_space = 0
    #nice list down there huh?
    state.all_comodities = [
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
    cargo_file = os.path.join(state.journal_folder, "Cargo.json")
    try:
        with open(cargo_file, "r") as cargo:
            cargo_data = json.load(cargo)
            current_cargo_list = cargo_data.get("Inventory", [])
            current_cargo_data = {item['Name']: item['Count'] for item in current_cargo_list}
    except json.JSONDecodeError:
        print(f"Json decode error")
    try:
        with open(journal_file_path) as f:
            f.seek(0, os.SEEK_END)
            while True:
                state.lines = f.readlines()
                if not state.lines and state.just_started == False and state.app_mode != "1":
                    time.sleep(0.1)
                    continue
                if state.app_mode == "3":
                    state.just_started = False
                    journal_logging.log_mode()
                elif state.app_mode == "2":
                    state.just_started = False
                    shopping_list.tracking_mode()
                elif state.app_mode == "1":
                    state.just_started = False
                    delivery_tracking.colonisation_tracker()
                    time.sleep(0.3)
    except json.JSONDecodeError:
        print(f"Json decode error")

