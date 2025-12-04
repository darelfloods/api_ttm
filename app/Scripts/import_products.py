import pandas as pd
import asyncio
from app.Db.Connection import products_collection
import os

async def import_products_from_excel(excel_file_path: str):
    """
    Importe les produits depuis un fichier Excel vers MongoDB
    """
    try:
        # Lire le fichier Excel
        df = pd.read_excel(excel_file_path)
        
        # Convertir le DataFrame en liste de dictionnaires
        products = df.to_dict('records')
        
        # Insérer les produits dans MongoDB
        if products:
            await products_collection.insert_many(products)
            print("Import des produits terminé avec succès!")
        
    except Exception as e:
        print(f"Erreur lors de l'import: {str(e)}")

if __name__ == "__main__":
    # Chemin vers votre fichier Excel
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file_path = os.path.join(current_dir, "..", "data", "products.xlsx")
    
    # Vérifier si le fichier existe
    if not os.path.exists(excel_file_path):
        print(f"Le fichier {excel_file_path} n'existe pas!")
        print("Veuillez créer un fichier Excel 'products.xlsx' dans le dossier 'app/data' avec les colonnes suivantes:")
        print("- name (obligatoire)")
        print("- description (optionnel)")
        print("- price (obligatoire)")
        print("- stock (obligatoire)")
        print("- category (optionnel)")
        print("- pharmacy (obligatoire)")
        print("- cip (obligatoire)")
    else:
        # Exécuter l'import de manière asynchrone
        asyncio.run(import_products_from_excel(excel_file_path)) 